"""
Undirected Graph Operations
"""

from itertools import chain
from staticgraph.graph import make
from staticgraph.exceptions import StaticGraphNotEqNodesException

def complement(G):
    """
    Returns the complement of Graph G

    Parameters
    ----------
    G : An undirected staticgraph

    Returns
    -------
    H : A new staticgraph graph.

    Notes
    ------

    It is mandatory that G and H be both undirected.
    """

    nset = set(G.nodes())
    n_nodes = G.order()
    n_edges = n_nodes * (n_nodes - 1) / 2 - G.size()
 
    cmp_edges = ((u, v) for u in G.nodes()
		        for v in nset - set(G.neighbours(u))
		        if u < v)
    H = make(n_nodes, n_edges, cmp_edges)
    return H

def union(G, H):
    """
    Return a new graph which is the simple union 
    of the node sets and edge sets.

    Parameters
    ----------
    G,H : Two undirected simple staticgraph

    Returns
    -------
    GC: A new graph  with the same type as G

    Notes
    -----
    It is mandatory that G and H be both undirected.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two undirected graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg)

    edges = ((u, v) for u in G.nodes()
		    for v in chain(G.neighbours(u), H.neighbours(u))
                    if u < v)
                    
    GC = make(G.order(), G.size() + H.size(), edges)
    return GC

def intersection(G, H):
    """
    Return a new graph that contains only the edges that exist in
    both G and H.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : Two undirected simple staticgraphs

    Returns
    -------
    GH : A new graph with the same type as G.

    Notes
    -----
    It is mandatory that G and H be both undirected.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two undirected graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg) 
   
    edges = ((u, v) for u in G.nodes()
                    for v in set(G.neighbours(u)) & set(H.neighbours(u))
                    if u < v)
        
    GH = make(G.order(), G.size(), edges)
    return GH

def difference(G, H):
    """
    Return a new graph that contains the edges that exist in G but not in H.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : Two undirected simple staticgraphs

    Returns
    -------
    D : A new graph with the same type as G.

    Notes
    -----
    It is mandatory that G and H be both undirected.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two undirected graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg)
    
    edges = ((u, v) for u in G.nodes()
                    for v in set(G.neighbours(u)) - set(H.neighbours(u))
                    if u < v)
    D = make(G.order(), G.size(), edges)
    return D

def symmetric_difference(G, H):
    """
    Return new graph with edges that exist in either G or H but not both.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : Two undirected simple staticgraphs

    Returns
    -------
    D : A new graph with the same type as G.

    Notes
    -----
    It is mandatory that G and H be both undirected.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two undirected graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg)

    diff1 = ((u, v) for u in G.nodes()
                    for v in set(G.neighbours(u)) - set(H.neighbours(u))
                    if u < v)

    diff2 = ((u, v) for u in H.nodes()
                    for v in set(H.neighbours(u)) - set(G.neighbours(u))
                    if u < v)

    edges = chain(diff1, diff2)
    D = make(G.order(), G.size() + H.size(), edges)
    return D
