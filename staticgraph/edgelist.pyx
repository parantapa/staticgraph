#cython: wraparound=False
#cython: boundscheck=False
"""
Fast edgelist manipulation
"""

from staticgraph.types import *
from staticgraph.types cimport *

import numpy as np
cimport numpy as np

cdef ETYPE_t U32MASK = (2 ** 32) - 1

cdef inline ETYPE_t uv_combine(ETYPE_t u, ETYPE_t v):
    return (u << 32) | (v & U32MASK)

cdef inline ETYPE_t u_get(ETYPE_t e):
    return (e >> 32)

cdef inline ETYPE_t v_get(ETYPE_t e):
    return (e & U32MASK)

cdef inline ETYPE_t uv_swap(ETYPE_t e):
    cdef:
        ETYPE_t u, v

    v = e & U32MASK
    u = e >> 32
    return (v << 32) | (u & U32MASK)

def swap(np.ndarray[ETYPE_t] es):
    """
    Swap the uv pairs in es
    """

    cdef:
        ATYPE_t i, n_edges

    n_edges = len(es)
    for i in range(n_edges):
        es[i] = uv_swap(es[i])

def compact(NTYPE_t n_nodes, np.ndarray[ETYPE_t] es):
    """
    Compact the edge list
    """

    cdef:
        NTYPE_t u, v, i
        ATYPE_t j, n_edges
        ETYPE_t e
        np.ndarray[ATYPE_t] indptr
        np.ndarray[NTYPE_t] indices

    n_edges = len(es)
    indptr  = np.empty(n_nodes + 1, ATYPE)
    indices = np.empty(n_edges, NTYPE)

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

def make(NTYPE_t n_nodes, object edges, ATYPE_t count):
    """
    Load edge list to memory
    """

    cdef:
        NTYPE_t u, v
        ATYPE_t i, j
        np.ndarray[ETYPE_t] es

    # Allocate memory
    es = np.empty(count, dtype=ETYPE)

    # Load all arcs into memory
    i = 0
    for u, v in edges:
        if i == count:
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
    count = i

    # Check for parallel edges
    es.sort()
    i, j = 1, 0
    while i < count:
        if es[i] == es[j]:
            i += 1
        else:
            es[j + 1] = es[i]
            i += 1
            j += 1
    count = j + 1

    # Release extra space
    es.resize(count, refcheck=False)

    return es

