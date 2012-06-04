"""
Fast implementation of digraph_make using static typing
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import os
from os.path import join, exists
import cPickle as pk
from itertools import islice

import numpy as np

cimport cython
cimport numpy as np
ctypedef np.uint32_t NTYPE_t
ctypedef np.uint64_t ATYPE_t

from staticgraph.digraph import DiGraph, NTYPE, ATYPE

def _make_el(size_t n_arcs, object iterable):
    """
    Load edge list to memory
    """

    cdef:
        size_t i, u, v
        np.ndarray[NTYPE_t, ndim=2] el

    # Allocate memory
    el = np.empty((n_arcs, 2), dtype=NTYPE)

    # Load all arcs into memory
    i = 0
    for u, v in islice(iterable, n_arcs):
        with cython.boundscheck(False):
            el[i, 0] = u
            el[i, 1] = v
        i += 1

    # Create a view with smaller number of rows
    el = el[:i, :]
    n_arcs = i

    return n_arcs, el

def _make_graph(np.ndarray[ATYPE_t] indptr,
                np.ndarray[NTYPE_t] indices,
                size_t n_nodes,
                size_t n_arcs,
                np.ndarray[NTYPE_t, ndim=2] el,
                bint simple,
                bint fwd):

    """
    Make compact representation of the graph
    """

    cdef:
        size_t u, v
        object dt, b
        size_t i, j, k

    u, v = (0, 1) if fwd else (1, 0)

    # Sort the edge list using a record view
    dt = [(str(u), NTYPE), (str(v), NTYPE)]
    b = el.ravel().view(dt)
    b.sort(order=['0','1'])

    # Copy the stuff into graph struct
    with cython.boundscheck(False):
        indptr[0] = 0
        i, j, k = 0, 0, 0
        while i < n_nodes:
            while j < n_arcs and el[j, u] == i:
                # Skip self loops
                if simple and el[j, v] == i:
                    j += 1
                    continue

                # Skip parallel edges
                if simple and k != 0 and el[j, v] == indices[k - 1]:
                    j += 1
                    continue

                # Copy the edge
                indices[k] = el[j, v]
                k += 1
                j += 1

            indptr[i + 1] = k
            i += 1

def make(store_dir, n_nodes, n_arcs, iterable, simple=False):
    """
    Make a DiGraph
    """

    assert np.iinfo(NTYPE).max > n_nodes
    assert np.iinfo(ATYPE).max > n_arcs

    # Load the edgelist to memory
    n_arcs, el = _make_el(n_arcs, iterable)

    if store_dir == ":memory:":
        mmap = lambda _, y, z : np.empty(shape=y, dtype=z)
    else:
        # The final data is stored using mmap array
        if not exists(store_dir):
            os.mkdir(store_dir, 0755)

        mmap = lambda x, y, z : np.memmap(join(store_dir, x), mode="w+",
                                          shape=y, dtype=z)

    # Create the compact array list
    p_indptr  = mmap("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = mmap("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = mmap("s_indices.dat", n_arcs, NTYPE)

    # Copy stuff into compact arrays
    _make_graph(s_indptr, s_indices, n_nodes, n_arcs, el, simple, True)
    _make_graph(p_indptr, p_indices, n_nodes, n_arcs, el, simple, False)

    # Re set the number of arcs
    n_arcs = s_indptr[n_nodes]

    if store_dir != ":memory:":
        # Make sure stuff is saved so others can read
        with open(join(store_dir, "base.pickle"), "wb") as fobj:
            pk.dump((n_nodes, n_arcs), fobj, -1)

        p_indptr.flush()
        p_indices.flush()
        s_indptr.flush()
        s_indices.flush()

    # Finally create our graph
    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G

