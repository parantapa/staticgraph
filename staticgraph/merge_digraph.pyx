#cython: wraparound=False
#cython: boundscheck=False
"""
Merge two digraphs into one
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

from staticgraph.digraph import alloc_digraph, flush_digraph

from staticgraph.types import *
from staticgraph.types cimport *

import numpy as np
cimport numpy as np

# Merge two compressed arrays into one
cdef void merge_es(np.ndarray[ATYPE_t] indptrA,
                   np.ndarray[ATYPE_t] indptrB,
                   np.ndarray[ATYPE_t] indptrC,
                   np.ndarray[NTYPE_t] indicesA,
                   np.ndarray[NTYPE_t] indicesB,
                   np.ndarray[NTYPE_t] indicesC,
                   NTYPE_t n_nodes,
                   bint simple):

    cdef:
        NTYPE_t u, v
        ATYPE_t i, j, k, iend, jend

    k = 0
    indptrC[0] = 0
    for u in range(n_nodes):
        i = indptrA[u]
        j = indptrB[u]
        iend = indptrA[u + 1]
        jend = indptrB[u + 1]

        # While we have nodes in both lsits
        while i < iend and j < jend:
            if indicesA[i] < indicesB[j]:
                v = indicesA[i]
                i += 1
            else:
                v = indicesB[j]
                j += 1

            if simple and v == u:
                continue
            if simple and k != indptrC[u] and indicesC[k - 1] == v:
                continue

            indicesC[k] = v
            k += 1

        # If list B has finished copy everything from A
        while i < iend:
            v = indicesA[i]
            i += 1
            
            if simple and v == u:
                continue
            if simple and k != 0 and indicesC[k - 1] == v:
                continue

            indicesC[k] = v
            k += 1

        # If list A is finished copy everything from B
        while j < jend:
            v = indicesB[j]
            j += 1
            
            if simple and v == u:
                continue
            if simple and k != 0 and indicesC[k - 1] == v:
                continue

            indicesC[k] = v
            k += 1

        # Note end of current list
        indptrC[u + 1] = k

def merge(A, B, simple=False, store=None):
    """
    Make a merged graph form two other digraphs
    """

    assert A.n_nodes == B.n_nodes
    
    n_nodes = A.n_nodes
    n_arcs  = A.n_arcs + B.n_arcs

    # Allocate enough space
    G = alloc_digraph(n_nodes, n_arcs, store)

    # Merge individual compact arrays
    merge_es(A.p_indptr, B.p_indptr, G.p_indptr,
             A.p_indices, B.p_indices, G.p_indices,
             n_nodes, simple)

    merge_es(A.s_indptr, B.s_indptr, G.s_indptr,
             A.s_indices, B.s_indices, G.s_indices,
             n_nodes, simple)

    # Re set the number of arcs
    G.n_arcs = G.s_indptr[G.n_nodes]

    # Sync stuff to disk
    flush_digraph(G, store)

    return G
