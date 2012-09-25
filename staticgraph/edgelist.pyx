#cython: wraparound=False
#cython: boundscheck=False
"""
Fast edgelist manipulation
"""

from staticgraph.types import *
from staticgraph.types cimport *

import numpy as np
cimport numpy as np

cdef NODE2_t MASK32 = (2 ** 32) - 1

cdef inline NODE2_t uv_combine(NODE2_t u, NODE2_t v):
    return (u << 32) | (v & MASK32)

cdef inline NODE2_t u_get(NODE2_t e):
    return (e >> 32)

cdef inline NODE2_t v_get(NODE2_t e):
    return (e & MASK32)

cdef inline NODE2_t uv_swap(NODE2_t e):
    cdef:
        NODE2_t u, v

    v = e & MASK32
    u = e >> 32
    return (v << 32) | (u & MASK32)

def swap(np.ndarray[NODE2_t] es):
    """
    Swap the uv pairs in es
    """

    cdef:
        INDEX_t i, n_edges

    n_edges = len(es)
    for i in range(n_edges):
        es[i] = uv_swap(es[i])

def compact(INDEX_t n_nodes, np.ndarray[NODE2_t] es):
    """
    Compact the edge list
    """

    cdef:
        NODE_t u, v
        NODE2_t e
        INDEX_t i, j, n_edges
        np.ndarray[INDEX_t] indptr
        np.ndarray[NODE_t] indices

    n_edges = len(es)
    indptr  = np.empty(n_nodes + 1, INDEX)
    indices = np.empty(n_edges, NODE)

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

def make(INDEX_t n_nodes, INDEX_t n_edges, object edges):
    """
    Load edge list to memory
    """

    cdef:
        NODE_t u, v
        INDEX_t i, j
        np.ndarray[NODE2_t] es

    # Allocate memory
    es = np.empty(n_edges, dtype=NODE2)

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

    # Check for parallel edges
    es.sort()
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

