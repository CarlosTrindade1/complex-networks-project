"""Caracteriza as comunidades distintas produzidas pelo GRASP determinístico."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from analyze_community_characterization import (
    field_label,
    fmt_node,
    normalize_field,
    pagerank_unweighted,
    parse_relations,
    percentile_scores,
)
from community_heuristic import (
    ExactReach,
    internal_arc_count,
    is_cpm_feasible,
    is_weakly_connected,
    load_baseline_graph,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "community_results/heuristic/characterization"
RUNS = ROOT / "community_results/heuristic/exact_reach"
INTERPRETATIONS = ROOT / "community_characterization/heuristic_community_interpretations.json"
CLASS_LABELS = {
    "agrupamento_misto": "agrupamento misto",
    "agrupamento_tematico": "agrupamento temático",
    "linhagem_cientifica": "linhagem científica",
    "tradicao_intelectual": "tradição intelectual",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def collect_distinct_solutions() -> list[dict]:
    """IDs 0–29 follow median seeds; later IDs are additional p25 solutions."""
    by_nodes: dict[tuple[str, ...], dict] = {}
    ordered: list[dict] = []
    for gamma_label in ("mediana", "p25"):
        for seed in range(30):
            path = RUNS / gamma_label / f"run_{seed:02d}.json"
            with path.open(encoding="utf-8") as handle:
                record = json.load(handle)
            if record["status"] != "ok":
                raise ValueError(f"Execução sem solução: {path}")
            nodes = tuple(record["solution"]["nodes"])
            if nodes not in by_nodes:
                item = {
                    "community_id": len(ordered),
                    "nodes": frozenset(nodes),
                    "solution": record["solution"],
                    "occurrences": [],
                }
                by_nodes[nodes] = item
                ordered.append(item)
            by_nodes[nodes]["occurrences"].append((gamma_label, seed))
    return ordered


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    graph = load_baseline_graph(ROOT)
    reach = ExactReach(graph)
    solutions = collect_distinct_solutions()
    with INTERPRETATIONS.open(encoding="utf-8") as handle:
        interpretations = {int(key): value for key, value in json.load(handle).items()}
    if set(interpretations) != set(range(len(solutions))):
        raise ValueError("A curadoria não cobre exatamente as comunidades distintas.")

    leiden_membership = {
        row["node"]: int(row["community_id"])
        for row in read_csv(ROOT / "community_results/final_partitions/leiden_consensus_final.csv")
    }
    leiden_labels = {
        int(row["community_id"]): row["interpretive_label"]
        for row in read_csv(ROOT / "community_results/baseline/baseline_communities.csv")
    }
    elite_nodes = {
        label: {
            frozenset(item["nodes"])
            for item in json.loads((RUNS / f"elite_{label}.json").read_text(encoding="utf-8"))["elite"]
        }
        for label in ("mediana", "p25")
    }

    fields_by_node: dict[str, set[str]] = {}
    network_fields: Counter[str] = Counter()
    for node in graph:
        raw = graph.nodes[node].get("field")
        if raw:
            fields = {normalize_field(part) for part in str(raw).split(";") if part.strip()}
            if fields:
                fields_by_node[node] = fields
                network_fields.update(fields)
    annotated_network = len(fields_by_node)

    characterization_rows = []
    representative_rows = []
    edge_rows = []
    field_rows = []
    details = {}

    for item in solutions:
        cid = item["community_id"]
        nodes = item["nodes"]
        size = len(nodes)
        saved = item["solution"]
        if size != saved["size"] or not is_weakly_connected(graph, nodes):
            raise ValueError(f"Comunidade {cid} inválida ou desconectada")
        if internal_arc_count(graph, nodes) != saved["internal_arcs"]:
            raise ValueError(f"Arcos internos divergentes na comunidade {cid}")
        if reach.total(nodes) != saved["total_reach"]:
            raise ValueError(f"Alcance divergente na comunidade {cid}")
        for label, _ in item["occurrences"]:
            gamma = json.loads((RUNS / "config.json").read_text(encoding="utf-8"))["gammas"][label]
            if not is_cpm_feasible(graph, nodes, gamma):
                raise ValueError(f"CPM inviável na comunidade {cid} / {label}")

        subgraph = graph.subgraph(nodes)
        pagerank = pagerank_unweighted(subgraph)
        node_mask = sum(1 << reach.positions[node] for node in nodes)
        individual_external = {}
        internal_reach = {}
        internal_out_degree = {}
        unique_reach = {}
        for node in nodes:
            mask = reach.masks[reach.scc_by_node[node]]
            internal_reach[node] = (mask & node_mask).bit_count()
            individual_external[node] = mask.bit_count() - internal_reach[node]
            internal_out_degree[node] = sum(target in nodes for target in graph.successors(node))
            unique_reach[node] = saved["total_reach"] - reach.total(nodes - {node})

        reach_percentile = percentile_scores(individual_external)
        internal_percentile = percentile_scores(internal_reach)
        pagerank_percentile = percentile_scores(pagerank)
        degree_percentile = percentile_scores(internal_out_degree)
        score = {}
        for node in nodes:
            reach_component = (
                reach_percentile[node]
                if max(individual_external.values()) > 0
                else internal_percentile[node]
            )
            score[node] = (
                0.45 * reach_component
                + 0.35 * pagerank_percentile[node]
                + 0.20 * degree_percentile[node]
            )
        ordered_nodes = sorted(nodes, key=lambda node: (
            -score[node], -individual_external[node], -pagerank[node], node
        ))
        for rank, node in enumerate(ordered_nodes, start=1):
            representative_rows.append({
                "community_id": cid,
                "rank": rank,
                "node": node,
                "representative_score": score[node],
                "individual_total_reach": reach.total({node}),
                "individual_external_reach": individual_external[node],
                "internal_reach": internal_reach[node],
                "unique_reach_loss_if_removed": unique_reach[node],
                "internal_pagerank": pagerank[node],
                "internal_out_degree": internal_out_degree[node],
                "leiden_community_id": leiden_membership[node],
            })

        edges = list(subgraph.edges(data=True))
        relation_counts: Counter[str] = Counter()
        for source, target, data in edges:
            relation_counts.update(parse_relations(data.get("relations")))
        incident = sum(
            source in nodes or target in nodes for source, target in graph.edges()
        )
        ranked_edges = sorted(edges, key=lambda edge: (
            -(score[edge[0]] + score[edge[1]]), edge[0], edge[1]
        ))
        for rank, (source, target, data) in enumerate(ranked_edges, start=1):
            edge_rows.append({
                "community_id": cid,
                "rank": rank,
                "source": source,
                "target": target,
                "relations": ";".join(parse_relations(data.get("relations"))),
            })

        annotated_nodes = sorted(nodes & fields_by_node.keys())
        local_fields: Counter[str] = Counter()
        for node in annotated_nodes:
            local_fields.update(fields_by_node[node])
        for field, count in sorted(local_fields.items()):
            field_rows.append({
                "community_id": cid,
                "field": field_label(field),
                "community_field_nodes": count,
                "network_field_nodes": network_fields[field],
                "field_coverage": len(annotated_nodes) / size,
                "enrichment_ratio_annotated":
                    (count / len(annotated_nodes)) / (network_fields[field] / annotated_network),
                "supported_evidence": len(annotated_nodes) / size >= 0.05 and count >= 2,
            })

        leiden_counts = Counter(leiden_membership[node] for node in nodes)
        interpretation = interpretations[cid]
        occurrences = ";".join(f"{label}:{seed:02d}" for label, seed in item["occurrences"])
        elite_labels = ";".join(label for label in ("mediana", "p25") if nodes in elite_nodes[label])
        row = {
            "community_id": cid,
            "interpretive_label": interpretation["label"],
            "classification": interpretation["classification"],
            "confidence": interpretation["confidence"],
            "size": size,
            "external_reach": saved["external_reach"],
            "external_reach_per_node": saved["external_reach_per_node"],
            "directed_density": saved["directed_density"],
            "internal_edges": len(edges),
            "internal_influence_edges": relation_counts["influenced"],
            "internal_doctoral_supervision_edges": relation_counts["doctoralSupervision"],
            "internal_edge_share_incident": len(edges) / incident if incident else 0.0,
            "field_coverage": len(annotated_nodes) / size,
            "leiden_community_count": len(leiden_counts),
            "leiden_composition": ";".join(f"{key}:{count}" for key, count in sorted(leiden_counts.items())),
            "occurrences": occurrences,
            "elite_in": elite_labels,
            "representative_vertices": ";".join(ordered_nodes[:5]),
            "nodes": ";".join(sorted(nodes)),
            "interpretive_note": interpretation["note"],
        }
        characterization_rows.append(row)
        details[cid] = {
            "representatives": ordered_nodes,
            "unique_reach": unique_reach,
            "individual_external": individual_external,
            "pagerank": pagerank,
            "edges": ranked_edges,
            "leiden_counts": leiden_counts,
            "supported_fields": [field for field, count in local_fields.items()
                                 if len(annotated_nodes) / size >= 0.05 and count >= 2],
        }

    write_csv(OUTPUT / "communities.csv", characterization_rows, list(characterization_rows[0]))
    write_csv(OUTPUT / "representatives.csv", representative_rows, list(representative_rows[0]))
    write_csv(OUTPUT / "internal_edges.csv", edge_rows, list(edge_rows[0]))
    write_csv(OUTPUT / "fields.csv", field_rows, [
        "community_id", "field", "community_field_nodes", "network_field_nodes",
        "field_coverage", "enrichment_ratio_annotated", "supported_evidence",
    ])

    counts = Counter(row["classification"] for row in characterization_rows)
    lines = [
        "# Caracterização das comunidades propagadoras do GRASP",
        "",
        "## Método",
        "",
        "As 60 execuções geraram 31 conjuntos de vértices distintos. Os IDs 0–29 correspondem às sementes 0–29 com `γ` mediano; o ID 30 é a variante adicional da semente 23 com `γ` no percentil 25. Conjuntos repetidos são caracterizados uma vez, com todas as ocorrências registradas na tabela. Cada conjunto é fracamente conexo e satisfaz o CPM da configuração em que ocorreu.",
        "",
        "A caracterização segue o protocolo Leiden: campos enriquecidos entre os vértices anotados, representantes por alcance e PageRank interno, tipos de relações internas e inspeção substantiva dos vértices e arestas. Acrescenta-se o alcance perdido ao retirar cada integrante, para identificar sua contribuição exclusiva ao alcance coletivo. Os rótulos Leiden aparecem apenas como contexto: a classificação é feita para cada conjunto da heurística.",
        "",
        "`field` está ausente em 30 dos 31 conjuntos e aparece em apenas um vértice do conjunto restante. Nenhum campo atinge simultaneamente duas ocorrências e cobertura de 5%; portanto, os rótulos não se apoiam em `field`. Nenhum conjunto foi classificado como escola candidata. As classes `tradição intelectual`, `linhagem científica`, `agrupamento temático` e `agrupamento misto` descrevem a evidência observável, sem afirmar identidade doutrinária.",
        "",
        "## Síntese",
        "",
        f"Foram caracterizados {len(characterization_rows)} conjuntos distintos: "
        + ", ".join(f"{count} {CLASS_LABELS[name]}" for name, count in sorted(counts.items())) + ".",
        "",
        "| ID | Rótulo | Classe | Confiança | Integrantes | Alcance externo | Leiden |",
        "|---:|---|---|---|---:|---:|---:|",
    ]
    for row in sorted(characterization_rows, key=lambda row: -row["external_reach"]):
        lines.append(
            f"| {row['community_id']} | {row['interpretive_label']} | "
            f"{CLASS_LABELS[row['classification']]} | {row['confidence']} | "
            f"{row['size']} | {row['external_reach']} | {row['leiden_community_count']} |"
        )
    lines.extend(["", "## Fichas por conjunto", ""])
    for row in characterization_rows:
        cid = row["community_id"]
        detail = details[cid]
        composition = "; ".join(
            f"{key}: {count} — {leiden_labels[key]}"
            for key, count in detail["leiden_counts"].most_common()
        )
        reps = "; ".join(
            f"{fmt_node(node)} (alcance ext. individual {detail['individual_external'][node]}, "
            f"PR int. {detail['pagerank'][node]:.3g}, perda exclusiva {detail['unique_reach'][node]})"
            for node in detail["representatives"][:5]
        )
        edges = "; ".join(
            f"{fmt_node(source)} → {fmt_node(target)} [{';'.join(parse_relations(data.get('relations')))}]"
            for source, target, data in detail["edges"][:5]
        )
        lines.extend([
            f"### {cid} — {row['interpretive_label']}",
            "",
            f"**Classe:** `{row['classification']}` · **confiança:** {row['confidence']} · **integrantes:** {row['size']} · **alcance externo:** {row['external_reach']} · **ocorrências:** {row['occurrences']}.",
            "",
            f"**Interpretação:** {row['interpretive_note']}",
            "",
            f"**Composição Leiden:** {composition}.",
            "",
            f"**Representantes:** {reps}.",
            "",
            f"**Relações internas:** {row['internal_influence_edges']} de influência e {row['internal_doctoral_supervision_edges']} de orientação; densidade dirigida {row['directed_density']:.3f}; {row['internal_edge_share_incident']:.1%} das arestas incidentes são internas.",
            "",
            f"**Exemplos internos:** {edges}.",
            "",
            f"**Campos apoiados:** nenhum; cobertura de `field` {row['field_coverage']:.1%}.",
            "",
            "**Integrantes:** " + "; ".join(fmt_node(node) for node in row["nodes"].split(";")) + ".",
            "",
        ])
    lines.extend([
        "## Limitações",
        "",
        "Os grupos foram escolhidos para maximizar alcance sob conectividade fraca e coesão CPM. Por isso, podem atravessar tradições e comunidades Leiden. Arestas de orientação registram genealogia acadêmica e não implicam adesão doutrinária. As relações do DBpedia e a propagação transitiva com `p=1` medem potencial estrutural, não transmissão histórica observada. A ausência quase completa de `field` impede validar os rótulos por enriquecimento temático. Nenhum rótulo desta etapa afirma uma escola candidata; por esse motivo não foi feita uma verificação externa de escolas.",
        "",
    ])
    (OUTPUT / "characterization.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(solutions)} conjuntos distintos; {len(representative_rows)} linhas de representantes")
    print("Classes:", dict(counts))
    print("Saída:", OUTPUT)


if __name__ == "__main__":
    main()
