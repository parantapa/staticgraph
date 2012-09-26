#cython: wraparound=False
#cython: boundscheck=False
"""
Fast edgelist manipulation
"""

import numpy as np
from numpy cimport uint64_t, uint32_t, ndarray

cdef uint64_t MASK32 = (2 ** 32) - 1

cdef inline uint64_t uv_combine(uint64_t u, uint64_t v):
    return (u << 32) | (v & MASK32)

cdef inline uint64_t u_get(uint64_t e):
    return (e >> 32)

cdef inline uint64_t v_get(uint64_t e):
    return (e & MASK32)

cdef inline uint64_t uv_swap(uint64_t e):
    cdef:
        uint64_t u, v

    v = e & MASK32
    u = e >> 32
    return (v << 32) | (u & MASK32)

def swap(ndarray[uint64_t] es):
    """
    Swap the uv pairs in es
    """

    cdef:
        size_t i, n_edges

    n_edges = len(es)
    for i in range(n_edges):
        es[i] = uv_swap(es[i])

def compact(size_t n_nodes, ndarray[uint64_t] es):
    """
    Compact the edge list
    """

    cdef:
        uint32_t u, v
        uint64_t e
        size_t i, j, n_edges
        ndarray[uint64_t] indptr
        ndarray[uint32_t] indices

    n_edges = len(es)
    indptr  = np.empty(n_nodes + 1, "u8")
    indices = np.empty(n_edges, "u4")

    indptr[0] = 0
    i, j = 0, 0
    while i < n_nodes:
        while j < n_edges:
            e = es[j]
            u = u_get(e)
            v = v_get(e)

            # Time for next node
            if u != i:
                break

            # Copy the edge
            indices[j] = v
            j += 1

        # Note the end of this node's edge list
        indptr[i + 1] = j
        i += 1

    return indptr, indices

def make(size_t n_nodes, size_t n_edges, object edges):
    """
    Load edge list to memory
    """

    cdef:
        uint32_t u, v
        size_t i, j
        ndarray[uint64_t] es

    # Allocate memory
    es = np.empty(n_edges, dtype="u8")

    # Load all arcs into memory
    i = 0
    for u, v in edges:
        if i == n_edges:
            raise ValueError("More edges found than allocated for")
        if not u < n_nodes:
            raise ValueError("Invalid source node found in edges")
        if not v < n_nodes:
            raise ValueError("Invalid destination node found in edges")

        # Self loop check
        if u == v:
            continue

        es[i] = uv_combine(u, v)
        i += 1
    n_edges = i

    # Release extra space and sort
    es.resize(n_edges, refcheck=False)
    es.sort()

    # Check for parallel edges
    i, j = 1, 0
    while i < n_edges:
        if es[i] == es[j]:
            i += 1
        else:
            es[j + 1] = es[i]
            i += 1
            j += 1
    n_edges = j + 1

    # Release extra space
    es.resize(n_edges, refcheck=False)

    return es

