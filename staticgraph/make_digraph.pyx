#cython: wraparound=False
#cython: boundscheck=False
"""
Fast directed graph creation
"""

from staticgraph.digraph import alloc_digraph, flush_digraph

from staticgraph.types import *
from staticgraph.types cimport *

import numpy as np
cimport numpy as np

# Low level codes represent two 32 bit uints in a 64bit one
cdef ETYPE_t U32MASK = 0xffffffff

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

cdef void swap_es(np.ndarray[ETYPE_t] es, ATYPE_t n_arcs):
    cdef:
        ATYPE_t i
        ETYPE_t e

    for i in range(n_arcs):
        e = es[i]
        es[i] = uv_swap(e)

def make_es(object iterable, NTYPE_t n_nodes, ATYPE_t n_arcs):
    """
    Load edge list to memory
    """

    cdef:
        ATYPE_t i
        ETYPE_t u, v, e
        np.ndarray[ETYPE_t] es

    # Allocate memory
    es = np.empty(n_arcs, dtype=ETYPE)

    # Load all arcs into memory
    i = 0
    for u, v in iterable:
        if i == n_arcs:
            break

        assert u < n_nodes
        assert v < n_nodes

        e = uv_combine(u, v)
        es[i] = e
        i += 1

    # Create a view with smaller number of rows
    es = es[:i]
    n_arcs = i

    return n_arcs, es

def compact_es(np.ndarray[ATYPE_t] indptr,
               np.ndarray[NTYPE_t] indices,
               np.ndarray[ETYPE_t] es,
               NTYPE_t n_nodes,
               ATYPE_t n_arcs,
               bint simple):
    """
    Make compact representation of the edge list
    """

    cdef:
        NTYPE_t u, v, i
        ATYPE_t j, k
        ETYPE_t e

    # Sort the edge list
    es.sort()

    indptr[0] = 0
    i, j, k = 0, 0, 0
    while i < n_nodes:
        while j < n_arcs:
            e = es[j]
            u = u_get(e)
            v = v_get(e)

            # Time for next node
            if u != i:
                break
            # Skip self loops
            if simple and v == i:
                j += 1
                continue
            # Skip parallel edges
            if simple and k != indptr[i] and v == indices[k - 1]:
                j += 1
                continue
            
            # Copy the edge
            indices[k] = v
            k += 1
            j += 1
        
        # Note the end of this node's edge list
        indptr[i + 1] = k
        i += 1

def make(n_nodes, n_arcs, iterable, simple=False, store=None):
    """
    Make a DiGraph

    n_nodes  - The number of nodes in the graph. The value is an upper bound on
               the number of nodes.
    n_arcs   - At most this many arcs will be retrived from the iterable. It is
               acceptable if there are less number of edges in the iterable than
               this value. The final graph may have less number of arcs if
               simple is True.
    iterable - A python iterable generating the arcs.
    simple   - If True, parallel arcs and self loops will be removed.
    store    - If not None then this must be a writable location of a directory.
               If the directory doesn't exist it will be created. The graph data
               structures will be created in this directory as memory mapped
               arrays. This can later be used to load the graph fast.
    """

    assert np.iinfo(NTYPE).max > n_nodes
    assert np.iinfo(ATYPE).max > n_arcs

    # Load the edgelist to memory
    n_arcs, es = make_es(iterable, n_nodes, n_arcs)

    # Allocate the digraph
    G = alloc_digraph(n_nodes, n_arcs, store)

    # Copy stuff into compact arrays
    compact_es(G.s_indptr, G.s_indices, es, n_nodes, n_arcs, simple)

    # Swap u, v for predecessor list
    swap_es(es, n_arcs)
    compact_es(G.p_indptr, G.p_indices, es, n_nodes, n_arcs, simple)

    # Re set the number of arcs
    G.n_arcs = G.s_indptr[G.n_nodes]

    # Flush the graph to disk
    flush_digraph(G, store)

    return G

