"""
Tests for implementation of Dijkstra's algorithm for graphs
"""

import networkx as nx
import staticgraph as sg
import pytest
from random import randint, uniform

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

    # 100 vertex random graph
        a = nx.gnp_random_graph(100, 0.1)
        for u, v in a.edges_iter():    
            a.add_weighted_edges_from([(u, v, uniform(0,100))])
        edge_list = []
        for u, v, w in a.edges_iter(data = True):
            edge_list.append((u, v, w['weight']))
        e = iter(edge_list)
        deg = sg.wgraph.make_deg(a.order(), e)
        e = iter(edge_list)
        b = sg.wgraph.make(a.order(), a.size(), e, deg)
        testgraphs.append((a, b))

        metafunc.parametrize("testgraph", testgraphs)

def test_dijkstra(testgraph):
    """
    Testing dijkstra_all function for graphs.
    """

    a, b = testgraph
    s = randint(0, 100)
    nx_dijk =  nx.dijkstra_predecessor_and_distance(a, s)
    nx_dijk = nx_dijk[1]
    sg_dijk = sg.dijkstra.dijkstra_all(b, s)
    for i in range(len(sg_dijk[0])):
        assert sg_dijk[1][i] == nx_dijk[sg_dijk[0][i]]
