"""
Tests for undirected graph
"""

from __future__ import division

import os
import tempfile
from random import randint
from collections import Counter

from staticgraph import make_graph, load_graph

G, H = None, None
EDGE_GEN = None
STORE_DIR = None

def setup_module(module):
    """
    Create the graphs
    """

    global G, H, EDGE_GEN, STORE_DIR

    n_nodes = 100
    n_edges  = 10000

    EDGE_GEN = []
    for _ in xrange(n_edges):
        u = randint(0, n_nodes -1)
        v = randint(0, n_nodes -1)
        EDGE_GEN.append((u, v))

    STORE_DIR = tempfile.mkdtemp()
    G = make_graph(STORE_DIR, n_nodes, n_edges, EDGE_GEN)
    H = load_graph(STORE_DIR)

def teardown_module(module):
    """
    Remove the created temporary directory
    """

    os.remove(os.path.join(STORE_DIR, "base.pickle"))
    os.remove(os.path.join(STORE_DIR, "indptr.dat"))
    os.remove(os.path.join(STORE_DIR, "indices.dat"))
    os.rmdir(STORE_DIR)

def test_degree():
    """
    Test degree integrity
    """

    for u in G.nodes():
        a = G.degree(u)
        b = H.degree(u)
        assert a == b

def test_neighbors():
    """
    Test node neighbors
    """

    for u in G.nodes():
        a = list(G.neighbors(u))
        b = list(H.neighbors(u))
        assert a == b

def test_edges_bothways():
    """
    Test edges
    """

    a = Counter()
    a.update((a, b) for a, b in EDGE_GEN)
    a.update((b, a) for a, b in EDGE_GEN)

    b = Counter(G.edges())
    c = Counter(H.edges())
    assert a == b
    assert b == c

def test_edges_once():
    """
    Test edges
    """

    a = Counter()
    for u, v in EDGE_GEN:
        if u < v:
            a[u, v] += 1
        elif v < u:
            a[v, u] += 1
        else:
            # self loops are ignored in this case
            pass

    b = Counter(G.edges(False))
    c = Counter(H.edges(False))
    assert a == b
    assert b == c

