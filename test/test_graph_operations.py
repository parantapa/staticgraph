"""
Tests for Operators of undirected graph structure
"""

import networkx as nx
import staticgraph as sg
from numpy.testing import assert_equal
import pytest

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

        # 100 vertex random graph
        a = nx.gnp_random_graph(100, 0.1)
        b = nx.gnp_random_graph(100, 0.1)
        c = sg.graph.make(a.order(), a.size(), a.edges_iter())
        d = sg.graph.make(b.order(), b.size(), b.edges_iter())
        testgraphs.append((a, b, c, d))

        metafunc.parametrize("testgraph", testgraphs)

    if "mismatch_graph" in metafunc.funcargnames:
        mismatch_graphs = []

        a = nx.gnp_random_graph(100, 0.1)
        b = nx.gnp_random_graph(150, 0.1)
        c = sg.graph.make(a.order(), a.size(), a.edges_iter())
        d = sg.graph.make(b.order(), b.size(), b.edges_iter())
        mismatch_graphs.append((c, d))

        metafunc.parametrize("mismatch_graph", mismatch_graphs)

def test_invalid_ops(mismatch_graph):
    """
    Test failure of graph operations on graphs with different orders
    """

    c, d = mismatch_graph

    with pytest.raises(sg.exceptions.StaticGraphNotEqNodesException):
        sg.graph_operations.union(c, d)

    with pytest.raises(sg.exceptions.StaticGraphNotEqNodesException):
        sg.graph_operations.intersection(c, d)

    with pytest.raises(sg.exceptions.StaticGraphNotEqNodesException):
        sg.graph_operations.difference(c, d)

    with pytest.raises(sg.exceptions.StaticGraphNotEqNodesException):
        sg.graph_operations.symmetric_difference(c, d)

def graph_equals(a, b):
    """
    Asserting the Equality of two Graphs
    """
    
    x = sorted(a.nodes_iter())
    y = sorted(b.nodes())
    assert x == y
    
    x = sorted(a.edges_iter())
    y = sorted(b.edges())
    assert x == y

def test_complement(testgraph):
    """
    Test the Complement of the graph are same
    """

    a = nx.complement(testgraph[0])
    b = sg.graph_operations.complement(testgraph[2])
    c = nx.complement(testgraph[1])
    d = sg.graph_operations.complement(testgraph[3])
    graph_equals(a, b)
    graph_equals(c, d)

def test_union(testgraph):
    """
    Test the Compose of the two graphs are same
    """

    a = nx.compose(testgraph[0], testgraph[1])
    b = sg.graph_operations.union(testgraph[2], testgraph[3])
    graph_equals(a, b)

def test_intersection(testgraph):
    """
    Test the Intersection of the two graphs are same
    """

    a = nx.intersection(testgraph[0], testgraph[1])
    b = sg.graph_operations.intersection(testgraph[2], testgraph[3])
    graph_equals(a, b)

def test_difference(testgraph):
    """
    Test the Difference of the two graphs are same
    """

    a = nx.difference(testgraph[0], testgraph[1])
    b = sg.graph_operations.difference(testgraph[2], testgraph[3])
    graph_equals(a, b)

def test_symmetric_defference(testgraph):
    """
    Test the Symmetric Difference of the two graphs are same
    """

    a = nx.symmetric_difference(testgraph[0], testgraph[1])
    b = sg.graph_operations.symmetric_difference(testgraph[2], testgraph[3])
    graph_equals(a, b)
