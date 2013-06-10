"""
Tests for Operators of undirected graph structure
"""

import networkx as nx
import staticgraph as sg
from numpy.testing import assert_equal

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

        # 100 vertex random graph
        a = nx.gnp_random_graph(100, 0.1)
        b = a = nx.gnp_random_graph(150, 0.1)
        c = sg.graph.make(a.order(), a.size(), a.edges_iter())
        d = sg.graph.make(b.order(), b.size(), b.edges_iter())
        testgraphs.append((a, b, c, d))

        metafunc.parametrize("testgraph", testgraphs)

def Assert(a, b):
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
    b = sg.graph.complement(testgraph[2])
    c = nx.complement(testgraph[1])
    d = sg.graph.complement(testgraph[3])
    Assert(a, b)
    Assert(c, d)

def test_compose(testgraph):
    """
    Test the Compose of the two graphs are same
    """

    a = nx.compose(testgraph[0], testgraph[1])
    b = sg.graph.compose(testgraph[2], testgraph[3])
    Assert(a, b)

def test_union(testgraph):
    """
    Test the Unions of the two graphs are same
    """

    a = nx.union(testgraph[0], testgraph[1])
    b = sg.graph.union(testgraph[2], testgraph[3])
    Assert(a, b)

def test_disjoint_union(testgraph):
    """
    Test the Disjoint Unions of the two graphs are same
    """

    a = nx.disjoint_union(testgraph[0], testgraph[1])
    b = sg.graph.disjoint_union(testgraph[2], testgraph[3])
    Assert(a, b)

def test_intersection(testgraph):
    """
    Test the Intersection of the two graphs are same
    """

    a = nx.intersection(testgraph[0], testgraph[1])
    b = sg.graph.intersection(testgraph[2], testgraph[3])
    Assert(a, b)

def test_difference(testgraph):
    """
    Test the Difference of the two graphs are same
    """

    a = nx.difference(testgraph[0], testgraph[1])
    b = sg.graph.difference(testgraph[2], testgraph[3])
    Assert(a, b)

def test_symmetric_defference(testgraph):
    """
    Test the Symmetric Difference of the two graphs are same
    """

    a = nx.symmetric_defference(testgraph[0], testgraph[1])
    b = sg.graph.symmetric_defference(testgraph[2], testgraph[3])
    Assert(a, b)
