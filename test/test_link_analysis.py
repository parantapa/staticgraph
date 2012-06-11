"""
Tests for link analysis functions
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

from staticgraph import make_digraph, hits

import numpy as np
from numpy.testing import assert_almost_equal

def test_5_path_graph():
    """
    Test 5 vertex path graph
    """

    arcs = [(0, 1), (1, 2), (2, 3), (3, 4)]
    known_auth = np.array([0.0, 0.25, 0.25, 0.25, 0.25])
    known_hub  = np.array([0.25, 0.25, 0.25, 0.25, 0.0])

    G = make_digraph(5, len(arcs), arcs)
    hub, auth = hits(G)

    assert_almost_equal(known_auth, auth)
    assert_almost_equal(known_hub, hub)

def test_5_complete_graph():
    """
    Test 5 vertex complete graph
    """

    arcs = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (1, 4),
            (2, 0), (2, 1), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4),
            (4, 0), (4, 1), (4, 2), (4, 3)]

    known_auth = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    known_hub  = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    G = make_digraph(5, len(arcs), arcs)
    hub, auth = hits(G)
    
    assert_almost_equal(known_auth, auth)
    assert_almost_equal(known_hub, hub)
