"""
Tests for implementation of Dijkstra's algorithm for graphs
"""

import networkx as nx
import staticgraph as sg
from random import randint, uniform

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

    # 100 vertex random undirected graph
        a = nx.gnp_random_graph(100, 0.1)
        for u, v in a.edges_iter():    
            a.add_weighted_edges_from([(u, v, uniform(0, 100))])
        edge_list = []
        for u, v, w in a.edges_iter(data = True):
            edge_list.append((u, v, w['weight']))
        e = iter(edge_list)
        deg = sg.wgraph.make_deg(a.order(), e)
        e = iter(edge_list)
        b = sg.wgraph.make(a.order(), a.size(), e, deg)

    # 100 vertex random directed graph
        c = nx.gnp_random_graph(100, 0.1, directed = True)
        for u, v in c.edges_iter():    
            c.add_weighted_edges_from([(u, v, uniform(0, 100))])
        edge_list = []
        for u, v, w in c.edges_iter(data = True):
            edge_list.append((u, v, w['weight']))
        e = iter(edge_list)
        deg = sg.wdigraph.make_deg(c.order(), e)
        e = iter(edge_list)
        d = sg.wdigraph.make(c.order(), c.size(), e, deg)
        testgraphs.append((a, b, c, d))


        metafunc.parametrize("testgraph", testgraphs)

def test_dijkstra_all_graph(testgraph):
    """
    Testing dijkstra_all function for undirected graphs.
    """

    a, b = testgraph[0:2]
    s = randint(0, 100)
    nx_dijk =  nx.dijkstra_predecessor_and_distance(a, s)
    nx_dijk = nx_dijk[1]
    sg_dijk = sg.dijkstra.dijkstra_all(b, s)
    for i in range(len(nx_dijk)):
        assert sg_dijk[1][i] == nx_dijk[sg_dijk[0][i]]

def test_dijkstra_all_digraph(testgraph):
    """
    Testing dijkstra_all function for directed graphs.
    """

    a, b = testgraph[2:]
    s = randint(0, 100)
    nx_dijk =  nx.dijkstra_predecessor_and_distance(a, s)
    nx_dijk = nx_dijk[1]
    sg_dijk = sg.dijkstra.dijkstra_all(b, s, directed = True)
    for i in range(len(nx_dijk)):
        assert sg_dijk[1][i] == nx_dijk[sg_dijk[0][i]]

def test_dijkstra_search_graph(testgraph):
    """
    Testing dijkstra_search function for undirected graphs.
    """

    a, b = testgraph[0:2]
    s = randint(0, 100)
    t = randint(0, 100)
    nx_dijk =  nx.dijkstra_path_length(a, s, t)
    sg_dijk = sg.dijkstra.dijkstra_search(b, s, t)
    assert nx_dijk == sg_dijk[1]

def test_dijkstra_search_digraph(testgraph):
    """
    Testing dijkstra_search function for undirected graphs.
    """

    a, b = testgraph[2:]
    s = randint(0, 100)
    t = randint(0, 100)
    nx_dijk =  nx.dijkstra_path_length(a, s, t)
    sg_dijk = sg.dijkstra.dijkstra_search(b, s, t, directed = True)
    assert nx_dijk == sg_dijk[1]

