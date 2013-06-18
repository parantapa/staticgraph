"""
Directed Graph Operations
"""

from itertools import chain
from staticgraph.digraph import make, make_deg
from staticgraph.exceptions import StaticGraphNotEqNodesException

def complement(G):
    """
    Returns the complement of Graph G

    Parameters
    ----------
    G : A directed staticgraph

    Returns
    -------
    H : A new staticgraph graph.

    Notes
    ------

    It is mandatory that G be directed.
    """

    nset = set(G.nodes())
    n_nodes = G.order()
    n_edges = n_nodes * (n_nodes - 1) - G.size() + 1
 
    cmp_edges = ((u, v) for u in G.nodes()
		        for v in nset - set(G.successors(u)))
    deg = make_deg(n_nodes, cmp_edges)
    cmp_edges = ((u, v) for u in G.nodes()
		        for v in nset - set(G.successors(u)))
    H = make(n_nodes, n_edges, cmp_edges, deg)
    return H

def union(G, H):
    """
    Return a new graph which is the simple union 
    of the node sets and edge sets.

    Parameters
    ----------
    G,H : Two directed simple staticgraph

    Returns
    -------
    GC: A new graph  with the same type as G

    Notes
    -----
    It is mandatory that G and H be both directed.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two directed graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg)

    n_nodes = G.order()
    edges = ((u, v) for u in G.nodes()
		    for v in chain(G.successors(u), H.successors(u)))
    deg = make_deg(n_nodes, edges)                
    edges = ((u, v) for u in G.nodes()
		    for v in chain(G.successors(u), H.successors(u)))
    GC = make(n_nodes, G.size() + H.size(), edges, deg)
    return GC

def intersection(G, H):
    """
    Return a new graph that contains only the edges that exist in
    both G and H.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : Two directed simple staticgraphs

    Returns
    -------
    GH : A new graph with the same type as G.

    Notes
    -----
    It is mandatory that G and H be both directed.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two directed graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg) 
   
    n_nodes = G.order()
    edges = ((u, v) for u in G.nodes()
                    for v in set(G.successors(u)) & set(H.successors(u)))
    deg = make_deg(n_nodes, edges)    
    edges = ((u, v) for u in G.nodes()
                    for v in set(G.successors(u)) & set(H.successors(u)))
    GH = make(n_nodes, G.size(), edges, deg)
    return GH

def difference(G, H):
    """
    Return a new graph that contains the edges that exist in G but not in H.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : Two directed simple staticgraphs

    Returns
    -------
    D : A new graph with the same type as G.

    Notes
    -----
    It is mandatory that G and H be both directed.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two directed graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg)
    
    n_nodes = G.order()
    edges = ((u, v) for u in G.nodes()
                    for v in set(G.successors(u)) - set(H.successors(u)))
    deg = make_deg(n_nodes, edges)
    edges = ((u, v) for u in G.nodes()
                    for v in set(G.successors(u)) - set(H.successors(u)))
    D = make(n_nodes, G.size(), edges, deg)
    return D

def symmetric_difference(G, H):
    """
    Return new graph with edges that exist in either G or H but not both.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : Two directed simple staticgraphs

    Returns
    -------
    D : A new graph with the same type as G.

    Notes
    -----
    It is mandatory that G and H be both directed.
    The node sets of G and H must be same.
    """

    if G.order() != H.order():
        msg = "Node sets of the two directed graphs are not equal!"
        raise StaticGraphNotEqNodesException(msg)

    n_nodes = G.order()
    diff1 = ((u, v) for u in G.nodes()
                    for v in set(G.successors(u)) - set(H.successors(u)))

    diff2 = ((u, v) for u in H.nodes()
                    for v in set(H.successors(u)) - set(G.successors(u)))
    
    edges = chain(diff1, diff2)
    deg = make_deg(n_nodes, edges)
    
    diff1 = ((u, v) for u in G.nodes()
                    for v in set(G.successors(u)) - set(H.successors(u)))

    diff2 = ((u, v) for u in H.nodes()
                    for v in set(H.successors(u)) - set(G.successors(u)))
    
    edges = chain(diff1, diff2)
    D = make(n_nodes, G.size() + H.size(), edges, deg)
    return D
