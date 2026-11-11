"""Caracteriza as comunidades consensuais Leiden (tau=0,5).

O script parte exclusivamente da rede canônica e dos artefatos persistidos da
partição/propagação. Ele acrescenta quatro camadas reproduzíveis:

1. campos distintivos em relação aos vértices anotados da rede analisada;
2. representantes que combinam alcance determinístico e centralidade interna;
3. composição e exemplos das relações internas de influência/orientação;
4. interpretação curada que separa escolas candidatas de outros agrupamentos.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "community_results"
INFLUENCE = RESULTS / "influence"
CHARACTERIZATION_CONFIG = ROOT / "community_characterization"
NETWORK_PATH = ROOT / "dbpedia-network-canonical.graphml"
MEMBERSHIP_PATH = RESULTS / "final_partitions" / "leiden_consensus_final.csv"
PROPAGATION_PATH = INFLUENCE / "leiden_community_collective_propagation.csv"
INTERPRETATIONS_PATH = CHARACTERIZATION_CONFIG / "leiden_community_interpretations.json"
EXTERNAL_SOURCES_PATH = CHARACTERIZATION_CONFIG / "leiden_community_external_sources.json"

DISTINCTIVE_FIELDS_PATH = INFLUENCE / "leiden_community_distinctive_fields.csv"
RELATION_SUMMARY_PATH = INFLUENCE / "leiden_community_internal_relations.csv"
REPRESENTATIVES_PATH = INFLUENCE / "leiden_community_representatives_reach_centrality.csv"
EDGE_EVIDENCE_PATH = INFLUENCE / "leiden_community_internal_edge_evidence.csv"
CHARACTERIZATION_PATH = INFLUENCE / "leiden_community_characterization.csv"
REPORT_PATH = INFLUENCE / "leiden_community_characterization.md"

TOP_FIELDS = 8
TOP_REPRESENTATIVES = 10
TOP_EDGES = 8


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"Nenhuma linha para salvar em {path}")
    if fieldnames is None:
        fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_relations(raw: object) -> tuple[str, ...]:
    if raw is None:
        return ()
    return tuple(part.strip() for part in str(raw).split(";") if part.strip())


def normalize_field(raw: str) -> str:
    return " ".join(raw.replace("_", " ").strip().split()).casefold()


def field_label(normalized: str) -> str:
    return normalized[:1].upper() + normalized[1:]


def weighted_bit_count(bits: int, extra_weights: dict[int, int]) -> int:
    total = bits.bit_count()
    for scc_id, extra in extra_weights.items():
        if bits & (1 << scc_id):
            total += extra
    return total


def percentile_scores(values: dict[str, float]) -> dict[str, float]:
    ordered = sorted(values, key=lambda node: (-values[node], node))
    denominator = max(len(ordered) - 1, 1)
    return {
        node: 1.0 - rank / denominator
        for rank, node in enumerate(ordered)
    }


def pagerank_unweighted(
    graph: nx.DiGraph,
    alpha: float = 0.85,
    tolerance: float = 1.0e-10,
    max_iterations: int = 500,
) -> dict[str, float]:
    """PageRank simples, sem dependência de SciPy, para um subgrafo dirigido."""
    nodes = list(graph)
    size = len(nodes)
    if size == 0:
        return {}
    scores = {node: 1.0 / size for node in nodes}
    base = (1.0 - alpha) / size

    for _ in range(max_iterations):
        updated = {node: base for node in nodes}
        dangling = alpha * sum(
            scores[node] for node in nodes if graph.out_degree(node) == 0
        ) / size
        for node in nodes:
            updated[node] += dangling
        for source in nodes:
            degree = graph.out_degree(source)
            if degree:
                contribution = alpha * scores[source] / degree
                for target in graph.successors(source):
                    updated[target] += contribution
        error = sum(abs(updated[node] - scores[node]) for node in nodes)
        scores = updated
        if error < size * tolerance:
            return scores

    raise RuntimeError("PageRank interno não convergiu.")


def fmt_node(node: str) -> str:
    return node.replace("__", " / ").replace("_", " ")


def supported_distinctive_fields(rows: list[dict]) -> list[dict]:
    """Evita tratar anotações raras de comunidades pouco cobertas como evidência."""
    if not rows or rows[0]["field_coverage"] < 0.05:
        return []
    return [row for row in rows if row["community_field_nodes"] >= 2]


def main() -> None:
    INFLUENCE.mkdir(parents=True, exist_ok=True)

    graph = nx.read_graphml(NETWORK_PATH)
    membership_rows = read_csv(MEMBERSHIP_PATH)
    node_to_community = {
        row["node"]: int(row["community_id"])
        for row in membership_rows
    }
    analysis_nodes = set(node_to_community)
    graph = graph.subgraph(analysis_nodes).copy()
    graph.remove_edges_from(list(nx.selfloop_edges(graph)))
    if graph.number_of_nodes() != 20_099 or graph.number_of_edges() != 31_545:
        raise ValueError("A rede analisada não coincide com a maior componente auditada.")

    communities: dict[int, set[str]] = defaultdict(set)
    for node, community_id in node_to_community.items():
        communities[community_id].add(node)

    with INTERPRETATIONS_PATH.open(encoding="utf-8") as file:
        interpretations = {
            int(key): value for key, value in json.load(file).items()
        }
    with EXTERNAL_SOURCES_PATH.open(encoding="utf-8") as file:
        external_sources = {
            int(key): value for key, value in json.load(file).items()
        }

    expected_ids = set(communities)
    if set(interpretations) != expected_ids:
        raise ValueError("As interpretações não cobrem exatamente as 96 comunidades.")

    propagation = {
        int(row["community_id"]): row
        for row in read_csv(PROPAGATION_PATH)
    }

    # Campos distintivos. A comparação usa apenas vértices com ao menos um
    # campo, reduzindo o viés produzido pela ausência maciça de anotações.
    fields_by_node: dict[str, set[str]] = {}
    global_field_counts: Counter[str] = Counter()
    for node in graph:
        raw = graph.nodes[node].get("field")
        fields = {
            normalize_field(part)
            for part in str(raw).split(";")
            if raw is not None and part.strip()
        }
        if fields:
            fields_by_node[node] = fields
            global_field_counts.update(fields)

    total_annotated_nodes = len(fields_by_node)
    distinctive_rows: list[dict] = []
    distinctive_by_community: dict[int, list[dict]] = defaultdict(list)

    for community_id, nodes in sorted(communities.items()):
        annotated_nodes = [node for node in nodes if node in fields_by_node]
        community_field_counts: Counter[str] = Counter()
        for node in annotated_nodes:
            community_field_counts.update(fields_by_node[node])

        candidates = []
        for field, local_count in community_field_counts.items():
            global_count = global_field_counts[field]
            local_prevalence = local_count / len(annotated_nodes)
            global_prevalence = global_count / total_annotated_nodes
            enrichment = local_prevalence / global_prevalence
            specificity = local_count / global_count
            score = math.sqrt(local_count) * math.log2(enrichment) * specificity
            candidates.append(
                {
                    "community_id": community_id,
                    "community_size": len(nodes),
                    "annotated_nodes": len(annotated_nodes),
                    "field_coverage": len(annotated_nodes) / len(nodes),
                    "field": field,
                    "field_label": field_label(field),
                    "community_field_nodes": local_count,
                    "network_field_nodes": global_count,
                    "community_prevalence_annotated": local_prevalence,
                    "network_prevalence_annotated": global_prevalence,
                    "enrichment_ratio": enrichment,
                    "log2_enrichment": math.log2(enrichment),
                    "field_specificity": specificity,
                    "distinctiveness_score": score,
                    "supported_evidence": (
                        len(annotated_nodes) / len(nodes) >= 0.05
                        and local_count >= 2
                    ),
                }
            )

        candidates.sort(
            key=lambda row: (
                not (row["community_field_nodes"] >= 2),
                -row["distinctiveness_score"],
                -row["community_field_nodes"],
                row["field"],
            )
        )
        for rank, row in enumerate(candidates[:TOP_FIELDS], start=1):
            row["field_rank"] = rank
            distinctive_rows.append(row)
            distinctive_by_community[community_id].append(row)

    write_csv(
        DISTINCTIVE_FIELDS_PATH,
        distinctive_rows,
        [
            "community_id", "community_size", "annotated_nodes", "field_coverage",
            "field_rank", "field", "field_label", "community_field_nodes",
            "network_field_nodes", "community_prevalence_annotated",
            "network_prevalence_annotated", "enrichment_ratio", "log2_enrichment",
            "field_specificity", "distinctiveness_score", "supported_evidence",
        ],
    )

    # Composição relacional interna e externa.
    relation_counts: dict[int, Counter[str]] = {
        community_id: Counter() for community_id in communities
    }
    internal_edges_by_community: dict[int, list[tuple[str, str, tuple[str, ...]]]] = defaultdict(list)

    for source, target, data in graph.edges(data=True):
        source_community = node_to_community[source]
        target_community = node_to_community[target]
        relations = parse_relations(data.get("relations"))
        if source_community == target_community:
            counts = relation_counts[source_community]
            counts["internal_edges"] += 1
            if len(relations) > 1:
                counts["internal_multirelation_edges"] += 1
            for relation in relations:
                counts[f"internal_{relation}"] += 1
            internal_edges_by_community[source_community].append(
                (source, target, relations)
            )
        else:
            source_counts = relation_counts[source_community]
            target_counts = relation_counts[target_community]
            source_counts["outgoing_external_edges"] += 1
            target_counts["incoming_external_edges"] += 1
            for relation in relations:
                source_counts[f"outgoing_external_{relation}"] += 1
                target_counts[f"incoming_external_{relation}"] += 1

    relation_rows: list[dict] = []
    for community_id, nodes in sorted(communities.items()):
        counts = relation_counts[community_id]
        internal_edges = counts["internal_edges"]
        incident_edges = (
            internal_edges
            + counts["outgoing_external_edges"]
            + counts["incoming_external_edges"]
        )
        influence_edges = counts["internal_influenced"]
        supervision_edges = counts["internal_doctoralSupervision"]
        relation_rows.append(
            {
                "community_id": community_id,
                "community_size": len(nodes),
                "internal_edges": internal_edges,
                "internal_influence_edges": influence_edges,
                "internal_doctoral_supervision_edges": supervision_edges,
                "internal_multirelation_edges": counts["internal_multirelation_edges"],
                "outgoing_external_edges": counts["outgoing_external_edges"],
                "incoming_external_edges": counts["incoming_external_edges"],
                "internal_edge_share_incident": internal_edges / incident_edges if incident_edges else 0.0,
                "doctoral_share_internal_typed": supervision_edges / (influence_edges + supervision_edges)
                if influence_edges + supervision_edges else 0.0,
                "internal_edge_density_directed": internal_edges / (len(nodes) * (len(nodes) - 1))
                if len(nodes) > 1 else 0.0,
            }
        )
    write_csv(RELATION_SUMMARY_PATH, relation_rows)

    # Alcance exato por SCC usando bitsets sobre o DAG de condensação.
    sccs = list(nx.strongly_connected_components(graph))
    if len(sccs) != 19_808:
        raise ValueError("A condensação não coincide com as 19.808 SCCs auditadas.")
    node_to_scc: dict[str, int] = {}
    for scc_id, nodes in enumerate(sccs):
        for node in nodes:
            node_to_scc[node] = scc_id

    condensation = nx.DiGraph()
    condensation.add_nodes_from(range(len(sccs)))
    for source, target in graph.edges:
        source_scc = node_to_scc[source]
        target_scc = node_to_scc[target]
        if source_scc != target_scc:
            condensation.add_edge(source_scc, target_scc)

    reach_bits: dict[int, int] = {}
    for scc_id in reversed(list(nx.topological_sort(condensation))):
        bits = 1 << scc_id
        for successor in condensation.successors(scc_id):
            bits |= reach_bits[successor]
        reach_bits[scc_id] = bits

    extra_global = {
        scc_id: len(nodes) - 1
        for scc_id, nodes in enumerate(sccs)
        if len(nodes) > 1
    }
    community_scc_masks: dict[int, int] = defaultdict(int)
    community_extra_weights: dict[int, dict[int, int]] = defaultdict(dict)
    for scc_id, scc_nodes in enumerate(sccs):
        counts = Counter(node_to_community[node] for node in scc_nodes)
        for community_id, count in counts.items():
            community_scc_masks[community_id] |= 1 << scc_id
            if count > 1:
                community_extra_weights[community_id][scc_id] = count - 1

    representative_rows: list[dict] = []
    representatives_by_community: dict[int, list[dict]] = defaultdict(list)
    all_scores: dict[str, float] = {}

    for community_id, nodes in sorted(communities.items()):
        subgraph = graph.subgraph(nodes)
        if len(nodes) == 1:
            pagerank = {next(iter(nodes)): 1.0}
        else:
            pagerank = pagerank_unweighted(subgraph)

        total_reach = {}
        internal_reach = {}
        internal_out_degree = {}
        for node in nodes:
            bits = reach_bits[node_to_scc[node]]
            total_reach[node] = weighted_bit_count(bits, extra_global)
            community_bits = bits & community_scc_masks[community_id]
            internal_reach[node] = weighted_bit_count(
                community_bits,
                community_extra_weights[community_id],
            )
            internal_out_degree[node] = sum(
                node_to_community[target] == community_id
                for target in graph.successors(node)
            )

        external_reach = {
            node: total_reach[node] - internal_reach[node]
            for node in nodes
        }
        reach_percentile = percentile_scores(external_reach)
        internal_reach_percentile = percentile_scores(internal_reach)
        pagerank_percentile = percentile_scores(pagerank)
        out_degree_percentile = percentile_scores(internal_out_degree)

        composite = {}
        for node in nodes:
            # Se a comunidade não alcança nós externos, o alcance interno
            # substitui o externo para evitar empates artificiais.
            reach_component = (
                reach_percentile[node]
                if max(external_reach.values()) > 0
                else internal_reach_percentile[node]
            )
            composite[node] = (
                0.45 * reach_component
                + 0.35 * pagerank_percentile[node]
                + 0.20 * out_degree_percentile[node]
            )

        ordered = sorted(
            nodes,
            key=lambda node: (
                -composite[node],
                -external_reach[node],
                -pagerank[node],
                node,
            ),
        )
        all_scores.update(composite)
        for rank, node in enumerate(ordered[:TOP_REPRESENTATIVES], start=1):
            row = {
                "community_id": community_id,
                "representative_rank": rank,
                "node": node,
                "representative_score": composite[node],
                "total_reach_nodes": total_reach[node],
                "internal_reach_nodes": internal_reach[node],
                "external_reach_nodes": external_reach[node],
                "internal_pagerank": pagerank[node],
                "out_degree": graph.out_degree(node),
                "in_degree": graph.in_degree(node),
                "internal_out_degree": internal_out_degree[node],
                "external_out_degree": graph.out_degree(node) - internal_out_degree[node],
                "scc_id": node_to_scc[node],
            }
            representative_rows.append(row)
            representatives_by_community[community_id].append(row)

    for row in representative_rows:
        collective_external = int(propagation[row["community_id"]]["external_reached_nodes"])
        if row["external_reach_nodes"] > collective_external:
            raise AssertionError("Alcance individual maior que o alcance coletivo da comunidade.")

    write_csv(REPRESENTATIVES_PATH, representative_rows)

    # Exemplos de relações internas priorizam arestas entre vértices que
    # também são representativos no critério alcance-centralidade.
    edge_rows: list[dict] = []
    for community_id, edges in sorted(internal_edges_by_community.items()):
        ranked = sorted(
            edges,
            key=lambda edge: (
                -(all_scores[edge[0]] + all_scores[edge[1]]),
                edge[0],
                edge[1],
            ),
        )
        for rank, (source, target, relations) in enumerate(ranked[:TOP_EDGES], start=1):
            edge_rows.append(
                {
                    "community_id": community_id,
                    "edge_rank": rank,
                    "source": source,
                    "target": target,
                    "relations": ";".join(relations),
                    "source_representative_score": all_scores[source],
                    "target_representative_score": all_scores[target],
                }
            )
    write_csv(EDGE_EVIDENCE_PATH, edge_rows)

    relation_by_community = {row["community_id"]: row for row in relation_rows}
    edge_evidence_by_community: dict[int, list[dict]] = defaultdict(list)
    for row in edge_rows:
        edge_evidence_by_community[row["community_id"]].append(row)

    characterization_rows: list[dict] = []
    for community_id, nodes in sorted(communities.items()):
        label, classification, confidence, note = interpretations[community_id]
        fields = distinctive_by_community[community_id]
        reliable_fields = supported_distinctive_fields(fields)
        representatives = representatives_by_community[community_id]
        relations = relation_by_community[community_id]
        prop = propagation[community_id]
        characterization_rows.append(
            {
                "community_id": community_id,
                "interpretive_label": label,
                "classification": classification,
                "confidence": confidence,
                "community_size": len(nodes),
                "field_coverage": fields[0]["field_coverage"] if fields else 0.0,
                "distinctive_fields_supported": "; ".join(
                    f"{row['field_label']} (n={row['community_field_nodes']}, {row['enrichment_ratio']:.1f}x)"
                    for row in reliable_fields[:3]
                ),
                "representative_vertices": "; ".join(
                    row["node"] for row in representatives[:5]
                ),
                "internal_influence_edges": relations["internal_influence_edges"],
                "internal_doctoral_supervision_edges": relations["internal_doctoral_supervision_edges"],
                "internal_edge_share_incident": relations["internal_edge_share_incident"],
                "external_reached_nodes_collective": int(prop["external_reached_nodes"]),
                "external_reach_rank": int(prop["rank_external_reach"]),
                "interpretive_note": note,
            }
        )
    write_csv(CHARACTERIZATION_PATH, characterization_rows)

    # Relatório legível, com uma síntese e a ficha das 96 comunidades.
    classification_counts = Counter(row["classification"] for row in characterization_rows)
    candidate_rows = [
        row for row in characterization_rows
        if row["classification"] == "escola_candidata"
    ]
    candidate_rows.sort(
        key=lambda row: (
            -row["external_reached_nodes_collective"],
            row["community_id"],
        )
    )
    candidate_ids = {row["community_id"] for row in candidate_rows}
    if set(external_sources) != candidate_ids:
        raise ValueError("Cada escola candidata deve ter uma fonte semântica externa.")

    lines = [
        "# Caracterização das comunidades consensuais Leiden (τ=0,5)",
        "",
        "## Critério de interpretação",
        "",
        "A caracterização não deriva do campo dominante. Ela combina campos enriquecidos em relação aos vértices anotados da rede, alcance determinístico individual, PageRank interno, composição das relações de influência/orientação e inspeção substantiva dos vértices e arestas mais representativos. Campos só entram como evidência apoiada no resumo quando têm pelo menos duas ocorrências e a cobertura de `field` da comunidade é de ao menos 5%; os demais continuam disponíveis na tabela exploratória, mas não sustentam o rótulo.",
        "",
        "`escola_candidata` é reservado a grupos com núcleo conceitual reconhecível e evidência relacional compatível. `tradição_intelectual` indica continuidade histórica ou conceitual mais ampla. `linhagem_científica` registra sobretudo genealogia de orientação/pesquisa. `agrupamento_temático` e `agrupamento_misto` significam que a evidência é insuficiente para afirmar escola de pensamento.",
        "",
        "## Síntese",
        "",
        f"Foram caracterizadas {len(characterization_rows)} comunidades: "
        + ", ".join(
            f"{count} {classification.replace('_', ' ')}"
            for classification, count in sorted(classification_counts.items())
        )
        + ".",
        "",
        "### Escolas candidatas, ordenadas pelo alcance coletivo externo",
        "",
        "| Comunidade | Rótulo | Confiança | Tamanho | Alcance externo | Influência interna | Orientação interna |",
        "|---:|---|---|---:|---:|---:|---:|",
    ]
    for row in candidate_rows:
        lines.append(
            f"| {row['community_id']} | {row['interpretive_label']} | {row['confidence']} | "
            f"{row['community_size']} | {row['external_reached_nodes_collective']} | "
            f"{row['internal_influence_edges']} | {row['internal_doctoral_supervision_edges']} |"
        )

    lines.extend(
        [
            "",
            "### Verificação semântica externa",
            "",
            "As fontes abaixo foram usadas apenas para verificar se o núcleo encontrado corresponde a uma tradição ou escola reconhecível; a atribuição comunitária e todas as métricas continuam sendo derivadas da rede.",
            "",
        ]
    )
    for row in candidate_rows:
        source = external_sources[row["community_id"]]
        lines.append(
            f"- **Comunidade {row['community_id']} — {row['interpretive_label']}:** "
            f"[{source['title']}]({source['url']}). {source['evidence']}"
        )

    lines.extend(["", "## Fichas por comunidade", ""])
    for row in characterization_rows:
        community_id = row["community_id"]
        representatives = representatives_by_community[community_id]
        edges = edge_evidence_by_community[community_id]
        fields = distinctive_by_community[community_id]
        reliable_fields = supported_distinctive_fields(fields)
        lines.extend(
            [
                f"### Comunidade {community_id} — {row['interpretive_label']}",
                "",
                f"**Classificação:** `{row['classification']}` · **confiança:** {row['confidence']} · **tamanho:** {row['community_size']} · **alcance externo coletivo:** {row['external_reached_nodes_collective']} (posição {row['external_reach_rank']}/96).",
                "",
                f"**Interpretação:** {row['interpretive_note']}",
                "",
                (
                    "**Verificação externa:** "
                    f"[{external_sources[community_id]['title']}]"
                    f"({external_sources[community_id]['url']}). "
                    f"{external_sources[community_id]['evidence']}"
                    if community_id in external_sources
                    else "**Verificação externa:** não necessária para um rótulo que não afirma escola candidata."
                ),
                "",
                "**Vértices representativos (alcance/centralidade):** "
                + "; ".join(
                    f"{fmt_node(item['node'])} (alcance ext. {item['external_reach_nodes']}, PR int. {item['internal_pagerank']:.3g})"
                    for item in representatives[:5]
                )
                + ".",
                "",
                "**Campos distintivos apoiados:** "
                + (
                    "; ".join(
                        f"{item['field_label']} (n={item['community_field_nodes']}, enriquecimento {item['enrichment_ratio']:.1f}×)"
                        for item in reliable_fields[:4]
                    )
                    if reliable_fields
                    else "nenhum que satisfaça simultaneamente suporte e cobertura mínimos"
                )
                + f". Cobertura de `field`: {row['field_coverage']:.1%}.",
                "",
                f"**Relações internas:** {row['internal_influence_edges']} arestas de influência e {row['internal_doctoral_supervision_edges']} de orientação; {row['internal_edge_share_incident']:.1%} das arestas incidentes são internas.",
                "",
                "**Exemplos internos:** "
                + (
                    "; ".join(
                        f"{fmt_node(item['source'])} → {fmt_node(item['target'])} [{item['relations']}]"
                        for item in edges[:4]
                    )
                    if edges
                    else "nenhuma aresta interna persistida"
                )
                + ".",
                "",
            ]
        )

    lines.extend(
        [
            "## Limitações",
            "",
            "Os rótulos são interpretações da rede DBpedia, não identidades ontológicas observadas. A cobertura do atributo `field` é desigual e muito baixa em várias comunidades; por isso, enriquecimentos com suporte pequeno são descritivos, não testes confirmatórios. Arestas de orientação expressam genealogia acadêmica, que não implica adesão doutrinária. A propagação transitiva com p=1 é uma hipótese determinística do modelo, não evidência de influência histórica efetivamente transmitida por todo o caminho.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Rede analisada: {graph.number_of_nodes():,} vértices e {graph.number_of_edges():,} arestas")
    print(f"Vértices com field: {total_annotated_nodes:,}")
    print(f"Escolas candidatas: {len(candidate_rows)}")
    for path in [
        DISTINCTIVE_FIELDS_PATH,
        RELATION_SUMMARY_PATH,
        REPRESENTATIVES_PATH,
        EDGE_EVIDENCE_PATH,
        CHARACTERIZATION_PATH,
        REPORT_PATH,
    ]:
        print(f"Salvo: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
