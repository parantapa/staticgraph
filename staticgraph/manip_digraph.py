"""
Functions to manipulate DiGraph
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

from itertools import chain

from staticgraph import make_digraph

def merge(G0, G1, simple=False, store=None):
    """
    Make a merged graph form two other digraphs
    """

    assert G0.n_nodes == G1.n_nodes

    n_nodes = G0.n_nodes
    n_arcs  = G0.n_arcs + G1.n_arcs
    iterable = chain(G0.arcs(), G1.arcs())

    return make_digraph(n_nodes, n_arcs, iterable, simple, store)

def subgraph(G, nodes, simple=False, store=None):
    """
    Make a subgraph from the given graph
    """

    nodes = set(nodes)

    n_nodes = G.n_nodes
    n_arcs = sum(G.outdegree(u) for u in nodes)
    iterable = ((u, v) for u in nodes
                       for v in G.successors(u)
                       if v in nodes)

    return make_digraph(n_nodes, n_arcs, iterable, simple, store)

