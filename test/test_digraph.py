"""
Tests for fast directed graph
"""

from __future__ import division

import networkx as nx
from numpy.testing import assert_equal

import staticgraph.digraph as dg

def pytest_funcarg__testgraph(request):
    """
    Create the testgraph tuple
    """

    if not hasattr(request.module, "_myargs"):
        a = nx.gnp_random_graph(100, 0.2, directed=True)
        b = dg.make(a.order(), a.edges_iter(), a.size())
        request.module.myargs = (a, b)

    return request.module.myargs

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
    
    dg.save(tmpdir.strpath, a)
    b = dg.load(tmpdir.strpath)

    assert a.n_nodes == b.n_nodes
    assert a.n_edges == b.n_edges
    assert_equal(a.p_indptr, b.p_indptr)
    assert_equal(a.s_indptr, b.s_indptr)
    assert_equal(a.p_indices, b.p_indices)
    assert_equal(a.s_indices, b.s_indices)

