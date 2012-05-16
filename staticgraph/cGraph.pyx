"""
Fast implementation of make for using static typing
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

from staticgraph.graph import Graph

def make(object store_dir, size_t n_nodes, size_t n_edges, object iterable):
    """
    Make a Graph
    """

    cdef:
        size_t invalid
        size_t i, j, u, v, tmp
        np.ndarray[DTYPE_t, ndim=1] head
        np.ndarray[DTYPE_t, ndim=1] nxt
        np.ndarray[DTYPE_t, ndim=1] data
        np.ndarray[DTYPE_t, ndim=1] indptr
        np.ndarray[DTYPE_t, ndim=1] indices

    assert np.iinfo(DTYPE).max > n_nodes
    assert np.iinfo(DTYPE).max > 2 * n_edges
    invalid = np.iinfo(DTYPE).max

    # Load all the stuff into our own lists
    head = np.empty(n_nodes, dtype=DTYPE)
    nxt  = np.empty(2 * n_edges, dtype=DTYPE)
    data = np.empty(2 * n_edges, dtype=DTYPE)

    head.fill(invalid)

    i = 0
    for u, v in islice(iterable, n_edges):
        tmp = head[u]
        data[i] = v
        nxt[i] = tmp
        head[u] = i
        i += 1

        tmp = head[v]
        data[i] = u
        nxt[i] = tmp
        head[v] = i
        i += 1
    n_edges = i / 2

    # The final data is stored using mmap array
    if not exists(store_dir):
        os.mkdir(store_dir, 0755)

    mmap = lambda x, y : np.memmap(join(store_dir, x), mode="w+",
                                   dtype=DTYPE, shape=y)

    indptr  = mmap("indptr.dat", n_nodes + 1)
    indices = mmap("indices.dat", 2 * n_edges)

    with cython.boundscheck(False):
        # Copy stuff into the mmapped arrays
        indptr[0] = 0
        i = 0
        for v in xrange(n_nodes):
            j = head[v]
            while j != invalid:
                indices[i] = data[j]
                j = nxt[j]
                i += 1
            indptr[v + 1] = i

    # Make sure stuff is saved so others can read
    with open(join(store_dir, "base.pickle"), "wb") as fobj:
        pk.dump((n_nodes, n_edges, DTYPE), fobj, -1)

    indptr.flush()
    indices.flush()

    # Finally create our graph
    G = Graph(indptr, indices, n_nodes, n_edges)
    return G

