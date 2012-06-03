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
STORE_DIR0, STORE_DIR1 = None, None

def setup_module(module):
    """
    Create the graphs
    """

    global G0, G1, H0, ARC_GEN, STORE_DIR0, STORE_DIR1

    n_nodes = 10
    n_arcs  = 100

    ARC_GEN = []
    for _ in xrange(n_arcs):
        u = randint(0, n_nodes -1)
        v = randint(0, n_nodes -1)
        ARC_GEN.append((u, v))

    # Make sure to add some duplicates
    dups = ARC_GEN[::2]
    ARC_GEN.extend(dups)

    STORE_DIR0 = tempfile.mkdtemp()
    G0 = make_digraph(STORE_DIR0, n_nodes, len(ARC_GEN), ARC_GEN)
    H0 = load_digraph(STORE_DIR0)

    STORE_DIR1 = tempfile.mkdtemp()
    G1 = make_digraph(STORE_DIR1, n_nodes, len(ARC_GEN), ARC_GEN, simple=True)

def teardown_module(module):
    """
    Remove the created temporary directory
    """

    os.remove(os.path.join(STORE_DIR0, "base.pickle"))
    os.remove(os.path.join(STORE_DIR0, "p_indptr.dat"))
    os.remove(os.path.join(STORE_DIR0, "p_indices.dat"))
    os.remove(os.path.join(STORE_DIR0, "s_indptr.dat"))
    os.remove(os.path.join(STORE_DIR0, "s_indices.dat"))
    os.rmdir(STORE_DIR0)

    os.remove(os.path.join(STORE_DIR1, "base.pickle"))
    os.remove(os.path.join(STORE_DIR1, "p_indptr.dat"))
    os.remove(os.path.join(STORE_DIR1, "p_indices.dat"))
    os.remove(os.path.join(STORE_DIR1, "s_indptr.dat"))
    os.remove(os.path.join(STORE_DIR1, "s_indices.dat"))
    os.rmdir(STORE_DIR1)

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

def test_arcs_forward():
    """
    Test arcs generated using successors
    """

    a = Counter(ARC_GEN)
    b = Counter(G0.arcs())
    c = Counter(H0.arcs())
    assert a == b
    assert b == c

def test_arcs_backward():
    """
    Test arcs generated using predecessors
    """

    a = Counter(ARC_GEN)
    b = Counter(G0.arcs(False))
    c = Counter(H0.arcs(False))
    assert a == b
    assert b == c

def test_no_self_loops():
    """
    Test if the graph has self loops
    """

    for u, v in G1.arcs():
        assert u != v

def test_no_parallel_arcs():
    """
    Test if the graph as parallel arcs
    """

    a = set((u, v) for u, v in ARC_GEN if u != v)
    b = set(G1.arcs())
    assert len(a) == G1.size()
    print a
    print b
    assert a == b

