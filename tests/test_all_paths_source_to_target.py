from collections import deque
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import all_paths_souce_to_target as standard_module
import all_paths_source_to_target_bfs as bfs_module
import all_paths_source_to_target_dp as dp_module

MODULES = [
    standard_module,
    bfs_module,
    dp_module,
]

IMPLS = [m.all_paths_source_target for m in MODULES]


def _to_tuple_set(paths: List[List[int]]):
    """Convert list of paths to set of tuples for order-agnostic comparison."""
    return set(tuple(p) for p in paths)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    # graph = [[1,2],[3],[3],[]]
    # Paths: [0,1,3], [0,2,3]
    graph = [[1, 2], [3], [3], []]
    result = impl(graph)
    expected = [[0, 1, 3], [0, 2, 3]]
    assert len(result) == 2
    assert _to_tuple_set(result) == _to_tuple_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    # graph = [[4,3,1],[3,2,4],[3],[4],[]]
    graph = [[4, 3, 1], [3, 2, 4], [3], [4], []]
    result = impl(graph)
    expected = [
        [0, 4],
        [0, 3, 4],
        [0, 1, 3, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 4],
    ]
    assert len(result) == 5
    assert _to_tuple_set(result) == _to_tuple_set(expected)


@pytest.mark.parametrize("impl", IMPLS)
def test_minimal_graph_two_nodes(impl):
    # Minimal graph: 2 nodes with an edge 0 -> 1
    graph = [[1], []]
    assert impl(graph) == [[0, 1]]


@pytest.mark.parametrize("impl", IMPLS)
def test_linear_path(impl):
    # 0 -> 1 -> 2 -> 3
    graph = [[1], [2], [3], []]
    assert impl(graph) == [[0, 1, 2, 3]]


@pytest.mark.parametrize("impl", IMPLS)
def test_disconnected_target(impl):
    # Target node n - 1 has no incoming edges from 0
    # 0 -> 1, 2 (target) has no incoming edges
    graph = [[1], [], []]
    assert impl(graph) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_dense_complete_dag(impl):
    # Complete DAG with 5 nodes: each i connects to all j > i
    # Total paths = 2^(5 - 2) = 2^3 = 8
    n = 5
    graph = [[j for j in range(i + 1, n)] for i in range(n)]
    result = impl(graph)
    assert len(result) == 8
    assert len(set(tuple(p) for p in result)) == 8
    for p in result:
        assert p[0] == 0 and p[-1] == n - 1


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_wrapper(module):
    sol = module.Solution()
    graph = [[1], []]
    assert sol.all_paths_source_target(graph) == [[0, 1]]


def _independent_path_oracle(graph: List[List[int]]) -> List[List[int]]:
    """Independent oracle generating all paths using iterative BFS."""
    n = len(graph)
    queue = deque([[0]])
    paths = []
    while queue:
        curr = queue.popleft()
        u = curr[-1]
        if u == n - 1:
            paths.append(curr)
            continue
        for v in graph[u]:
            queue.append(curr + [v])
    return paths


@pytest.mark.parametrize("impl", IMPLS)
@given(
    n=st.integers(min_value=2, max_value=6),
    seed=st.integers(min_value=0, max_value=1000),
)
@settings(max_examples=35)
def test_hypothesis_dag_oracle(impl, n, seed):
    # Generate an arbitrary DAG where edges (u, v) only go forward (u < v)
    import random
    rng = random.Random(seed)
    graph: List[List[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() > 0.4:
                graph[u].append(v)

    result = impl(graph)
    oracle = _independent_path_oracle(graph)

    # 1. Total path count agreement
    assert len(result) == len(oracle)

    # 2. Every path starts at 0 and ends at n - 1
    for p in result:
        assert p[0] == 0
        assert p[-1] == n - 1
        # Validate that each hop is an edge in the graph
        for i in range(len(p) - 1):
            assert p[i + 1] in graph[p[i]]

    # 3. All paths are distinct
    assert len(set(tuple(p) for p in result)) == len(result)

    # 4. Exact set agreement with oracle
    assert _to_tuple_set(result) == _to_tuple_set(oracle)
