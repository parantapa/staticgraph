#cython: wraparound=False
#cython: boundscheck=False
"""
Link analysis algorithms for graphs
"""

from __future__ import division

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import numpy as np
from numpy cimport uint64_t, uint32_t, ndarray

def hits(object G, size_t max_iter=20, double tol_err=1e-8):
    """
    Find hits hubs and authorities algorithm on the directed graph
    """

    cdef:
        ndarray[double] hub, auth, hlast
        ndarray[uint64_t] p_indptr, s_indptr
        ndarray[uint32_t] p_indices, s_indices
        uint32_t u, v
        size_t i, start, end, n_nodes
        double norm, err

    # Assign to typed variables for fast acces
    p_indptr  = G.p_indptr
    p_indices = G.p_indices
    s_indptr  = G.s_indptr
    s_indices = G.s_indices
    n_nodes   = G.n_nodes

    # Create the stores
    hub   = np.ones(n_nodes, dtype="f8")
    auth  = np.ones(n_nodes, dtype="f8")
    hlast = np.ones(n_nodes, dtype="f8")

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

        # Calculate hub scores
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

        # Calculate error for convergence
        err = 0
        for u in range(n_nodes):
            err += abs(hub[u] - hlast[u])
        if err < tol_err:
            break
        for u in range(n_nodes):
            hlast[u] = hub[u]

    return hub, auth

def pagerank(object G, double alpha=0.85, size_t max_iter=20,
             double tol_err=1e-8):
    """
    Run pagerank algorithm on the graph
    """

    cdef:
        ndarray[double] score, xscor
        ndarray[uint64_t] p_indptr, s_indptr
        ndarray[uint32_t] p_indices, s_indices, dangle
        uint32_t u, v
        size_t i, sstart, send, pstart, pend, n_nodes, n_dangle
        double norm, dangle_score, err

    # Assign to typed variables for fast acces
    p_indptr  = G.p_indptr
    p_indices = G.p_indices
    s_indptr  = G.s_indptr
    s_indices = G.s_indices
    n_nodes   = G.n_nodes

    # Create the stores
    score  = np.empty(n_nodes, dtype="f8")
    xscor  = np.empty(n_nodes, dtype="f8")
    dangle = np.empty(n_nodes, dtype="u4")

    # Initialize fist score
    xscor.fill(1.0 / n_nodes)

    # Keep note of nodes with no outdegree
    i = 0
    for u in range(n_nodes):
        sstart = s_indptr[u]
        send   = s_indptr[u + 1]
        if send - sstart == 0:
            dangle[i] = u
            i += 1
    n_dangle = i

    # Run max_iter number of times
    for _ in range(max_iter):

        # Calculate score from dangling nodes per node
        dangle_score = 0
        for i in range(n_dangle):
            u = dangle[i]
            dangle_score += xscor[u]
        dangle_score *= alpha
        dangle_score /= n_nodes

        # Calculate individual scores for each node
        norm = 0
        for v in range(n_nodes):
            score[v] = 0
            pstart = p_indptr[v]
            pend   = p_indptr[v + 1]
            for i in range(pstart, pend):
                u = p_indices[i]
                sstart = s_indptr[u]
                send   = s_indptr[u + 1]
                score[v] += alpha * xscor[u] / (send - sstart)
            score[v] += dangle_score
            score[v] += (1.0 - alpha) / n_nodes
            norm += score[v]
        for v in range(n_nodes):
            score[v] /= norm

        # Calculate error for convergence
        err = 0
        for u in range(n_nodes):
            err += abs(score[u] - xscor[u])
        if err < tol_err:
            break
        for u in range(n_nodes):
            xscor[u] = score[u]

    return score

