"""
Tests for undirected graph structure.
"""

import networkx as nx
import staticgraph as sg
from numpy.testing import assert_equal
from random import triangular
from itertools import chain

def create_iter(edges):
    """
    Returns iterator for edges and their weights (u,v,w) of networkx graphs.
    """

    for i in edges:
        yield i[0], i[1], i[2]['weight']


def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test functions.
    """

    if "graph" in metafunc.funcargnames:
        wgraphs = []

        # 100 vertex random graph
        a = nx.gnp_random_graph(100, 0.1)
        for e in a.edges_iter(data = True):
            e[2]['weight'] = triangular(-2, 2, 0)
        deg = sg.wgraph.make_deg(a.order(), create_iter(a.edges_iter(data = True)))
        b = sg.wgraph.make(a.order(), a.size(), create_iter(a.edges_iter(data = True)), deg)
        wgraphs.append((a, b))
        
        # 100 vertex random graph with parallel edges
        a = nx.gnp_random_graph(100, 0.1)
        for e in a.edges_iter(data = True):
            e[2]['weight'] = triangular(-2, 2, 0)
        deg = sg.wgraph.make_deg(a.order(), chain(create_iter(a.edges_iter(data = True)), create_iter(a.edges_iter(data = True))))
        b = sg.wgraph.make(a.order(), 2 * a.size(), chain(create_iter(a.edges_iter(data = True)), create_iter(a.edges_iter(data = True))), deg)
        wgraphs.append((a, b))
        
        # 100 vertex random graph with overestimated edge count
        a = nx.gnp_random_graph(100, 0.1)
        for e in a.edges_iter(data = True):
            e[2]['weight'] = triangular(-2, 2, 0)
        deg = sg.wgraph.make_deg(a.order(), create_iter(a.edges_iter(data = True)))
        b = sg.wgraph.make(a.order(), 2 * a.size(), create_iter(a.edges_iter(data = True)), deg)
        wgraphs.append((a, b))
        
        metafunc.parametrize("graph", wgraphs)

def test_nodes(graph):
    """
    Test the nodes of the graph.
    """

    a = sorted(graph[0].nodes_iter())
    b = sorted(graph[1].nodes())
    assert a == b

def test_edges(graph):
    """
    Test the edges of the graph.
    """

    a = sorted(graph[0].edges_iter())
    b = sorted(graph[1].edges())
    assert a == b

def test_weights(graph):
    """
    Test the weights of each edge of the graph.
    """

    for u, v, w in graph[0].edges_iter(data = True):
        nx_weight = w['weight']
        sg_weight = graph[1].weight(u, v)
        assert nx_weight == sg_weight

def test_neighbours(graph):
    """
    Test the neighbours for every node.
    """

    for u in graph[0].nodes_iter():
        a = sorted(graph[0].neighbors_iter(u))
        b = sorted(graph[1].neighbours(u))
        assert (u, a) == (u, b)

def test_basics(graph):
    """
    Test graph order, size, and node degrees.
    """

    assert graph[0].order() == graph[1].order()
    assert graph[0].size() == graph[1].size()

    for u in graph[0].nodes_iter():
        assert graph[0].degree(u) == graph[1].degree(u)

def test_load_save(tmpdir, graph):
    """
    Test graph persistance.
    """

    a = graph[1]

    sg.wgraph.save(tmpdir.strpath, a)
    b = sg.wgraph.load(tmpdir.strpath)

    assert a.n_nodes == b.n_nodes
    assert a.n_edges == b.n_edges
    assert_equal(a.n_indptr, b.n_indptr)
    assert_equal(a.n_indices, b.n_indices)
    assert_equal(a.weights, b.weights)
