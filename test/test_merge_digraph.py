"""
Tests for directed graph merging
"""

from __future__ import division

from random import randint
from collections import Counter

from staticgraph import make_digraph, merge_digraph

G0, G1, G2, H2 = None, None, None, None

def setup_module(module):
    """
    Create the graphs
    """

    global G0, G1, G2, H2

    n_nodes = 100
    n_arcs  = 10000

    arcs0, arcs1 = [], []
    for _ in xrange(n_arcs):
        u = randint(0, n_nodes -1)
        v = randint(0, n_nodes -1)
        arcs0.append((u, v))
        
        u = randint(0, n_nodes -1)
        v = randint(0, n_nodes -1)
        arcs1.append((u, v))

    # Make sure to add some duplicates
    dups = arcs0[::2]
    arcs0.extend(dups)
    
    dups = arcs1[::2]
    arcs1.extend(dups)

    G0 = make_digraph(":memory:", n_nodes, len(arcs0), arcs0)
    G1 = make_digraph(":memory:", n_nodes, len(arcs1), arcs1)
    
    G2 = merge_digraph(":memory:", G0, G1)
    H2 = merge_digraph(":memory:", G0, G1, simple=True)

def test_indegree():
    """
    Test indegree integrity
    """

    for u in G0.nodes():
        a = G0.indegree(u) + G1.indegree(u)
        b = G2.indegree(u)
        assert a == b

def test_outdegree():
    """
    Test outdegree integrity
    """

    for u in G0.nodes():
        a = G0.outdegree(u) + G1.outdegree(u)
        b = G2.outdegree(u)
        assert a == b

def test_successors():
    """
    Test node successors
    """

    for u in G0.nodes():
        a = Counter(G0.successors(u))
        a.update(G1.successors(u))
        b = Counter(G2.successors(u))
        assert a == b

def test_predecessors():
    """
    Test node predecessors
    """

    for u in G0.nodes():
        a = Counter(G0.predecessors(u))
        a.update(G1.predecessors(u))
        b = Counter(G2.predecessors(u))
        assert a == b

def test_arcs_forward():
    """
    Test arcs generated using successors
    """

    a = Counter(G0.arcs())
    a.update(G1.arcs())
    b = Counter(G2.arcs())
    assert a == b

def test_arcs_backward():
    """
    Test arcs generated using predecessors
    """

    a = Counter(G0.arcs(False))
    a.update(G1.arcs(False))
    b = Counter(G2.arcs(False))
    assert a == b

def test_simple_indegree():
    """
    Test indegree integrity
    """

    for u in G0.nodes():
        a = G0.indegree(u) + G1.indegree(u)
        b = H2.indegree(u)
        assert a >= b

def test_simple_outdegree():
    """
    Test outdegree integrity
    """

    for u in G0.nodes():
        a = G0.outdegree(u) + G1.outdegree(u)
        b = H2.outdegree(u)
        assert a >= b

def test_simple_successors():
    """
    Test node successors
    """

    for u in G0.nodes():
        a = set(G0.successors(u))
        a.update(G1.successors(u))
        b = set(G2.successors(u))
        assert a == b

def test_simple_predecessors():
    """
    Test node predecessors
    """

    for u in G0.nodes():
        a = set(G0.predecessors(u))
        a.update(G1.predecessors(u))
        b = set(G2.predecessors(u))
        assert a == b

def test_simple_arcs_forward():
    """
    Test arcs generated using successors
    """

    a = set(G0.arcs())
    a.update(G1.arcs())
    b = set(G2.arcs())
    assert a == b

def test_simple_arcs_backward():
    """
    Test arcs generated using predecessors
    """

    a = set(G0.arcs(False))
    a.update(G1.arcs(False))
    b = set(G2.arcs(False))
    assert a == b

