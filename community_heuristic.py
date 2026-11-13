"""Primitives for connected, CPM-constrained spreading communities.

The topological and MIA scores are construction proxies. Final comparisons
must use an independent diffusion evaluator on the original graph.
"""

from __future__ import annotations

import csv
import heapq
import math
import random
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


def load_baseline_graph(root: str | Path = ".") -> nx.DiGraph:
    """Load exactly the directed node set used by the Leiden baseline."""
    root = Path(root)
    graph = nx.read_graphml(root / "dbpedia-network-canonical.graphml")
    with (root / "community_results/final_partitions/leiden_consensus_final.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        nodes = {row["node"] for row in csv.DictReader(handle)}
    if not nodes <= set(graph):
        raise ValueError("The baseline partition contains unknown nodes")
    graph = graph.subgraph(nodes).copy()
    graph.remove_edges_from(nx.selfloop_edges(graph))
    if not graph.is_directed() or len(graph) != 20099 or graph.number_of_edges() != 31545:
        raise ValueError("The graph does not match the frozen baseline")
    return graph


def internal_arc_count(graph: nx.DiGraph, community: frozenset[str] | set[str]) -> int:
    return sum(1 for source in community for target in graph.successors(source) if target in community)


def cpm_score(graph: nx.DiGraph, community: frozenset[str] | set[str], gamma: float) -> float:
    """Directed CPM contribution, with diagonal terms omitted as specified."""
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be in [0, 1]")
    size = len(community)
    return internal_arc_count(graph, community) - gamma * size * (size - 1)


def is_cpm_feasible(graph: nx.DiGraph, community: frozenset[str] | set[str], gamma: float) -> bool:
    return cpm_score(graph, community, gamma) >= -1e-12


def weak_frontier(graph: nx.DiGraph, community: frozenset[str] | set[str]) -> set[str]:
    frontier = set()
    for node in community:
        frontier.update(graph.predecessors(node))
        frontier.update(graph.successors(node))
    return frontier - set(community)


def is_weakly_connected(graph: nx.DiGraph, community: frozenset[str] | set[str]) -> bool:
    return bool(community) and nx.is_weakly_connected(graph.subgraph(community))


class TopologicalScore:
    """One-step external coverage; singleton score equals out-degree."""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def __call__(self, community: frozenset[str] | set[str]) -> float:
        targets = {target for source in community for target in self.graph.successors(source)}
        return float(len(targets - set(community)))


class ExactReach:
    """Deterministic directed reachability using SCC bit masks."""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.positions = {node: position for position, node in enumerate(graph)}
        dag = nx.condensation(graph)
        self.scc_by_node = dag.graph["mapping"]
        masks = {}
        for scc in reversed(list(nx.topological_sort(dag))):
            mask = sum(1 << self.positions[node] for node in dag.nodes[scc]["members"])
            for successor in dag.successors(scc):
                mask |= masks[successor]
            masks[scc] = mask
        self.masks = masks

    def total(self, community: frozenset[str] | set[str]) -> int:
        mask = 0
        for node in community:
            mask |= self.masks[self.scc_by_node[node]]
        return mask.bit_count()

    def external(self, community: frozenset[str] | set[str]) -> int:
        return self.total(community) - len(community)

    def reachable_pair_count(self) -> int:
        """Number of vertex-target memberships, a lower bound for full MIA storage."""
        return sum(self.masks[self.scc_by_node[node]].bit_count() for node in self.graph)


class MIAInfluence:
    """Exact IC expectation on each target's maximum-influence in-arborescence.

    This is an approximation to IC on the original graph when p < 1.
    ``max_entries`` prevents accidental full-graph materialization at p = 1.
    """

    def __init__(
        self,
        graph: nx.DiGraph,
        theta: float = 1.0,
        default_probability: float = 1.0,
        max_entries: int | None = None,
    ):
        if not 0 < theta <= 1 or not 0 <= default_probability <= 1:
            raise ValueError("theta must be in (0, 1] and probability in [0, 1]")
        self.graph = graph
        self.theta = theta
        self.default_probability = default_probability
        self.trees = {}
        entries = 0
        for target in sorted(graph, key=str):
            order, children = self._build_tree(target)
            entries += len(order)
            if max_entries is not None and entries > max_entries:
                raise MemoryError(f"MIA needs more than {max_entries} tree entries")
            self.trees[target] = (order, children)
        self.entry_count = entries

    def _probability(self, source: str, target: str) -> float:
        probability = float(self.graph.edges[source, target].get("p", self.default_probability))
        if not 0 <= probability <= 1:
            raise ValueError(f"Invalid edge probability on {source!r} -> {target!r}")
        return probability

    def _build_tree(self, target: str):
        limit = -math.log(self.theta)
        queue = [(0.0, str(target), target)]
        distance = {target: 0.0}
        parent = {}
        settled = set()
        order = []
        while queue:
            current_distance, _, node = heapq.heappop(queue)
            if node in settled or current_distance > distance[node] + 1e-12:
                continue
            settled.add(node)
            order.append(node)
            for predecessor in sorted(self.graph.predecessors(node), key=str):
                if predecessor in settled:
                    continue
                probability = self._probability(predecessor, node)
                if probability == 0:
                    continue
                candidate = current_distance - math.log(probability)
                if candidate > limit + 1e-12:
                    continue
                if candidate < distance.get(predecessor, math.inf) - 1e-12:
                    distance[predecessor] = candidate
                    parent[predecessor] = node
                    heapq.heappush(queue, (candidate, str(predecessor), predecessor))
        children = {node: [] for node in order}
        for node, successor in parent.items():
            children[successor].append(node)
        return order, children

    def total(self, community: frozenset[str] | set[str]) -> float:
        seeds = set(community)
        total = 0.0
        for target, (order, children) in self.trees.items():
            activation = {}
            for node in reversed(order):
                if node in seeds:
                    activation[node] = 1.0
                else:
                    inactive = 1.0
                    for predecessor in children[node]:
                        inactive *= 1.0 - activation[predecessor] * self._probability(predecessor, node)
                    activation[node] = 1.0 - inactive
            total += activation[target]
        return total

    def external(self, community: frozenset[str] | set[str]) -> float:
        return self.total(community) - len(community)


@dataclass(frozen=True)
class CommunitySolution:
    nodes: frozenset[str]
    proxy_score: float
    gamma: float
    run_seed: int


def _restricted_choice(items: list[tuple[float, str]], rng: random.Random, fraction: float) -> str:
    if not 0 < fraction <= 1:
        raise ValueError("fraction must be in (0, 1]")
    items.sort(key=lambda item: (-item[0], str(item[1])))
    limit = max(1, math.ceil(fraction * len(items)))
    return rng.choice(items[:limit])[1]


def grasp_construct(
    graph: nx.DiGraph,
    score,
    gamma: float,
    run_seed: int,
    restricted_fraction: float = 0.2,
) -> CommunitySolution | None:
    """Construct one feasible solution; return None if the chosen seed cannot grow."""
    rng = random.Random(run_seed)
    seeds = [(score(frozenset((node,))), node) for node in graph]
    if not seeds:
        return None
    community = frozenset((_restricted_choice(seeds, rng, restricted_fraction),))
    current_score = score(community)
    while True:
        candidates = []
        for node in weak_frontier(graph, community):
            expanded = community | {node}
            if not is_cpm_feasible(graph, expanded, gamma):
                continue
            gain = score(expanded) - current_score
            if gain > 1e-12:
                candidates.append((gain, node))
        if not candidates:
            break
        community = community | {_restricted_choice(candidates, rng, restricted_fraction)}
        current_score = score(community)
    if len(community) < 2:
        return None
    return CommunitySolution(community, current_score, gamma, run_seed)


def grasp_refine(graph: nx.DiGraph, score, solution: CommunitySolution) -> CommunitySolution:
    """Best-improvement local search with atomic add, remove, and swap moves."""
    community = solution.nodes
    current_score = solution.proxy_score
    while True:
        best_nodes = None
        best_score = current_score
        candidate_sets = set()
        for node in weak_frontier(graph, community):
            candidate_sets.add(community | {node})
        for removed in community:
            reduced = community - {removed}
            if len(reduced) >= 2:
                candidate_sets.add(reduced)
            for added in weak_frontier(graph, reduced) - set(community):
                candidate_sets.add(reduced | {added})
        for candidate in candidate_sets:
            if not is_cpm_feasible(graph, candidate, solution.gamma):
                continue
            if not is_weakly_connected(graph, candidate):
                continue
            candidate_score = score(candidate)
            if candidate_score > best_score + 1e-12:
                best_nodes = candidate
                best_score = candidate_score
            elif (
                best_nodes is not None
                and abs(candidate_score - best_score) <= 1e-12
                and tuple(sorted(candidate, key=str)) < tuple(sorted(best_nodes, key=str))
            ):
                best_nodes = candidate
        if best_nodes is None:
            break
        community = best_nodes
        current_score = best_score
    return CommunitySolution(community, current_score, solution.gamma, solution.run_seed)


def diverse_elite(solutions: list[CommunitySolution], limit: int = 20, max_jaccard: float = 0.5):
    """Keep high-scoring solutions whose seed sets are sufficiently distinct."""
    if limit < 1 or not 0 <= max_jaccard <= 1:
        raise ValueError("Invalid elite parameters")
    selected = []
    for solution in sorted(
        solutions,
        key=lambda item: (-item.proxy_score, len(item.nodes), tuple(sorted(item.nodes, key=str))),
    ):
        if all(
            len(solution.nodes & other.nodes) / len(solution.nodes | other.nodes) <= max_jaccard
            for other in selected
        ):
            selected.append(solution)
            if len(selected) == limit:
                break
    return selected


def run_grasp(
    graph: nx.DiGraph,
    score,
    gamma: float,
    run_seeds=range(30),
    restricted_fraction: float = 0.2,
    elite_limit: int = 20,
):
    """Run randomized construction and refinement, retaining diverse solutions."""
    all_solutions = []
    for run_seed in run_seeds:
        solution = grasp_construct(graph, score, gamma, run_seed, restricted_fraction)
        if solution is not None:
            all_solutions.append(grasp_refine(graph, score, solution))
    return all_solutions, diverse_elite(all_solutions, limit=elite_limit)
