"""
Space efficient Directed Graph implementation
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import os
from os.path import join, exists, isdir
import cPickle as pk
import numpy as np

from staticgraph.types import ATYPE, NTYPE

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
        return (int(v) for v in self.s_indices[start:stop])

    def predecessors(self, v):
        """
        Yield predecessors of v
        """

        start = self.p_indptr.item(v)
        stop  = self.p_indptr.item(v + 1)
        return (int(u) for u in self.p_indices[start:stop])

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
            return ((u, v) for u in self.nodes()
                           for v in self.successors(u))
        else:
            return ((u, v) for v in self.nodes()
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

def alloc_digraph(n_nodes, n_arcs, store):
    """
    Create empty digraph to be filled
    """

    if store is None:
        # Use in memory arrays
        create = lambda _, y, z: np.empty(shape=y, dtype=z)
    else:
        # Use memory mapped arrays
        if not exists(store):
            os.mkdir(store, 0755)

        create = lambda x, y, z: np.memmap(join(store, x), mode="w+",
                                           shape=y, dtype=z)

    # Create the arrays
    p_indptr  = create("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = create("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = create("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = create("s_indices.dat", n_arcs, NTYPE)

    # Finally create the graph
    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G

def flush_digraph(G, store):
    """
    Flush the memory of the digraph if arrays are mmapped
    """

    if store is not None:
        # Make sure stuff is saved so others can read
        fname = join(store, "base.pickle")
        with open(fname, "wb") as fobj:
            pk.dump((G.n_nodes, G.n_arcs), fobj, -1)

        G.p_indptr.flush()
        G.p_indices.flush()
        G.s_indptr.flush()
        G.s_indices.flush()

def load_digraph(store):
    """
    Load a digraph from disk
    """

    # Check if directory is valid
    assert isdir(store)

    # Load basic info
    fname = join(store, "base.pickle")
    with open(fname, "rb") as fobj:
        n_nodes, n_arcs = pk.load(fobj)

    load = lambda x, y, z: np.memmap(join(store, x), mode="r",
                                     shape=y, dtype=z)

    # Make the arrays
    p_indptr  = load("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = load("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = load("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = load("s_indices.dat", n_arcs, NTYPE)

    # Create the graph
    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G
