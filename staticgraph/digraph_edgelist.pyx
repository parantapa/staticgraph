#cython: wraparound=False
#cython: boundscheck=False
"""
Routines for fast edgelist manipulation in directed unweighted simple graph.
"""

import numpy as np
from numpy cimport uint64_t, uint32_t, ndarray

def make_deg(size_t n_nodes, object edges):
    """
    Create the degree distribution of nodes.
    """

    cdef:
        uint32_t u, v
        ndarray[uint32_t] p_deg
        ndarray[uint32_t] s_deg
        size_t i, j

    p_deg = np.zeros(n_nodes, "u4")
    s_deg = np.zeros(n_nodes, "u4")

    for u, v in edges:
        if u == v:
            continue
        i, j = u, v
        s_deg[i] += 1
        p_deg[j] += 1
    
    return p_deg, s_deg

def make_comp(size_t n_nodes, size_t n_edges, object edges, ndarray[uint32_t] p_deg, ndarray[uint32_t] s_deg):
    """
    Create the compressed arrays for edgelist.
    """

    cdef:
        uint32_t u, v
        uint64_t start, stop
        size_t i, j, n, del_ctr, e
        ndarray[uint64_t] p_indptr
        ndarray[uint32_t] p_indices
        ndarray[uint64_t] p_idxs
        ndarray[uint64_t] s_indptr
        ndarray[uint32_t] s_indices
        ndarray[uint64_t] s_idxs

    p_indptr = np.empty(n_nodes + 1, "u8")
    p_indices = np.empty(2 * n_edges, "u4")
    s_indptr = np.empty(n_nodes + 1, "u8")
    s_indices = np.empty(2 * n_edges, "u4")

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
    for u, v in edges:
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
        s_idxs[i] += 1
        
        p_indices[p_idxs[j]] = u
        p_idxs[j] += 1

        e += 1
    
    #Sorting the edgelist
    for i in xrange(n_nodes):
        start = p_indptr[i]
        stop  = p_indptr[i + 1]
        p_indices[start:stop].sort()
        start = s_indptr[i]
        stop  = s_indptr[i + 1]
        s_indices[start:stop].sort()

    # Eliminating parallel edges

    i, j, del_ctr = 0, 1, 0  
    for n in xrange(n_nodes):
        if(p_indptr[n] == p_indptr[n + 1]):
            continue
        p_indices[i] = p_indices[i + del_ctr]
        stop  = p_indptr[n + 1]
        while j < stop:
            if p_indices[i] == p_indices[j]:
                j += 1
                del_ctr += 1
            else:
                p_indices[i + 1] = p_indices[j]
                i += 1
                j += 1
                
        p_indptr[n + 1] = i + 1
        i += 1
        j += 1
    p_indices = np.resize(p_indices, e - del_ctr)
    
    i, j, del_ctr = 0, 1, 0  
    for n in xrange(n_nodes):
        if(s_indptr[n] == s_indptr[n + 1]):
            continue
        s_indices[i] = s_indices[i + del_ctr]
        stop  = s_indptr[n + 1]
        while j < stop:
            if s_indices[i] == s_indices[j]:
                j += 1
                del_ctr += 1
            else:
                s_indices[i + 1] = s_indices[j]
                i += 1
                j += 1
                
        s_indptr[n + 1] = i + 1
        i += 1
        j += 1
    s_indices = np.resize(s_indices, e - del_ctr)
    
    return p_indptr, p_indices, s_indptr, s_indices
