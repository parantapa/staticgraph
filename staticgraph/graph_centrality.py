"""
module to implement different centrality measures for undirected graphs.
"""

import staticgraph as sg
from numpy import empty

def degree_centrality(G):
    """
    Compute the degree centrality for nodes.

    The degree centrality for a node v is the fraction of nodes it
    is connected to.

    Parameters
    ----------
    G : An undirected staticgraph 

    Returns
    -------
    degree_centrality : numpy array having degree centrality of the nodes.

    See Also
    --------
    betweenness_centrality, load_centrality, eigenvector_centrality

    Notes
    -----
    The degree centrality values are normalized by dividing by the maximum 
    possible degree in a simple graph n-1 where n is the number of nodes in G.
    """

    degree_centrality = empty(G.order(), dtype = ufloat64)
    d = G.order() - 1
    for u in G.nodes():
        degree_centrality[u] = G.degree(u) / d
    return degree_centrality
