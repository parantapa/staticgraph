#cython: wraparound=False
#cython: boundscheck=False
"""
Link analysis algorithms for graphs
"""

from __future__ import division

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

from staticgraph.types import *
from staticgraph.types cimport *

import numpy as np
cimport numpy as np

from libc.math cimport sqrt

def hits(object G, size_t max_iter=20, double tol_err=1e-8):
    """
    Find hits hubs and authorities algorithm on the directed graph
    """

    cdef:
        np.ndarray[double] hub, auth, hlast
        np.ndarray[ATYPE_t] p_indptr, s_indptr
        np.ndarray[NTYPE_t] p_indices, s_indices
        NTYPE_t n_nodes, u, v
        ATYPE_t i, start, end
        double norm, err

    # Create the stores
    hub   = np.ones(G.n_nodes, dtype=np.double)
    auth  = np.ones(G.n_nodes, dtype=np.double)
    hlast = np.ones(G.n_nodes, dtype=np.double)

    # Assign to typed variables for fast acces
    p_indptr  = G.p_indptr
    p_indices = G.p_indices
    s_indptr  = G.s_indptr
    s_indices = G.s_indices
    n_nodes   = G.n_nodes

    for _ in range(max_iter):
        # Calculate auth scores
        norm = 0
        for v in range(n_nodes):
            auth[v] = 0
            start = p_indptr[v]
            end   = p_indptr[v + 1]
            for i in range(start, end):
                u = p_indices[i]
                auth[v] += hub[u]
            norm += auth[v]
        for v in range(n_nodes):
            auth[v] /= norm

        norm = 0
        for u in range(n_nodes):
            hub[u] = 0
            start = s_indptr[u]
            end   = s_indptr[u + 1]
            for i in range(start, end):
                v = s_indices[i]
                hub[u] += auth[v]
            norm += hub[u]
        for u in range(n_nodes):
            hub[u] /= norm

        err = 0
        for u in range(n_nodes):
            err += abs(hub[u] - hlast[u])
        if err < tol_err:
            break
        for u in range(n_nodes):
            hlast[u] = hub[u]

    return hub, auth

