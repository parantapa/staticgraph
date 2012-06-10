"""
Tests for directed graph
"""

from __future__ import division

import os
import tempfile
from random import randint
from collections import Counter

from staticgraph import make_digraph, load_digraph

G0, G1, H0 = None, None, None
ARC_GEN = None
STORE_DIR = None

def setup_module(_):
    """
    Create the graphs
    """

    global G0, G1, H0, ARC_GEN, STORE_DIR

    n_nodes = 100
    n_arcs  = 10000

    ARC_GEN = []
    for _ in xrange(n_arcs):
        u = randint(0, n_nodes -1)
        v = randint(0, n_nodes -1)
        ARC_GEN.append((u, v))

    # Make sure to add some duplicates
    dups = ARC_GEN[::2]
    ARC_GEN.extend(dups)

    STORE_DIR = tempfile.mkdtemp()
    G0 = make_digraph(n_nodes, len(ARC_GEN), ARC_GEN, store=STORE_DIR)
    H0 = load_digraph(STORE_DIR)

    G1 = make_digraph(n_nodes, len(ARC_GEN), ARC_GEN, simple=True)

def teardown_module(_):
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
    Test indegree integrity
    """

    for u in G0.nodes():
        a = G0.indegree(u)
        b = H0.indegree(u)
        assert a == b

def test_outdegree():
    """
    Test outdegree integrity
    """

    for u in G0.nodes():
        a = G0.outdegree(u)
        b = H0.outdegree(u)
        assert a == b

def test_successors():
    """
    Test node successors
    """

    for u in G0.nodes():
        a = list(G0.successors(u))
        b = list(H0.successors(u))
        assert a == b

def test_predecessors():
    """
    Test node predecessors
    """

    for u in G0.nodes():
        a = list(G0.predecessors(u))
        b = list(H0.predecessors(u))
        assert a == b

def test_all_arcs():
    """
    Test arcs generated using successors
    """

    a = Counter(ARC_GEN)
    b = Counter(G0.arcs())
    c = Counter(H0.arcs())
    d = Counter(G0.arcs(False))
    e = Counter(H0.arcs(False))
    assert a == b
    assert b == c
    assert c == d
    assert d == e

def test_simple_no_self_loops():
    """
    Test if the graph has self loops
    """

    for u, v in G1.arcs():
        assert u != v

    for u, v in G1.arcs(False):
        assert u != v

def test_simple_no_parallel_arcs():
    """
    Test if the graph has parallel arcs
    """

    a = set(G1.arcs())
    b = list(G1.arcs())
    assert len(a) == len(b)

    a = set(G1.arcs(False))
    b = list(G1.arcs(False))
    assert len(a) == len(b)

def test_simple_all_arcs():
    """
    Test simole graph has all the required arcs
    """

    a = set((u, v) for u, v in ARC_GEN if u != v)
    b = set(G1.arcs())
    c = set(G1.arcs(False))
    assert a == b
    assert a == c

