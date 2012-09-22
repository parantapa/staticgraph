"""
Test the component finding algorithms
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import networkx as nx
import staticgraph as sg
import staticgraph.digraph as dg

def pytest_generate_tests(metafunc):
    """
    Generate the arguments for test funcs
    """

    if "testgraph" in metafunc.funcargnames:
        testgraphs = []

        for _ in xrange(20):
            # Random graph of 100 vertices
            a = nx.gnp_random_graph(100, 0.1, directed=True)
            b = dg.make(a.order(), a.edges_iter(), a.size())
            testgraphs.append((a, b))

        metafunc.parametrize("testgraph", testgraphs)

def assert_components_equal(comps0, comps1):
    """
    Check if the two components are the same
    """

    # We have the same number of components
    assert len(comps0) == max(comps1)

    # For each component in comps0
    for comp in comps0:

        # Find component number of first node
        u = comp[0]
        c = comps1[u]

        # For every other node component number must be same
        for v in comp[1:]:
            assert c == comps1[v]

    # For every component the component number should be different
    d = 0
    for comp in comps0:
        u = comp[0]
        c = comps1[u]

        assert c != d

        d = c

def test_strongly_connected_components(testgraph):
    """
    Test strongly connected components
    """

    comps0 = nx.strongly_connected_components(testgraph[0])
    comps1 = sg.strongly_connected_components(testgraph[1])

    assert_components_equal(comps0, comps1)

def xtest_weakly_connected_components(testgraph):
    """
    Test strongly connected components
    """

    comps0 = nx.weakly_connected_components(testgraph[0])
    comps1 = sg.weakly_connected_components(testgraph[1])

    assert_components_equal(comps0, comps1)

