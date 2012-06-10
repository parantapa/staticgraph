#cython: wraparound=False
#cython: boundscheck=False
"""
Functions to create DiGraphs from existing ones
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import os
from os.path import join, exists, isdir
import cPickle as pk

from staticgraph.digraph import DiGraph
from staticgraph import make_digraph

import numpy as np
NTYPE = np.uint32
ATYPE = np.uint64

cimport cython
cimport numpy as np
from libc.stdint cimport uint32_t, uint64_t
ctypedef uint32_t NTYPE_t
ctypedef uint64_t ATYPE_t

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

            if simple and k != 0 and indicesC[k - 1] == v:
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

    # Make the arrays for final graph
    if store is None:
        make_array = lambda _, y, z: np.empty(shape=y, dtype=z)
    else:
        # The final data is stored using mmap array
        if not exists(store):
            os.mkdir(store, 0755)

        make_array = lambda x, y, z: np.memmap(join(store, x), mode="w+",
                                               shape=y, dtype=z)

    # Create the compact array list
    p_indptr  = make_array("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = make_array("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = make_array("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = make_array("s_indices.dat", n_arcs, NTYPE)

    # Merge individual compact arrays
    merge_es(A.p_indptr, B.p_indptr, p_indptr,
             A.p_indices, B.p_indices, p_indices,
             n_nodes, simple)

    merge_es(A.s_indptr, B.s_indptr, s_indptr,
             A.s_indices, B.s_indices, s_indices,
             n_nodes, simple)

    # Re set the number of arcs
    n_arcs = s_indptr[n_nodes]

    if store is not None:
        # Make sure stuff is saved so others can read
        fname = join(store, "base.pickle")
        with open(fname, "wb") as fobj:
            pk.dump((n_nodes, n_arcs), fobj, -1)

        p_indptr.flush()
        p_indices.flush()
        s_indptr.flush()
        s_indices.flush()

    # Finally create our graph
    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G

def subgraph(G, nodes, simple=False, store=None):
    """
    Make a subgraph from the given graph
    """

    nodes = set(nodes)

    n_nodes = G.n_nodes
    n_arcs = sum(G.outdegree(u) for u in nodes)
    iterable = ((u, v) for u in nodes
                       for v in G.successors(u)
                       if v in nodes)

    return make_digraph(n_nodes, n_arcs, iterable, simple, store)

