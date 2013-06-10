"""
Commonly Used Undirected Graph Operations
"""
from staticgraph.graph import make

def edges_iter(edges):
    """
    Return an iterable of the list edges
    """
    
    for u, v in edges:
        yield u, v

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

    Graph, node, and edge data are not propagated to the new graph.
    """

    nset = set(G.nodes())
    n_nodes = G.order()
    n_edges = n_nodes * (n_nodes - 1) / 2 - G.size()
 
    cmp_edges = ((u, w) for u in G.nodes()
		    for w in nset - set(G.neighbours(u))
		    if w > u)
    H = make(n_nodes, n_edges, cmp_edges)
    return H

def compose(G, H):
    """
    Return a new graph of G composed with H.

    Composition is the simple union of the node sets and edge sets.
    The node sets of G and H need not be disjoint.)

    Parameters
    ----------
    G,H : Two Undirected staticgraphs

    Returns
    -------
    K: A new graph  with the same type as G

    Notes
    -----
    It is mandatory that G and H be both undirected.
    """

    edges = ((u, v) for (u, v) in G.edges()
                    or (u, v) in H.edges())
                    
    n_nodes = G.order()
    if H.order() > G.order():
        n_nodes = H.order()
    GC = make(n_nodes, G.size() + H.size(), edges_iter(edges))
    return GC
