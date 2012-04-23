"""
Tests for static graph modules
"""

from __future__ import division

from random import randint
from collections import Counter

from largegraph import digraph
from largegraph import cDigraph

def make_graphs(tmpdir):
    """
    Create the graphs
    """

    node_reserve = 100
    arc_reserve = 10000

    G1 = digraph.DiGraph(node_reserve, arc_reserve)
    G2 = cDigraph.DiGraph(node_reserve, arc_reserve)

    arc_gen = []
    for _ in xrange(arc_reserve):
        u = randint(0, node_reserve -1)
        v = randint(0, node_reserve -1)
        arc_gen.append((u, v))

    G1.add_arcs(arc_gen)
    G2.add_arcs(arc_gen)

    H1 = digraph.StaticDiGraph(str(tmpdir.join("H1")), G1)
    H2 = cDigraph.StaticDiGraph(str(tmpdir.join("H2")), G2)

    return G1, G2, H1, H2, arc_gen

def test_same_data(tmpdir):
    """
    Both modules produce the same data.
    """

    G1, G2, H1, H2, arc_gen = make_graphs(tmpdir)

    for u in xrange(G1.order()):
        a = G1.indegree(u)
        b = G2.indegree(u)
        c = H1.indegree(u)
        d = H2.indegree(u)
        assert a == c
        assert b == d

        a = G1.outdegree(u)
        b = G2.outdegree(u)
        c = H1.outdegree(u)
        d = H2.outdegree(u)
        assert a == c
        assert b == d

        a = list(G1.successors(u))
        b = list(G2.successors(u))
        c = list(H1.successors(u))
        d = list(H2.successors(u))
        assert a == c
        assert b == d

        a = list(G1.predecessors(u))
        b = list(G2.predecessors(u))
        c = list(H1.predecessors(u))
        d = list(H2.predecessors(u))
        assert a == c
        assert b == d
    
    a = Counter(arc_gen)
    b = Counter(H1.arcs())
    c = Counter(H2.arcs())
    d = Counter(H1.arcs(False))
    e = Counter(H2.arcs(False))
    assert a == b
    assert b == c
    assert c == d
    assert d == e

def test_size(tmpdir):
    """
    Both formats have same size.
    """

    G1, _, H1, H2, _ = make_graphs(tmpdir)

    assert H1.nbytes() == H2.nbytes()
    assert G1.nbytes() > H1.nbytes()

def test_persistance(tmpdir):
    """
    Test data saved is data retrieved.
    """

    G1, G2, _, _, arc_gen = make_graphs(tmpdir)

    H1 = digraph.StaticDiGraph(str(tmpdir.join("H1")))
    H2 = cDigraph.StaticDiGraph(str(tmpdir.join("H2")))

    for u in xrange(G1.order()):
        a = G1.indegree(u)
        b = G2.indegree(u)
        c = H1.indegree(u)
        d = H2.indegree(u)
        assert a == c
        assert b == d

        a = G1.outdegree(u)
        b = G2.outdegree(u)
        c = H1.outdegree(u)
        d = H2.outdegree(u)
        assert a == c
        assert b == d


        a = list(G1.successors(u))
        b = list(G2.successors(u))
        c = list(H1.successors(u))
        d = list(H2.successors(u))
        assert a == c
        assert b == d

        a = list(G1.predecessors(u))
        b = list(G2.predecessors(u))
        c = list(H1.predecessors(u))
        d = list(H2.predecessors(u))
        assert a == c
        assert b == d

    a = Counter(arc_gen)
    b = Counter(H1.arcs())
    c = Counter(H2.arcs())
    d = Counter(H1.arcs(False))
    e = Counter(H2.arcs(False))
    assert a == b
    assert b == c
    assert c == d
    assert d == e

