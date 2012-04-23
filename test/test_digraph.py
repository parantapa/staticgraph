"""
Tests for static graph modules
"""

from __future__ import division

import timeit
from random import randint
from collections import Counter

from largegraph import digraph
from largegraph import cDigraph

def test_add_arcs():
    """
    We have at least a 100 time increase in add_arcs speed for cDigraph.
    We have same memory usage for both modules.
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

    x = timeit.timeit(lambda: G1.add_arcs(arc_gen), number = 1)
    y = timeit.timeit(lambda: G2.add_arcs(arc_gen), number = 1)

    assert (x / y) > 100
    assert G1.nbytes() == G2.nbytes()

def test_same_data():
    """
    Both modules produce the same data.
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

    for u in xrange(node_reserve):
        a = list(G1.successors(u))
        b = list(G2.successors(u))

        assert a == b

        a = list(G1.predecessors(u))
        b = list(G2.predecessors(u))

        assert a == b

        a = G1.indegree(u)
        b = G2.indegree(u)

        assert a == b

        a = G1.outdegree(u)
        b = G2.outdegree(u)

        assert a == b

def test_all_arcs():
    """
    Arcs added are arcs present.
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

    x = Counter(arc_gen)
    y = Counter(G1.arcs())
    z = Counter(G2.arcs())

    assert x == y
    assert y == z

