"""
Tests for directed graph structure.
"""

import networkx as nx
import staticgraph as sg
from numpy.testing import assert_equal

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test functions.
    """

    if "digraph" in metafunc.funcargnames:
        digraphs = []

        # 100 vertex random graph
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        deg = sg.digraph.make_deg(a.order(), a.edges_iter())
        b = sg.digraph.make(a.order(), a.size(), a.edges_iter(), deg)
        digraphs.append((a, b))
        
        # 100 vertex random graph with parallel edges
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        deg = sg.digraph.make_deg(a.order(), a.edges() + a.edges())
        b = sg.digraph.make(a.order(),  2 * a.size(), a.edges() + a.edges(), deg)
        digraphs.append((a, b))
        
        # 100 vertex random graph with overestimated edge count
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        deg = sg.digraph.make_deg(a.order(), a.edges_iter())
        b = sg.digraph.make(a.order(), 2 * a.size(), a.edges_iter(), deg)
        digraphs.append((a, b))

        metafunc.parametrize("digraph", digraphs)

def test_nodes(digraph):
    """
    Test the nodes of the graph.
    """

    a = sorted(digraph[0].nodes_iter())
    b = sorted(digraph[1].nodes())
    assert a == b

def test_edges(digraph):
    """
    Test the edges of the graph.
    """

    a = sorted(digraph[0].edges_iter())
    b = sorted(digraph[1].edges())
    assert a == b

def test_successors(digraph):
    """
    Test the successors for every node.
    """

    for u in digraph[0].nodes_iter():
        a = sorted(digraph[0].successors_iter(u))
        b = sorted(digraph[1].successors(u))
        assert (u, a) == (u, b)

def test_predecessors(digraph):
    """
    Test the predecessors for every node.
    """

    for u in digraph[0].nodes_iter():
        a = sorted(digraph[0].predecessors_iter(u))
        b = sorted(digraph[1].predecessors(u))
        assert (u, a) == (u, b)

def test_basics(digraph):
    """
    Test basic graph statistics.
    """

    assert digraph[0].order() == digraph[1].order()
    assert digraph[0].size() == digraph[1].size()

    for u in digraph[0].nodes_iter():
        assert digraph[0].in_degree(u) == digraph[1].in_degree(u)
        assert digraph[0].out_degree(u) == digraph[1].out_degree(u)

def test_load_save(tmpdir, digraph):
    """
    Test if persistance is working correctly.
    """

    a = digraph[1]
    
    sg.digraph.save(tmpdir.strpath, a)
    b = sg.digraph.load(tmpdir.strpath)

    assert a.n_nodes == b.n_nodes
    assert a.n_edges == b.n_edges
    assert_equal(a.p_indptr, b.p_indptr)
    assert_equal(a.s_indptr, b.s_indptr)
    assert_equal(a.p_indices, b.p_indices)
    assert_equal(a.s_indices, b.s_indices)

