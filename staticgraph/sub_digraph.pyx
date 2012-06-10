# #cython: wraparound=False
# #cython: boundscheck=False
"""
Create a subgraph from an existing graph
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

from staticgraph.digraph import alloc_digraph, flush_digraph

from staticgraph.types import *
from staticgraph.types cimport *

import numpy as np
cimport numpy as np

# Merge two compressed arrays into one
cdef void subset_es(np.ndarray[ATYPE_t] indptrA,
                    np.ndarray[ATYPE_t] indptrB,
                    np.ndarray[NTYPE_t] indicesA,
                    np.ndarray[NTYPE_t] indicesB,
                    np.ndarray[np.int8_t] nset,
                    bint simple):

    cdef:
        NTYPE_t n_nodes, u, v
        ATYPE_t i, iend, j

    n_nodes = indptrA.shape[0] - 1

    j = 0
    indptrB[0] = 0
    for u in range(n_nodes):
        if nset[u]:
            i    = indptrA[u]
            iend = indptrA[u + 1]

            while i < iend:
                v = indicesA[i]
                i += 1

                if simple and v == u:
                    continue
                if simple and j != 0 and indicesB[j - 1] == v:
                    continue
                if not nset[v]:
                    continue

                indicesB[j] = v
                j += 1

        # Note end of current list
        indptrB[u + 1] = j

cdef ATYPE_t arc_max(np.ndarray[ATYPE_t] indptr,
                     np.ndarray[NTYPE_t] nodes):

    cdef:
        ATYPE_t i, n, max_arcs
        NTYPE_t u

    max_arcs = 0
    n = nodes.shape[0]
    for i in range(n):
        u = nodes[i]
        max_arcs += indptr[u + 1] - indptr[u]

    return max_arcs

def sub(A, nodes, simple=False, store=None):
    """
    Create a subgraph of A using the given subset of nodes
    """

    # Create a numpy list and set of nodes
    nodes = np.fromiter(nodes, dtype=NTYPE, count=len(nodes))
    nset  = np.zeros(A.n_nodes, dtype=np.int8)
    nset[nodes] = 1

    n_nodes = A.n_nodes
    n_arcs  = arc_max(A.p_indptr, nodes)

    # Allocate the graph
    G = alloc_digraph(n_nodes, n_arcs, store)

    # Find edge subset
    subset_es(A.p_indptr, G.p_indptr,
              A.p_indices, G.p_indices,
              nset, simple)

    subset_es(A.s_indptr, G.s_indptr,
              A.s_indices, G.s_indices,
              nset, simple)

    # Re set the number of arcs
    G.n_arcs = G.s_indptr[G.n_nodes]

    # Sync stuff to disk
    flush_digraph(G, store)

    return G

