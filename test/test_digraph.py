"""
Tests for static graph modules
"""

from __future__ import division

import timeit
from random import randint
from collections import Counter

from largegraph import digraph
from largegraph import cDigraph

def make_graphs(add_arcs=True):
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

    if add_arcs:
        G1.add_arcs(arc_gen)
        G2.add_arcs(arc_gen)

    return G1, G2, arc_gen

def test_add_arcs():
    """
    We have at least a 100 time increase in add_arcs speed for cDigraph.
    We have same memory usage for both modules.
    """

    G1, G2, arc_gen = make_graphs(False)

    x = timeit.timeit(lambda: G1.add_arcs(arc_gen), number = 1)
    y = timeit.timeit(lambda: G2.add_arcs(arc_gen), number = 1)

    assert (x / y) > 100
    assert G1.nbytes() == G2.nbytes()

def test_same_data():
    """
    Both modules produce the same data.
    """

    G1, G2, arc_gen = make_graphs()

    for u in xrange(G1.order()):
        a = G1.indegree(u)
        b = G2.indegree(u)
        assert a == b

        a = G1.outdegree(u)
        b = G2.outdegree(u)
        assert a == b

        a = list(G1.successors(u))
        b = list(G2.successors(u))
        assert a == b

        a = list(G1.predecessors(u))
        b = list(G2.predecessors(u))
        assert a == b

    a = Counter(arc_gen)
    b = Counter(G1.arcs())
    c = Counter(G2.arcs())
    d = Counter(G1.arcs(False))
    e = Counter(G2.arcs(False))
    assert a == b
    assert b == c
    assert c == d
    assert d == e

