"""
Routines for fast edgelist manipulation.
"""

import numpy as np

def make_deg(n_nodes, edges):
    """
    Create the degree distribution of nodes.
    """

    p_deg = np.zeros(n_nodes, dtype="u4")
    s_deg = np.zeros(n_nodes, dtype="u4")
    for u, v in edges:
        if u == v:
            continue
        s_deg[u] += 1
        p_deg[v] += 1
    
    return p_deg, s_deg

def make_comp(n_nodes, n_edges, edges, p_deg, s_deg):
    """
    Create the compressed arrays for edgelist.
    """

    p_indptr = np.empty(n_nodes + 1, dtype="u8")
    p_indices = np.empty(n_edges, dtype="u4")
    s_indptr = np.empty(n_nodes + 1, dtype="u8")
    s_indices = np.empty(n_edges, dtype="u4")
    p_indptr[0]  = s_indptr[0] = 0
    p_indptr[1:] = np.cumsum(p_deg)
    s_indptr[1:] = np.cumsum(s_deg)
    p_idxs = np.array(p_indptr[:-1], dtype="u8")
    s_idxs = np.array(s_indptr[:-1], dtype="u8")
    
    for u, v in edges:
        if u == v:
            continue

        s_indices[s_idxs[u]] = v
        s_idxs[u] += 1
        
        p_indices[p_idxs[v]] = u
        p_idxs[v] += 1

    for u in range(n_nodes):
        start = p_indptr[u]
        stop  = p_indptr[u + 1]
        p_indices[start:stop].sort()
        start = s_indptr[u]
        stop  = s_indptr[u + 1]
        s_indices[start:stop].sort()

    i, j = 0, 1
    for u in range(n_nodes):
        stop  = p_indptr[u + 1]

        while j < stop:
            if p_indices[i] == p_indices[j]:
                j += 1
            else:
                p_indices[i + 1] = p_indices[j]
                i += 1
                j += 1

        p_indptr[u + 1] = i + 1
        i = j
        j += 1
    
    i, j = 0, 1
    for u in range(n_nodes):
        stop  = s_indptr[u + 1]

        while j < stop:
            if s_indices[i] == s_indices[j]:
                j += 1
            else:
                s_indices[i + 1] = s_indices[j]
                i += 1
                j += 1

        s_indptr[u + 1] = i + 1
        i = j
        j += 1

    return p_indptr, p_indices[:np.sum(p_deg)], s_indptr, s_indices[:np.sum(s_deg)]
