#cython: wraparound=False
#cython: boundscheck=False
"""
Routines for fast edgelist manipulation in undirected unweighted simple graph.
"""

import numpy as np
from numpy cimport uint64_t, uint32_t, ndarray

def make_deg(size_t n_nodes, object edges):
    """
    Create the approximate degree distribution of nodes.

    Duplcate edges are counted here, and discarded later.
    """

    cdef:
        uint32_t u, v
        ndarray[uint32_t] deg

    deg = np.zeros(n_nodes, "u4")

    for u, v in edges:
        if u == v:
            continue

        deg[u] += 1
        deg[v] += 1

    return deg

cdef void remove_dups(size_t n_nodes, ndarray[uint64_t] indptr,
                      ndarray[uint32_t] indices):
    """
    Remove the duplicate edges.
    """

    cdef:
        uint32_t u
        uint64_t stop
        size_t i, j, ndups

    # Delete any duplicate edges
    i, j, ndups = 0, 1, 0
    for u in range(n_nodes):
        # Ignore nodes with no neighbors
        if indptr[u] == indptr[u + 1]:
            continue

        # Copy the first element in place
        indices[i] = indices[i + ndups]

        # For the rest of edges check if next edge is duplicate
        # If so then skip it othewise move it to proper place
        stop  = indptr[u + 1]
        while j < stop:
            if indices[i] == indices[j]:
                j += 1
                ndups += 1
            else:
                indices[i + 1] = indices[j]
                i += 1
                j += 1

        # Since some edges are now gone move the end of the current
        # neighbor set in place
        indptr[u + 1] = i + 1
        i += 1
        j += 1

def make_comp(size_t n_nodes, size_t n_edges, object edges,
              ndarray[uint32_t] deg):
    """
    Create the compressed edgelist for the graph.
    """

    cdef:
        uint32_t u, v
        uint64_t start, stop
        size_t i, j, n
        ndarray[uint64_t] indptr
        ndarray[uint32_t] indices
        ndarray[uint64_t] nextv

    # Create the arrays
    indptr  = np.empty(n_nodes + 1, "u8")
    indices = np.empty(2 * n_edges, "u4")
    nextv   = np.empty(n_nodes, "u8")

    # Make the approximate indptr from the approximate deg dist given
    indptr[0]  = 0
    for i in range(1, n_nodes + 1):
        indptr[i] = deg[i - 1] + indptr[i - 1]

    # Create indexes where neighbors of nodes are to be inserted
    # The next neighbor of node u is inserted at location nextv[u]
    for i in range(n_nodes):
        nextv[i] = indptr[i]

    # Creating the edgelist
    n = 0
    for u, v in edges:
        if n == n_edges:
            raise ValueError("More edges found than allocated for")
        if not u < n_nodes:
            raise ValueError("Invalid source node found in edges")
        if not v < n_nodes:
            raise ValueError("Invalid destination node found in edges")

        # Self loop check
        if u == v:
            continue

        # Where the next nodes are inserted
        i = nextv[u]
        j = nextv[v]

        # Insert the edges
        indices[i] = v
        indices[j] = u

        nextv[u] += 1
        nextv[v] += 1
        n        += 1

    # Sorting the neighbor list of every node individually.
    # This should ideally be faster than sorting all edges together.
    for i in range(n_nodes):
        start = indptr[i]
        stop  = indptr[i + 1]
        if stop - start > 1:
            indices[start:stop].sort()

    # Remove the duplicate edges
    remove_dups(n_nodes, indptr, indices)

    # Resize the indices array in place
    indices.resize(indptr[n_nodes], refcheck=False)

    return indptr, indices
