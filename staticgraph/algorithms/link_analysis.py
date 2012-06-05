"""
Link analysis algorithms for graphs
"""

from __future__ import division

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import numpy as np

def hits(G, max_iter=25, max_error=1e-8):
    """
    Find hits hubs and authorities algorithm on the directed graph
    """

    hub   = np.zeros(G.n_nodes, dtype=np.double)
    auth  = np.zeros(G.n_nodes, dtype=np.double)
    hlast = np.zeros(G.n_nodes, dtype=np.double)

    es = [e for e in G.nodes() if G.indegree(e) != 0]
    es = np.array(es, dtype=np.uint32)
    js = [j for j in G.nodes() if G.outdegree(j) != 0]
    js = np.array(js, dtype=np.uint32)

    hub[js] = 1
    for i in xrange(max_iter):
        print "Round ", i

        for v in es:
            auth[v] = np.sum(hub[G.predecessors(v)])

        norm = np.sum(auth[es] ** 2) ** 0.5
        auth[es] /= norm

        for u in js:
            hub[u] = np.sum(auth[G.successors(u)])
        
        norm = np.sum(hub[js] ** 2) ** 0.5
        hub[js] /= norm

        err = np.sum(np.abs(hlast[js] - hub[js]))
        if err < max_error:
            break
        hlast[js] = hub[js]

    return hub, auth

