"""
Tests for undirected graph structure
"""

__author__  = "Arpan Das <arpandas91@gmail.com>"

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
        b = sg.graph.make(a.order(), a.size(), a.edges_iter())
        testgraphs.append((a, b))

        # 100 vertex random graph with parallel edges
        a = nx.gnp_random_graph(100, 0.1)
        b = sg.graph.make(a.order(), 2 * a.size(), a.edges() + a.edges())
        testgraphs.append((a, b))

        # 100 vertex random graph with overestimated edge count
        a = nx.gnp_random_graph(100, 0.1)
        b = sg.graph.make(a.order(), 2 * a.size(), a.edges_iter())
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

def test_neighbours(testgraph):
    """
    Test the neighbours for every node
    """

    for u in testgraph[0].nodes_iter():
        a = sorted(testgraph[0].neighbors_iter(u))
        b = sorted(testgraph[1].neighbours(u))
        assert (u, a) == (u, b)


def test_basics(testgraph):
    """
    Test some basic stuff
    """

    assert testgraph[0].order() == testgraph[1].order()
    assert testgraph[0].size() == testgraph[1].size()

    for u in testgraph[0].nodes_iter():
        assert testgraph[0].degree(u) == testgraph[1].degree(u)

def test_load_save(tmpdir, testgraph):
    """
    Test if persistance is working correctly
    """

    a = testgraph[1]
    
    sg.graph.save(tmpdir.strpath, a)
    b = sg.graph.load(tmpdir.strpath)

    assert a.n_nodes == b.n_nodes
    assert a.n_edges == b.n_edges
    assert_equal(a.n_indptr, b.n_indptr)
    assert_equal(a.n_indices, b.n_indices)

