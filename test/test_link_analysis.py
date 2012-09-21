"""
Tests for link analysis functions
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import staticgraph.digraph as dg
from staticgraph import hits, pagerank

import numpy as np
from numpy.testing import assert_almost_equal

def test_hits_5_path_graph():
    """
    Test 5 vertex path graph
    """

    arcs = [(0, 1), (1, 2), (2, 3), (3, 4)]
    known_auth = np.array([0.0, 0.25, 0.25, 0.25, 0.25])
    known_hub  = np.array([0.25, 0.25, 0.25, 0.25, 0.0])

    G = dg.make(5, arcs, len(arcs))
    hub, auth = hits(G)

    assert_almost_equal(known_auth, auth, decimal=5)
    assert_almost_equal(known_hub, hub, decimal=5)

def test_hits_5_complete_graph():
    """
    Test 5 vertex complete graph
    """

    arcs = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (1, 4),
            (2, 0), (2, 1), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4),
            (4, 0), (4, 1), (4, 2), (4, 3)]

    known_auth = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    known_hub  = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    G = dg.make(5, arcs, len(arcs))
    hub, auth = hits(G)
    
    assert_almost_equal(known_auth, auth, decimal=5)
    assert_almost_equal(known_hub, hub, decimal=5)

def test_hits_5_path_graph_dangle():
    """
    Test 5 vertex path graph
    """

    arcs = [(0, 1), (1, 2), (2, 3), (3, 4)]
    known_hub  = np.array([0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0])
    known_auth = np.array([0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0])

    G = dg.make(8, arcs, len(arcs))
    hub, auth = hits(G)

    assert_almost_equal(known_auth, auth, decimal=5)
    assert_almost_equal(known_hub, hub, decimal=5)

def test_hits_5_complete_graph_dangle():
    """
    Test 5 vertex complete graph
    """

    arcs = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (1, 4),
            (2, 0), (2, 1), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4),
            (4, 0), (4, 1), (4, 2), (4, 3)]

    known_hub  = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0])
    known_auth = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0])

    G = dg.make(8, arcs, len(arcs))
    hub, auth = hits(G)
    
    assert_almost_equal(known_auth, auth, decimal=5)
    assert_almost_equal(known_hub, hub, decimal=5)

def test_pagerank_5_path_graph():
    """
    Test 5 vertex path graph
    """

    arcs = [(0, 1), (1, 2), (2, 3), (3, 4)]
    known_score = np.array([0.08118361587281554,
                            0.15018969032686746,
                            0.208844855233203,
                            0.2587017434248718,
                            0.30108009514224215])

    G = dg.make(5, arcs, len(arcs))
    score = pagerank(G)

    assert_almost_equal(known_score, score, decimal=5)

def test_pagerank_5_complete_graph():
    """
    Test 5 vertex complete graph
    """

    arcs = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (1, 4),
            (2, 0), (2, 1), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4),
            (4, 0), (4, 1), (4, 2), (4, 3)]

    known_score = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    G = dg.make(5, arcs, len(arcs))
    score = pagerank(G)
    
    assert_almost_equal(known_score, score, decimal=5)

def test_pagerank_5_path_graph_dangle():
    """
    Test 5 vertex path graph
    """

    arcs = [(0, 1), (1, 2), (2, 3), (3, 4)]
    known_score = np.array([0.06528371294784407,
                            0.1207748692773813,
                            0.1679423518633439,
                            0.20803471102948676,
                            0.24211321603841182,
                            0.06528371294784407,
                            0.06528371294784407,
                            0.06528371294784407])


    G = dg.make(8, arcs, len(arcs))
    score = pagerank(G)

    assert_almost_equal(known_score, score, decimal=5)

def test_pagerank_5_complete_graph_dangle():
    """
    Test 5 vertex complete graph
    """

    arcs = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (1, 4),
            (2, 0), (2, 1), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4),
            (4, 0), (4, 1), (4, 2), (4, 3)]

    known_score = np.array([0.18348623832041686,
                            0.18348623832041686,
                            0.1834862383204169,
                            0.18348623832041686,
                            0.1834862383204169,
                            0.027522936132638585,
                            0.027522936132638585,
                            0.027522936132638585])

    G = dg.make(8, arcs, len(arcs))
    score = pagerank(G)

    assert_almost_equal(known_score, score, decimal=5)

