"""
Components of a graph
"""

import numpy as np

from staticgraph.types import NTYPE

def strong(G):
    """
    Returns a array mapping each node to a component
    """

    preorder     = np.zeros(G.order(), dtype = NTYPE)
    lowlink      = np.zeros(G.order(), dtype = NTYPE)
    comp_num     = np.zeros(G.order(), dtype = NTYPE)
    comp_num_max = 1

    q   = np.empty(G.order(), dtype = NTYPE)
    q_t = 0
    s   = np.empty(G.order(), dtype = NTYPE)
    s_t = 0

    index = 0

    for u in G.nodes():
        if comp_num[u] == 0:
            s[s_t] = u
            s_t += 1

            while s_t != 0:
                v = s[s_t - 1]
                if preorder[v] == 0:
                    index += 1
                    preorder[v] = index

                done = True
                for w in G.successors(v):
                    if preorder[w] == 0:
                        s[s_t] = w
                        s_t += 1
                        done = False
                        break

                if done:
                    lowlink[v] = preorder[v]
                    for w in G.successors(v):
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

