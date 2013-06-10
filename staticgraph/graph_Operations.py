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
    G : graph
       A staticgraph graph

    Returns
    -------
    Complement_Graph : A new graph.

    Notes
    ------
    Note that complement() does not create self-loops and also
    does not produce parallel edges for MultiGraphs.

    Graph, node, and edge data are not propagated to the new graph.
    """
 
    n_nodes = G.order()
    edges = sorted([(u, v) for u in range(n_nodes)
            for v in range(u+1, n_nodes) 
            if (u, v) not in G.edges()])
    Complement_Graph = make(n_nodes, len(edges), edges_iter(edges))
    return Complement_Graph
