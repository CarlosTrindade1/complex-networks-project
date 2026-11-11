"""Consolida os resultados reproduzíveis do baseline do projeto.

Este script não executa nem define a heurística futura. Ele apenas lê os
artefatos já produzidos pelo pipeline do baseline, valida sua consistência e
gera uma visão consolidada para comparações posteriores.
"""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "community_results"
FINAL_DIR = RESULTS_DIR / "final_partitions"
INFLUENCE_DIR = RESULTS_DIR / "influence"
SEED_DIR = INFLUENCE_DIR / "seed_selection"
BASELINE_DIR = RESULTS_DIR / "baseline"


def _coerce(value: str):
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def read_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        return [
            {key: _coerce(value) for key, value in row.items()}
            for row in csv.DictReader(file)
        ]


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"Nenhuma linha para salvar em {path}")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def contingency(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    _, left_inverse = np.unique(left, return_inverse=True)
    _, right_inverse = np.unique(right, return_inverse=True)
    table = np.zeros(
        (left_inverse.max() + 1, right_inverse.max() + 1),
        dtype=np.int64,
    )
    np.add.at(table, (left_inverse, right_inverse), 1)
    return table


def partition_agreement(table: np.ndarray) -> dict[str, float]:
    n = int(table.sum())
    left_sizes = table.sum(axis=1)
    right_sizes = table.sum(axis=0)
    joint = table / n
    left_probability = left_sizes / n
    right_probability = right_sizes / n
    nonzero = np.nonzero(table)
    mutual_information = float(np.sum(
        joint[nonzero]
        * np.log(
            joint[nonzero]
            / (
                left_probability[nonzero[0]]
                * right_probability[nonzero[1]]
            )
        )
    ))
    left_entropy = float(-np.sum(left_probability * np.log(left_probability)))
    right_entropy = float(-np.sum(right_probability * np.log(right_probability)))
    nmi = 2 * mutual_information / (left_entropy + right_entropy)
    variation = left_entropy + right_entropy - 2 * mutual_information

    choose_two = lambda values: values * (values - 1) // 2
    index = int(choose_two(table).sum())
    left_index = int(choose_two(left_sizes).sum())
    right_index = int(choose_two(right_sizes).sum())
    total_pairs = n * (n - 1) // 2
    expected = left_index * right_index / total_pairs
    maximum = 0.5 * (left_index + right_index)
    ari = (index - expected) / (maximum - expected)

    return {
        "normalized_mutual_information": nmi,
        "adjusted_rand_index": ari,
        "variation_of_information_nats": variation,
    }


def load_partition(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        return data["membership"].copy(), data["nodes"].astype(str).copy()


def summarize_runs(algorithm: str) -> dict:
    rows = read_rows(RESULTS_DIR / f"{algorithm}_runs.csv")
    modularities = [row["modularity"] for row in rows]
    communities = [row["number_of_communities"] for row in rows]
    runtimes = [row["runtime_seconds"] for row in rows]
    return {
        "algorithm": algorithm,
        "runs": len(rows),
        "seed_minimum": min(row["seed"] for row in rows),
        "seed_maximum": max(row["seed"] for row in rows),
        "modularity_mean": statistics.fmean(modularities),
        "modularity_population_sd": statistics.pstdev(modularities),
        "modularity_minimum": min(modularities),
        "modularity_maximum": max(modularities),
        "communities_minimum": min(communities),
        "communities_maximum": max(communities),
        "runtime_seconds_mean": statistics.fmean(runtimes),
    }


def sensitivity_rows() -> list[dict]:
    rows = []
    for algorithm in ("louvain", "leiden"):
        baseline_membership, baseline_nodes = load_partition(
            FINAL_DIR / f"{algorithm}_consensus_final.npz"
        )
        for tau in (0.3, 0.5, 0.7):
            if tau == 0.5:
                membership = baseline_membership
                nodes = baseline_nodes
                iterations = 2
            else:
                tau_label = str(tau).replace(".", "_")
                membership, nodes = load_partition(
                    FINAL_DIR
                    / "sensitivity"
                    / f"{algorithm}_tau_{tau_label}_final.npz"
                )
                history = read_rows(
                    FINAL_DIR
                    / "sensitivity"
                    / f"{algorithm}_tau_{tau_label}_history.csv"
                )
                iterations = max(row["iteration"] for row in history)

            if not np.array_equal(nodes, baseline_nodes):
                raise ValueError(
                    f"Ordem de nós incompatível em {algorithm}, tau={tau}"
                )

            agreement = partition_agreement(
                contingency(baseline_membership, membership)
            )
            rows.append({
                "algorithm": algorithm,
                "tau": tau,
                "consensus_iterations": iterations,
                "communities": int(np.unique(membership).size),
                "nmi_vs_tau_0_5": agreement["normalized_mutual_information"],
                "ari_vs_tau_0_5": agreement["adjusted_rand_index"],
                "variation_of_information_nats_vs_tau_0_5": (
                    agreement["variation_of_information_nats"]
                ),
            })
    return rows


def consolidate_communities() -> list[dict]:
    characterization = read_rows(
        INFLUENCE_DIR / "leiden_community_characterization.csv"
    )
    propagation = {
        row["community_id"]: row
        for row in read_rows(
            INFLUENCE_DIR / "leiden_community_collective_propagation.csv"
        )
    }
    seed_summary = read_rows(
        SEED_DIR / "deterministic_seed_community_summary.csv"
    )
    seed_by_strategy_and_community = {
        (row["strategy"], row["community_id"]): row
        for row in seed_summary
    }

    rows = []
    for community in characterization:
        community_id = community["community_id"]
        influence = propagation[community_id]
        greedy = seed_by_strategy_and_community.get(
            ("greedy_celf", community_id), {}
        )
        degree = seed_by_strategy_and_community.get(
            ("maior_grau_saida", community_id), {}
        )
        rows.append({
            **community,
            "reached_nodes_collective": influence["reached_nodes"],
            "reach_fraction_network_collective": influence[
                "reach_fraction_network"
            ],
            "external_reach_fraction_network_collective": influence[
                "external_reach_fraction_network"
            ],
            "other_communities_reached_collective": influence[
                "other_communities_reached"
            ],
            "maximum_propagation_depth_collective": influence[
                "maximum_propagation_depth"
            ],
            "external_reach_per_collective_seed": influence[
                "external_reach_per_collective_seed"
            ],
            "rank_total_reach": influence["rank_total_reach"],
            "rank_collective_efficiency": influence[
                "rank_collective_efficiency"
            ],
            "greedy_seed_count": greedy.get("seed_count", 0),
            "greedy_seed_nodes": greedy.get("seed_nodes"),
            "degree_seed_count": degree.get("seed_count", 0),
            "degree_seed_nodes": degree.get("seed_nodes"),
        })

    if len(rows) != 96 or set(propagation) != {
        row["community_id"] for row in rows
    }:
        raise ValueError("As 96 comunidades não foram consolidadas corretamente")
    return rows


def artifact_rows() -> list[dict]:
    artifacts = [
        ("network", "dbpedia-network-canonical.graphml", "Rede canônica completa"),
        ("partition", "community_results/final_partitions/leiden_consensus_final.npz", "Partição Leiden consensual principal"),
        ("partition", "community_results/final_partitions/louvain_consensus_final.npz", "Partição Louvain consensual de referência"),
        ("stability", "community_results/leiden_runs.csv", "Cem execuções independentes de Leiden"),
        ("stability", "community_results/louvain_runs.csv", "Cem execuções independentes de Louvain"),
        ("partition_metrics", "community_results/final_partitions/partition_summary.csv", "Métricas das partições finais"),
        ("partition_agreement", "community_results/final_partitions/agreement_metrics.csv", "Concordância Louvain-Leiden"),
        ("characterization", "community_results/influence/leiden_community_characterization.csv", "Caracterização das 96 comunidades Leiden"),
        ("community_influence", "community_results/influence/leiden_community_collective_propagation.csv", "Propagação coletiva das comunidades"),
        ("seed_selection", "community_results/influence/seed_selection/deterministic_seed_selection_steps.csv", "Seleção e ganhos marginais das sementes"),
        ("seed_budgets", "community_results/influence/seed_selection/deterministic_seed_budget_comparison.csv", "Comparação de k=1, 5 e 10"),
        ("seed_characterization", "community_results/influence/seed_selection/deterministic_seed_community_characterization.csv", "Comunidades das sementes"),
        ("baseline_summary", "community_results/baseline/baseline_summary.json", "Resumo consolidado legível por máquina"),
        ("baseline_communities", "community_results/baseline/baseline_communities.csv", "Tabela consolidada por comunidade"),
        ("baseline_sensitivity", "community_results/baseline/baseline_sensitivity.csv", "Sensibilidade ao limiar de consenso"),
    ]
    rows = []
    for category, relative_path, description in artifacts:
        path = ROOT / relative_path
        rows.append({
            "category": category,
            "path": relative_path,
            "description": description,
            "exists": path.exists(),
        })
    return rows


def consolidate_baseline() -> dict:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)

    graph = nx.read_graphml(ROOT / "dbpedia-network-canonical.graphml")
    graph.remove_edges_from(nx.selfloop_edges(graph))
    largest_wcc = max(nx.weakly_connected_components(graph), key=len)
    baseline_graph = graph.subgraph(largest_wcc).copy()
    sccs = list(nx.strongly_connected_components(baseline_graph))
    condensed = nx.condensation(baseline_graph, scc=sccs)

    partition_summary = read_rows(FINAL_DIR / "partition_summary.csv")
    agreement_rows = read_rows(FINAL_DIR / "agreement_metrics.csv")
    agreement = {row["metric"]: row["value"] for row in agreement_rows}
    run_stability = [summarize_runs(name) for name in ("louvain", "leiden")]
    sensitivity = sensitivity_rows()
    communities = consolidate_communities()
    seed_budgets = read_rows(
        SEED_DIR / "deterministic_seed_budget_comparison.csv"
    )
    classifications = Counter(row["classification"] for row in communities)
    confidence = Counter(row["confidence"] for row in communities)

    summary = {
        "schema_version": "1.0",
        "status": "baseline_concluded",
        "network": {
            "source": "dbpedia-network-canonical.graphml",
            "directed": True,
            "canonical_nodes": graph.number_of_nodes(),
            "canonical_edges_without_self_loops": graph.number_of_edges(),
            "analysis_component": "largest_weakly_connected_component",
            "analysis_nodes": baseline_graph.number_of_nodes(),
            "analysis_edges": baseline_graph.number_of_edges(),
        },
        "community_detection": {
            "algorithms": ["louvain", "leiden"],
            "independent_runs_per_algorithm": 100,
            "seeds": {"minimum": 0, "maximum": 99},
            "consensus_threshold_primary": 0.5,
            "consensus_threshold_sensitivity": [0.3, 0.7],
            "selected_partition_for_interpretation": "leiden",
            "selected_partition_communities": 96,
            "partition_metrics": partition_summary,
            "louvain_leiden_agreement": agreement,
            "run_stability": run_stability,
            "sensitivity": sensitivity,
        },
        "influence_model": {
            "model": "deterministic_directed_reachability",
            "edge_activation_probability": 1.0,
            "scc_treatment": "condensation_dag",
            "strongly_connected_components": condensed.number_of_nodes(),
            "condensation_edges": condensed.number_of_edges(),
            "largest_scc_nodes": max(map(len, sccs)),
            "community_seed_interpretation": "all nodes in the community",
            "individual_seed_budgets": [1, 5, 10],
            "individual_seed_strategies": [
                "greedy_celf",
                "maior_grau_saida",
            ],
            "seed_budget_results": seed_budgets,
        },
        "characterization": {
            "communities": len(communities),
            "classification_counts": dict(classifications),
            "confidence_counts": dict(confidence),
            "field_annotated_nodes": 473,
            "analysis_nodes": baseline_graph.number_of_nodes(),
            "field_limitation": (
                "Field é esparso; evidência apoiada requer ao menos duas "
                "ocorrências e cobertura comunitária mínima de 5%."
            ),
        },
        "frozen_future_comparison_protocol": {
            "same_network": True,
            "same_deterministic_propagation": True,
            "same_scc_treatment": True,
            "same_partition_metrics": True,
            "same_influence_metrics": True,
            "note": "Nenhuma heurística é definida ou executada neste baseline.",
        },
        "limitations": [
            "Arestas representam relações diretas observadas no DBpedia.",
            "Propagação transitiva é uma hipótese estrutural do modelo.",
            "p=1 mede alcance potencial, não probabilidade empírica de difusão.",
            "A caracterização semântica é limitada pela baixa cobertura de field.",
            "A análise principal usa somente a maior componente fracamente conexa.",
        ],
    }

    write_rows(BASELINE_DIR / "baseline_communities.csv", communities)
    write_rows(BASELINE_DIR / "baseline_run_stability.csv", run_stability)
    write_rows(BASELINE_DIR / "baseline_sensitivity.csv", sensitivity)
    with (BASELINE_DIR / "baseline_summary.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)
        file.write("\n")

    artifacts = artifact_rows()
    write_rows(BASELINE_DIR / "baseline_artifact_index.csv", artifacts)
    if not all(row["exists"] for row in artifacts):
        missing = [row["path"] for row in artifacts if not row["exists"]]
        raise FileNotFoundError(f"Artefatos ausentes: {missing}")

    return summary


if __name__ == "__main__":
    result = consolidate_baseline()
    print(
        "Baseline consolidado: "
        f"{result['network']['analysis_nodes']:,} nós, "
        f"{result['community_detection']['selected_partition_communities']} "
        "comunidades Leiden."
    )
    print(f"Artefatos: {BASELINE_DIR.relative_to(ROOT)}")
