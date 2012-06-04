"""
Tests for directed graph
"""

from __future__ import division

from random import randint, sample

from staticgraph import make_digraph, sub_digraph

G0, G1, G2 = None, None, None
N1, N2 = None, None

def setup_module(module):
    """
    Create the graphs
    """

    global G0, G1, G2, N1, N2

    n_nodes = 100
    n_arcs  = 10000

    arcs = []
    for _ in xrange(n_arcs):
        u = randint(0, n_nodes -1)
        v = randint(0, n_nodes -1)
        arcs.append((u, v))

    # Make sure to add some duplicates
    dups = arcs[::2]
    arcs.extend(dups)

    G0 = make_digraph(":memory:", n_nodes, len(arcs), arcs)
    N1 = set(sample(xrange(n_nodes), int(n_nodes / 2)))
    G1 = sub_digraph(":memory:", G0, N1)
    N2 = set(sample(xrange(n_nodes), int(n_nodes / 2)))
    G2 = sub_digraph(":memory:", G0, N2, simple=True)

def test_indegree():
    """
    Test indegree integrity
    """

    for u in G0.nodes():
        if u not in N1:
            assert G1.indegree(u) == 0

def test_outdegree():
    """
    Test outdegree integrity
    """

    for u in G0.nodes():
        if u not in N1:
            assert G1.outdegree(u) == 0

def test_successors():
    """
    Test node successors
    """

    for u in G0.nodes():
        if u in N1:
            a = set(G1.successors(u))
            assert a <= N1

def test_predecessors():
    """
    Test node predecessors
    """

    for u in G0.nodes():
        if u in N1:
            a = set(G1.predecessors(u))
            assert a <= N1

def test_arcs_forward():
    """
    Test arcs generated using successors
    """

    for u, v in G1.arcs():
        assert u in N1 and v in N1

def test_arcs_backward():
    """
    Test arcs generated using predecessors
    """

    for u, v in G1.arcs(False):
        assert u in N1 and v in N1

def test_simple_all_arcs():
    """
    Test we are not missing any arcs
    """

    a = set((u, v) for u, v in G0.arcs()
                   if u in N2
                   if v in N2
                   if u != v)
    b = set(G2.arcs())
    c = set(G2.arcs(False))
    assert a == b
    assert a == c

