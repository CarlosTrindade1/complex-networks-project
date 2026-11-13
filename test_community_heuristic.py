"""Small, independent checks of diffusion and feasibility invariants."""

import itertools
import unittest

import networkx as nx

from community_heuristic import (
    ExactReach,
    MIAInfluence,
    TopologicalScore,
    cpm_score,
    diverse_elite,
    grasp_construct,
    grasp_refine,
    is_cpm_feasible,
    is_weakly_connected,
)


class CommunityHeuristicTests(unittest.TestCase):
    def test_directed_cpm_and_external_reach(self):
        graph = nx.DiGraph([("a", "b"), ("b", "c")])
        self.assertAlmostEqual(cpm_score(graph, {"a", "b"}, 0.1), 0.8)
        self.assertFalse(is_cpm_feasible(graph, {"a", "c"}, 0.1))
        reach = ExactReach(graph)
        self.assertEqual(reach.total({"a"}), 3)
        self.assertEqual(reach.external({"a"}), 2)
        self.assertEqual(reach.external({"a", "b"}), 1)

    def test_mia_matches_exact_reach_at_probability_one(self):
        graph = nx.DiGraph(
            [("a", "b"), ("b", "a"), ("b", "c"), ("a", "c"), ("d", "b")]
        )
        exact = ExactReach(graph)
        mia = MIAInfluence(graph, theta=1.0)
        for size in range(len(graph) + 1):
            for chosen in itertools.combinations(graph, size):
                seeds = frozenset(chosen)
                self.assertAlmostEqual(mia.total(seeds), exact.total(seeds))
                self.assertAlmostEqual(mia.external(seeds), exact.external(seeds))

    def test_mia_probability_and_threshold(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "b", p=0.5)
        graph.add_edge("b", "c", p=0.5)
        self.assertAlmostEqual(MIAInfluence(graph, theta=0.2).total({"a"}), 1.75)
        self.assertAlmostEqual(MIAInfluence(graph, theta=0.3).total({"a"}), 1.5)

    def test_grasp_constructs_feasible_connected_solution(self):
        graph = nx.DiGraph([("a", "b"), ("a", "e"), ("b", "c"), ("b", "d")])
        score = TopologicalScore(graph)
        solutions = [grasp_construct(graph, score, 0.1, seed) for seed in range(20)]
        solutions = [solution for solution in solutions if solution is not None]
        self.assertTrue(solutions)
        for solution in solutions:
            self.assertGreaterEqual(len(solution.nodes), 2)
            self.assertTrue(is_cpm_feasible(graph, solution.nodes, 0.1))
            self.assertTrue(is_weakly_connected(graph, solution.nodes))
            refined = grasp_refine(graph, score, solution)
            self.assertGreaterEqual(refined.proxy_score, solution.proxy_score)
            self.assertTrue(is_cpm_feasible(graph, refined.nodes, 0.1))
            self.assertTrue(is_weakly_connected(graph, refined.nodes))
        self.assertLessEqual(len(diverse_elite(solutions, limit=2)), 2)


if __name__ == "__main__":
    unittest.main()
