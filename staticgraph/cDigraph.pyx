"""
Fast implementation of make using static typing
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"
__version__ = "0.1"

import os
from os.path import join, exists, isdir
import cPickle as pk
from itertools import islice

import numpy as np
DTYPE   = np.uint32

cimport cython
cimport numpy as np
ctypedef np.uint32_t DTYPE_t

from staticgraph.digraph import DiGraph

def make(object store_dir, size_t n_nodes, size_t n_arcs, object iterable):
    """
    Make a DiGraph
    """

    cdef:
        size_t invalid
        size_t i, j, u, v, tmp
        np.ndarray[DTYPE_t, ndim=1] p_head
        np.ndarray[DTYPE_t, ndim=1] p_next
        np.ndarray[DTYPE_t, ndim=1] p_data
        np.ndarray[DTYPE_t, ndim=1] s_head
        np.ndarray[DTYPE_t, ndim=1] s_next
        np.ndarray[DTYPE_t, ndim=1] s_data
        np.ndarray[DTYPE_t, ndim=1] p_indptr
        np.ndarray[DTYPE_t, ndim=1] p_indices
        np.ndarray[DTYPE_t, ndim=1] s_indptr
        np.ndarray[DTYPE_t, ndim=1] s_indices

    assert np.iinfo(DTYPE).max > n_nodes
    assert np.iinfo(DTYPE).max > n_arcs
    invalid = np.iinfo(DTYPE).max

    # Load all the stuff into our own lists
    p_head = np.empty(n_nodes, dtype=DTYPE)
    p_next = np.empty(n_arcs, dtype=DTYPE)
    p_data = np.empty(n_arcs, dtype=DTYPE)
    s_head = np.empty(n_nodes, dtype=DTYPE)
    s_next = np.empty(n_arcs, dtype=DTYPE)
    s_data = np.empty(n_arcs, dtype=DTYPE)

    p_head.fill(invalid)
    s_head.fill(invalid)

    i = 0
    for u, v in islice(iterable, n_arcs):
        tmp = p_head[v]
        p_data[i] = u
        p_next[i] = tmp
        p_head[v] = i

        tmp = s_head[u]
        s_data[i] = v
        s_next[i] = tmp
        s_head[u] = i

        i += 1
    n_arcs = i

    # The final data is stored using mmap array
    if not exists(store_dir):
        os.mkdir(store_dir, 0755)

    mmap = lambda x, y : np.memmap(join(store_dir, x), mode="w+",
                                   dtype=DTYPE, shape=y)

    p_indptr  = mmap("p_indptr.dat", n_nodes + 1)
    p_indices = mmap("p_indices.dat", n_arcs)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1)
    s_indices = mmap("s_indices.dat", n_arcs)

    with cython.boundscheck(False):
        # Copy stuff into the mmapped arrays
        p_indptr[0] = 0
        i = 0
        for v in xrange(n_nodes):
            j = p_head[v]
            while j != invalid:
                p_indices[i] = p_data[j]
                j = p_next[j]
                i += 1
            p_indptr[v + 1] = i

        s_indptr[0] = 0
        i = 0
        for u in xrange(n_nodes):
            j = s_head[u]
            while j != invalid:
                s_indices[i] = s_data[j]
                j = s_next[j]
                i += 1
            s_indptr[u + 1] = i

    # Make sure stuff is saved so others can read
    with open(join(store_dir, "base.pickle"), "wb") as fobj:
        pk.dump((n_nodes, n_arcs, DTYPE), fobj, -1)

    p_indptr.flush()
    p_indices.flush()
    s_indptr.flush()
    s_indices.flush()

    # Finally create our graph
    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G

