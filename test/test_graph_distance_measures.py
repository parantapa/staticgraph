"""
Tests for different distance measures for graphs.
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
        a = nx.gnp_random_graph(100, 0.5)
        deg = sg.graph.make_deg(a.order(), a.edges_iter())
        b = sg.graph.make(a.order(), a.size(), a.edges_iter(), deg)
        testgraphs.append((a, b))

        metafunc.parametrize("testgraph", testgraphs)

def test_eccentricity(testgraph):
    """
    Testing eccentricity function for graphs.
    """

    a, b = testgraph
    nx_ecc = nx.eccentricity(a)
    sg_ecc = sg.graph_distance_measures.eccentricity(b, b.order())
    for i in range(sg_ecc[0].size):
        assert sg_ecc[1, i] == nx_ecc[sg_ecc[0, i]]

def test_diameter(testgraph):
    """
    Testing diameter function for graphs.
    """

    a, b = testgraph
    nx_dia = nx.diameter(a)
    sg_dia = sg.graph_distance_measures.diameter(b, b.order())
    assert nx_dia == sg_dia

def test_radius(testgraph):
    """
    Testing radius function for graphs.
    """

    a, b = testgraph
    nx_rad = nx.radius(a)
    sg_rad = sg.graph_distance_measures.radius(b, b.order())
    assert nx_rad == sg_rad

def test_periphery(testgraph):
    """
    Testing periphery function for graphs.
    """

    a, b = testgraph
    nx_per = nx.periphery(a)
    sg_per = sg.graph_distance_measures.periphery(b, b.order())
    nx_per = array(nx_per, dtype = uint32)
    nx_per.sort()
    sg_per.sort()
    assert_equal(nx_per, sg_per)

def test_center(testgraph):
    """
    Testing center function for graphs.
    """

    a, b = testgraph
    nx_center = nx.center(a)
    sg_center = sg.graph_distance_measures.center(b, b.order())
    nx_center = array(nx_center, dtype = uint32)
    nx_center.sort()
    sg_center.sort()
    assert_equal(nx_center, sg_center)

