"""
Space efficient Directed Graph implementation
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

from os.path import join, isdir
import cPickle as pk

import numpy as np
NTYPE = np.uint32
ATYPE = np.uint64

class DiGraph(object):
    """
    DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    """

    def __init__(self, p_indptr, p_indices,
                       s_indptr, s_indices,
                       n_nodes, n_arcs):
        self.p_indptr  = p_indptr
        self.p_indices = p_indices
        self.s_indptr  = s_indptr
        self.s_indices = s_indices
        self.n_nodes   = n_nodes
        self.n_arcs    = n_arcs

    def nbytes(self):
        """
        Returns the total bytes used to store internal arrays
        """

        nbytes  = self.p_indptr.nbytes
        nbytes += self.p_indices.nbytes
        nbytes += self.s_indptr.nbytes
        nbytes += self.s_indices.nbytes
        return nbytes

    def successors(self, u):
        """
        Yield successors of u
        """

        start = self.s_indptr.item(u)
        stop  = self.s_indptr.item(u + 1)
        return self.s_indices[start:stop]

    def predecessors(self, v):
        """
        Yield predecessors of v
        """

        start = self.p_indptr.item(v)
        stop  = self.p_indptr.item(v + 1)
        return self.p_indices[start:stop]

    def indegree(self, v):
        """
        Return indegree of node v
        """

        start = self.p_indptr.item(v)
        stop  = self.p_indptr.item(v + 1)
        return stop - start

    def outdegree(self, u):
        """
        Return outdegree of node u
        """

        start = self.s_indptr.item(u)
        stop  = self.s_indptr.item(u + 1)
        return stop - start

    def order(self):
        """
        Return the number of nodes in the graph
        """

        return self.n_nodes

    def size(self):
        """
        Return the number of edges in the graph
        """

        return self.n_arcs

    def nodes(self):
        """
        Return a iterable that generates the nodes of the graph
        """

        return xrange(self.n_nodes)

    def arcs(self, fwd=True):
        """
        Return a iterable that yields the arcs of the graph
        """

        if fwd:
            return ((u, int(v)) for u in self.nodes()
                           for v in self.successors(u))
        else:
            return ((int(u), v) for v in self.nodes()
                           for u in self.predecessors(v))

    def has_node(self, u):
        """
        Check if node u exists
        """

        return (0 <= u < self.n_nodes)

    def has_arc(self, u, v):
        """
        Check if arc (u, v) exists
        """

        return sum(1 for vv in self.successors(u) if v == vv)

def load(store_dir):
    """
    Load a DiGraph
    """

    assert isdir(store_dir)

    with open(join(store_dir, "base.pickle")) as fobj:
        n_nodes, n_arcs = pk.load(fobj)

    mmap = lambda x, y, z : np.memmap(join(store_dir, x), mode="r",
                                      shape=y, dtype=z)

    p_indptr  = mmap("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = mmap("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = mmap("s_indices.dat", n_arcs, NTYPE)

    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G
