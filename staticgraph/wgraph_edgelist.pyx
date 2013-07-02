#cython: wraparound=False
#cython: boundscheck=False

"""
Routines for fast edgelist manipulation in undirected weighted simple graph.
"""

import numpy as np
from numpy cimport uint64_t, uint32_t, float64_t, ndarray

def make_deg(size_t n_nodes, object edges):
    """
    Create the degree distribution of nodes.
    """

    cdef:
        uint32_t u, v
        ndarray[uint32_t] deg

    deg = np.zeros(n_nodes, "u4")

    for u, v, w in edges:
        if u == v:
            continue
        i, j = u, v
        deg[i] += 1
        deg[j] += 1
    
    return deg

def make_comp(size_t n_nodes, size_t n_edges, object edges, ndarray[uint32_t] deg):
    """
    Create the compressed arrays for edgelist.
    """

    cdef:
        uint32_t u, v
        uint64_t start, stop, ptr
        float64_t w
        size_t i, j, n, del_ctr, e
        ndarray[uint64_t] indptr
        ndarray[uint32_t] indices, temp_ind
        ndarray[uint64_t] idxs
        ndarray[float64_t] weights, temp_w
        object sort_indices

    indptr = np.empty(n_nodes + 1, "u8")
    indices = np.empty(2 * n_edges, "u4")
    weights = np.empty(2 * n_edges, "f8")
    temp_ind = np.empty(2 * n_edges, "u4")
    temp_w = np.empty(2 * n_edges, "f8")

    indptr[0] = 0
    for i in xrange(1, n_nodes + 1):
        indptr[i] = deg[i - 1] + indptr[i - 1]
    idxs = np.empty(n_nodes, "u8")
    for i in xrange(n_nodes):
        idxs[i] = indptr[i]

    #Creating the edgelist
    e = 0
    for u, v, w in edges:
        if e == n_edges:
            raise ValueError("More edges found than allocated for")
        if not u < n_nodes:
            raise ValueError("Invalid source node found in edges")
        if not v < n_nodes:
            raise ValueError("Invalid destination node found in edges")

        #self loop check
        if u == v:
            continue
        i, j = u, v

        indices[idxs[i]] = v
        indices[idxs[j]] = u
        weights[idxs[i]] = weights[idxs[j]] = w
        idxs[i] += 1
        idxs[j] += 1

        e += 1

    #Sorting the edgelist
    for i in xrange(n_nodes):
        start = indptr[i]
        stop  = indptr[i + 1]
        sort_indices = indices[start:stop].argsort()
        indices[start:stop] = indices[start:stop][sort_indices]
        weights[start:stop] = weights[start:stop][sort_indices]

        
    # Eliminating parallel edges

    i, j, del_ctr = 0, 1, 0
    ptr = 0
    for n in xrange(n_nodes):
        if(ptr == indptr[n + 1]):
            continue
        indices[i] = indices[i + del_ctr]
        weights[i] = weights[i + del_ctr]
        stop  = indptr[n + 1]
        while j < stop:
            if indices[i] == indices[j]:
                j += 1
                del_ctr += 1
            else:
                indices[i + 1] = indices[j]
                weights[i + 1] = weights[j]
                i += 1
                j += 1
        
        ptr = indptr[n + 1]        
        indptr[n + 1] = i + 1
        i += 1
        j += 1

    indices = np.resize(indices, indptr[n_nodes])
    weights = np.resize(weights, indptr[n_nodes])
    return indptr, indices, weights
