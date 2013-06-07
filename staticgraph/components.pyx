#cython: wraparound=False
#cython: boundscheck=False
"""
Finding components in directed graphs.
"""

import numpy as np
from numpy cimport uint64_t, uint32_t, ndarray

def weak(object G):
    """
    Compute weak components in the graph.

    Returns a array mapping each node to a weakly connected component.
    Component numbers start from 1.
    The algorithm uses DFS to find components.

    G - the directed graph.
    """

    cdef:
        ndarray[uint64_t] p_indptr, s_indptr
        ndarray[uint32_t] p_indices, s_indices, comp_num, s
        uint32_t u, v, w
        size_t i, start, end, n_nodes, comp_num_max, s_t

    # Assign to typed variables for fast acces
    p_indptr  = G.p_indptr
    p_indices = G.p_indices
    s_indptr  = G.s_indptr
    s_indices = G.s_indices
    n_nodes   = G.n_nodes

    # Set the component number of all nodes to zero
    # FIXME: find better names for the next 2 variables
    comp_num     = np.zeros(G.order(), dtype="u4")
    comp_num_max = 1

    # Create the dfs stack
    s   = np.empty(G.order(), dtype="u4")
    s_t = 0

    # For every node check if it already belongs to a component
    # If not start a dfs from that node
    for u in range(n_nodes):
        if comp_num[u] == 0:
            s[s_t] = u
            s_t += 1
            comp_num[u] = comp_num_max

            # While stack is not empty
            while s_t != 0:
                v = s[s_t - 1]
                s_t -= 1

                # Check all susccessors
                start = s_indptr[v]
                end   = s_indptr[v + 1]
                for i in range(start, end):
                    w = s_indices[i]
                    if comp_num[w] == 0:
                        s[s_t] = w
                        s_t += 1
                        comp_num[w] = comp_num_max

                # Check all predecessors
                start = p_indptr[v]
                end   = p_indptr[v + 1]
                for i in range(start, end):
                    w = p_indices[i]
                    if comp_num[w] == 0:
                        s[s_t] = w
                        s_t += 1
                        comp_num[w] = comp_num_max

            # Out of the while loop
            comp_num_max += 1

    return comp_num

def strong(object G):
    """
    Compute strong components for the graph.

    Returns a array mapping each node to a strongly connected component.
    Component numbers start from 1.

    G - the directed graph.
    """

    cdef:
        ndarray[uint64_t] s_indptr
        ndarray[uint32_t] s_indices, preorder, lowlink, comp_num, q, s
        uint32_t u, v, w, k
        size_t i, start, end, n_nodes, comp_num_max, q_t, s_t, index

    # Assign to typed variables for fast acces
    s_indptr  = G.s_indptr
    s_indices = G.s_indices
    n_nodes   = G.n_nodes

    # Setup the data structures
    preorder     = np.zeros(G.order(), dtype="u4")
    lowlink      = np.zeros(G.order(), dtype="u4")
    comp_num     = np.zeros(G.order(), dtype="u4")
    comp_num_max = 1

    # Setup the stacks
    q   = np.empty(G.order(), dtype="u4")
    q_t = 0
    s   = np.empty(G.order(), dtype="u4")
    s_t = 0

    # Start index
    index = 0

    for u in range(n_nodes):
        if comp_num[u] == 0:
            s[s_t] = u
            s_t += 1

            while s_t != 0:
                v = s[s_t - 1]
                if preorder[v] == 0:
                    index += 1
                    preorder[v] = index

                done = True
                start = s_indptr[v]
                end   = s_indptr[v + 1]
                for i in range(start, end):
                    w = s_indices[i]
                    if preorder[w] == 0:
                        s[s_t] = w
                        s_t += 1
                        done = False
                        break

                if done:
                    lowlink[v] = preorder[v]
                    start = s_indptr[v]
                    end   = s_indptr[v + 1]
                    for i in range(start, end):
                        w = s_indices[i]
                        if comp_num[w] == 0:
                            if preorder[w] > preorder[v]:
                                lowlink[v] = min(lowlink[v], lowlink[w])
                            else:
                                lowlink[v] = min(lowlink[v], preorder[w])
                    s_t -= 1

                    if lowlink[v] == preorder[v]:
                        comp_num[v] = comp_num_max
                        while q_t != 0 and preorder[q[q_t - 1]] > preorder[v]:
                            k = q[q_t - 1]
                            q_t -= 1
                            comp_num[k] = comp_num_max
                        comp_num_max += 1
                    else:
                        q[q_t] = v
                        q_t += 1

    return comp_num

