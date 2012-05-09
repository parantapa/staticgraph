"""
Tests for static graph modules
"""

from __future__ import division

import os
import tempfile
from random import randint
from collections import Counter

from staticgraph import DiGraph, CDiGraph

G, H, I = None, None, None
ARC_GEN = None
STORE_DIR = None

def setup_module(module):
    """
    Create the graphs
    """

    global G, H, I, ARC_GEN, STORE_DIR

    node_reserve = 100
    arc_reserve = 10000

    G = DiGraph(node_reserve)

    ARC_GEN = []
    for _ in xrange(arc_reserve):
        u = randint(0, node_reserve -1)
        v = randint(0, node_reserve -1)
        ARC_GEN.append((u, v))

    G.add_arcs_from(ARC_GEN)

    STORE_DIR = tempfile.mkdtemp()
    H = CDiGraph(STORE_DIR, G)
    I = CDiGraph(STORE_DIR)

def teardown_module(module):
    """
    Remove the created temporary directory
    """

    os.remove(os.path.join(STORE_DIR, "base.pickle"))
    os.remove(os.path.join(STORE_DIR, "p_indptr.dat"))
    os.remove(os.path.join(STORE_DIR, "p_indices.dat"))
    os.remove(os.path.join(STORE_DIR, "s_indptr.dat"))
    os.remove(os.path.join(STORE_DIR, "s_indices.dat"))
    os.rmdir(STORE_DIR)

def test_indegree():
    """
    Test in degree integrity
    """

    for u in G.nodes():
        a = G.indegree(u)
        b = H.indegree(u)
        c = I.indegree(u)
        assert a == b
        assert b == c

def test_outdegree():
    """
    Test in degree integrity
    """

    for u in G.nodes():
        a = G.outdegree(u)
        b = H.outdegree(u)
        c = I.outdegree(u)
        assert a == b
        assert b == c

def test_successors():
    """
    Test node successors
    """

    for u in G.nodes():
        a = list(G.successors(u))
        b = list(H.successors(u))
        c = list(I.successors(u))
        assert a == b
        assert b == c

def test_predecessors():
    """
    Test node predecessors
    """

    for u in G.nodes():
        a = list(G.predecessors(u))
        b = list(H.predecessors(u))
        c = list(I.predecessors(u))
        assert a == b
        assert b == c

def test_edges_forward():
    """
    Test edges generated using successors
    """

    a = Counter(ARC_GEN)
    b = Counter(G.arcs())
    c = Counter(H.arcs())
    d = Counter(I.arcs())
    assert a == b
    assert b == c
    assert c == d

def test_edges_backward():
    """
    Test edges generated using predecessors
    """

    a = Counter(ARC_GEN)
    b = Counter(G.arcs(False))
    c = Counter(H.arcs(False))
    d = Counter(I.arcs(False))
    assert a == b
    assert b == c
    assert c == d

