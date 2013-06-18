"""
Routines for fast edgelist manipulation.
"""

import numpy as np

def make_deg(n_nodes, edges):
    """
    Create the degree distribution of nodes.
    """

    deg = np.zeros(n_nodes, dtype="u4")
    
    for u, v in edges:
        if u == v:
            continue
        deg[u] += 1
        deg[v] += 1
    
    return deg

def make_comp(n_nodes, n_edges, edges, deg):
    """
    Create the compressed arrays for edgelist.
    """

    indptr = np.empty(n_nodes + 1, dtype="u8")
    indices = np.empty(2 * n_edges, dtype="u4")

    indptr[0]  = 0
    indptr[1:] = np.cumsum(deg)
    idxs = np.array(indptr[:-1], dtype="u8")
    
    for u, v in edges:
        if u == v:
            continue

        indices[idxs[u]] = v
        idxs[u] += 1
        
        indices[idxs[v]] = u
        idxs[v] += 1

    for u in range(n_nodes):
        start = indptr[u]
        stop  = indptr[u + 1]
        indices[start:stop].sort()

    i, j = 0, 1
    for u in range(n_nodes):
        stop  = indptr[u + 1]

        while j < stop:
            if indices[i] == indices[j]:
                j += 1
            else:
                indices[i + 1] = indices[j]
                i += 1
                j += 1

        indptr[u + 1] = i + 1
        i = j
        j += 1

    return indptr, indices[:np.sum(deg)]
