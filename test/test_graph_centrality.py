"""
Tests for different centrality measures for graphs.
"""

import networkx as nx
import staticgraph as sg
from numpy import array, uint32
from numpy.testing import assert_equal

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs.
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

    # 100 vertex random graph
        a = nx.gnp_random_graph(100, 0.1)
        deg = sg.graph.make_deg(a.order(), a.edges_iter())
        b = sg.graph.make(a.order(), a.size(), a.edges_iter(), deg)
        testgraphs.append((a, b))

        metafunc.parametrize("testgraph", testgraphs)

def test_degree_centrality(testgraph):
    """
    Testing degree centrality function for graphs.
    """

    a, b = testgraph
    nx_deg = nx.degree_centrality(a)
    sg_deg = sg.graph_centrality.degree_centrality(b)
    for i in a.nodes():
        assert "{0:.12f}".format(nx_deg[i]) == "{0:.12f}".format(sg_deg[i])
