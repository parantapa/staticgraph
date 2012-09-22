"""
Tests for link analysis functions
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import networkx as nx
import staticgraph as sg

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

        # Complete graph of 100 vertices
        a = nx.complete_graph(100, create_using=nx.DiGraph())
        b = sg.digraph.make(a.order(), a.edges_iter(), a.size())
        testgraphs.append((a, b))

        # Complete graph of 100 vertices with 100 dangling vertices
        a = nx.complete_graph(100, create_using=nx.DiGraph())
        a.add_nodes_from(range(200))
        b = sg.digraph.make(a.order(), a.edges_iter(), a.size())
        testgraphs.append((a, b))

        # Path graph of 100 vertices
        a = nx.path_graph(100, create_using=nx.DiGraph())
        b = sg.digraph.make(a.order(), a.edges_iter(), a.size())
        testgraphs.append((a, b))

        # Path graph of 100 vertices with 100 dangling vertices
        a = nx.path_graph(100, create_using=nx.DiGraph())
        a.add_nodes_from(range(200))
        b = sg.digraph.make(a.order(), a.edges_iter(), a.size())
        testgraphs.append((a, b))

        # Random graph of 100 vertices
        a = nx.gnp_random_graph(100, 0.1, directed=True)
        b = sg.digraph.make(a.order(), a.edges_iter(), a.size())
        testgraphs.append((a, b))

        metafunc.parametrize("testgraph", testgraphs)

def test_hits(testgraph):
    """
    Test hits algorithm
    """

    h0, a0 = nx.hits(testgraph[0], max_iter=100)
    h1, a1 = sg.links.hits(testgraph[1], max_iter=100)

    for u in testgraph[0].nodes_iter():
        assert abs(h0[u] - h1[u]) < 1e-5
        assert abs(a0[u] - a1[u]) < 1e-5

def test_pagerank(testgraph):
    """
    Test pagerank algorithm
    """

    s0 = nx.pagerank(testgraph[0], max_iter=100)
    s1 = sg.links.pagerank(testgraph[1], max_iter=100)

    for u in testgraph[0].nodes_iter():
        assert abs(s0[u] - s1[u]) < 1e-5

