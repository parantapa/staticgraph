#cython: wraparound=False
#cython: boundscheck=False

"""
Routines for fast edgelist manipulation in directed weighted simple graph.
"""

import numpy as np
from numpy cimport uint64_t, uint32_t, float64_t, ndarray

def make_deg(size_t n_nodes, object edges):
    """
    Create the degree distribution of nodes.
    """

    cdef:
        uint32_t u, v
        ndarray[uint32_t] p_deg
        ndarray[uint32_t] s_deg
        size_t i, j
        float64_t w

    p_deg = np.zeros(n_nodes, "u4")
    s_deg = np.zeros(n_nodes, "u4")

    for u, v, w in edges:
        if u == v:
            continue
        i, j = u, v
        s_deg[i] += 1
        p_deg[j] += 1

    return p_deg, s_deg

def make_comp(size_t n_nodes, size_t n_edges, object edges, 
              ndarray[uint32_t] p_deg, ndarray[uint32_t] s_deg):
    """
    Create the compressed arrays for edgelist.
    """

    cdef:
        uint32_t u, v, tmp
        uint64_t start, stop, e
        float64_t w, temp
        size_t i, j, n, del_ctr
        ndarray[uint64_t] p_indptr
        ndarray[uint32_t] p_indices
        ndarray[uint64_t] p_idxs
        ndarray[uint64_t] s_indptr
        ndarray[uint32_t] s_indices
        ndarray[uint64_t] s_idxs
        ndarray[float64_t] p_weights, s_weights

    p_indptr = np.empty(n_nodes + 1, "u8")
    p_indices = np.empty(n_edges, "u4")
    s_indptr = np.empty(n_nodes + 1, "u8")
    s_indices = np.empty(n_edges, "u4")
    p_weights = np.empty(n_edges, "f8")
    s_weights = np.empty(n_edges, "f8")

    p_indptr[0] = s_indptr[0] = 0
    for i in xrange(1, n_nodes + 1):
        p_indptr[i] = p_deg[i - 1] + p_indptr[i - 1]
        s_indptr[i] = s_deg[i - 1] + s_indptr[i - 1]
    p_idxs = np.empty(n_nodes, "u8")
    s_idxs = np.empty(n_nodes, "u8")
    for i in xrange(n_nodes):
        p_idxs[i] = p_indptr[i]
        s_idxs[i] = s_indptr[i]

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

        s_indices[s_idxs[i]] = v
        p_indices[p_idxs[j]] = u
        s_weights[s_idxs[i]] = w
        p_weights[p_idxs[j]] = w
        s_idxs[i] += 1
        p_idxs[j] += 1

        e += 1

    #Sorting the edgelist
    for i in xrange(n_nodes):
        start = p_indptr[i]
        stop  = p_indptr[i + 1]
        sort_indices = p_indices[start:stop].argsort()
        p_indices[start:stop] = p_indices[start:stop][sort_indices]
        p_weights[start:stop] = p_weights[start:stop][sort_indices]

        start = s_indptr[i]
        stop  = s_indptr[i + 1]
        sort_indices = s_indices[start:stop].argsort()
        s_indices[start:stop] = s_indices[start:stop][sort_indices]
        s_weights[start:stop] = s_weights[start:stop][sort_indices]
      
    # Eliminating parallel edges

    i, j, del_ctr = 0, 1, 0
    for n in xrange(n_nodes):
        if(s_indptr[n] == s_indptr[n + 1]):
            continue
        s_indices[i] = s_indices[i + del_ctr]
        s_weights[i] = s_weights[i + del_ctr]
        stop  = s_indptr[n + 1]
        while j < stop:
            if s_indices[i] == s_indices[j]:
                j += 1
                del_ctr += 1
            else:
                s_indices[i + 1] = s_indices[j]
                s_weights[i + 1] = s_weights[j]
                i += 1
                j += 1
                
        s_indptr[n + 1] = i + 1
        i += 1
        j += 1

    s_indices = np.resize(s_indices, s_indptr[n_nodes])
    s_weights = np.resize(s_weights, s_indptr[n_nodes])
    
    i, j, del_ctr = 0, 1, 0
    for n in xrange(n_nodes):
        if(p_indptr[n] == p_indptr[n + 1]):
            continue
        p_indices[i] = p_indices[i + del_ctr]
        p_weights[i] = p_weights[i + del_ctr]
        stop  = p_indptr[n + 1]
        while j < stop:
            if p_indices[i] == p_indices[j]:
                j += 1
                del_ctr += 1
            else:
                p_indices[i + 1] = p_indices[j]
                p_weights[i + 1] = p_weights[j]
                i += 1
                j += 1
                
        p_indptr[n + 1] = i + 1
        i += 1
        j += 1

    p_indices = np.resize(p_indices, p_indptr[n_nodes])
    p_weights = np.resize(p_weights, p_indptr[n_nodes])

    return p_indptr, p_indices, s_indptr, s_indices, p_weights, s_weights
