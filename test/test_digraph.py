"""
Tests for directed graph structure
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

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
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        b = sg.digraph.make(a.order(), a.size(), a.edges_iter())
        testgraphs.append((a, b))

        # 100 vertex random graph with parallel edges
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        b = sg.digraph.make(a.order(), 2 * a.size(), a.edges() + a.edges())
        testgraphs.append((a, b))

        # 100 vertex random graph with overestimated edge count
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        b = sg.digraph.make(a.order(), 2 * a.size(), a.edges_iter())
        testgraphs.append((a, b))

        metafunc.parametrize("testgraph", testgraphs)

def test_nodes(testgraph):
    """
    Test the nodes of the graph are same
    """

    a = sorted(testgraph[0].nodes_iter())
    b = sorted(testgraph[1].nodes())
    assert a == b

def test_edges(testgraph):
    """
    Test the edges are the same
    """

    a = sorted(testgraph[0].edges_iter())
    b = sorted(testgraph[1].edges())
    assert a == b

def test_successors(testgraph):
    """
    Test the successors for every node
    """

    for u in testgraph[0].nodes_iter():
        a = sorted(testgraph[0].successors_iter(u))
        b = sorted(testgraph[1].successors(u))
        assert (u, a) == (u, b)

def test_predecessors(testgraph):
    """
    Test the successors for every node
    """

    for u in testgraph[0].nodes_iter():
        a = sorted(testgraph[0].predecessors_iter(u))
        b = sorted(testgraph[1].predecessors(u))
        assert (u, a) == (u, b)

def test_basics(testgraph):
    """
    Test some basic stuff
    """

    assert testgraph[0].order() == testgraph[1].order()
    assert testgraph[0].size() == testgraph[1].size()

    for u in testgraph[0].nodes_iter():
        assert testgraph[0].in_degree(u) == testgraph[1].in_degree(u)
        assert testgraph[0].out_degree(u) == testgraph[1].out_degree(u)

def test_load_save(tmpdir, testgraph):
    """
    Test if persistance is working correctly
    """

    a = testgraph[1]
    
    sg.digraph.save(tmpdir.strpath, a)
    b = sg.digraph.load(tmpdir.strpath)

    assert a.n_nodes == b.n_nodes
    assert a.n_edges == b.n_edges
    assert_equal(a.p_indptr, b.p_indptr)
    assert_equal(a.s_indptr, b.s_indptr)
    assert_equal(a.p_indices, b.p_indices)
    assert_equal(a.s_indices, b.s_indices)

