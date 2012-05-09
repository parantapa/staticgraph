"""
Space efficient Directed Graph implementation
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"
__version__ = "0.1"

import os
import sys
from os.path import join, exists, isdir
from cPickle import load, dump

import numpy as np

# Base data type
DTYPE = np.uint32

class DiGraphBase(object):
    """
    Base class for DiGraph and CDiGraph

    Abstract class; Don't use directly.
    """

    def __init__(self):
        self.n_nodes = None
        self.n_arcs  = None

    def nbytes(self):
        """
        Returns the total bytes used to store internal arrays
        """

        raise NotImplementedError()

    def successors(self, u):
        """
        Yield successors of u
        """

        raise NotImplementedError()

    def predecessors(self, v):
        """
        Yield predecessors of v
        """

        raise NotImplementedError()

    def indegree(self, v):
        """
        Return indegree of node v
        """

        raise NotImplementedError()

    def outdegree(self, u):
        """
        Return outdegree of node u
        """

        raise NotImplementedError()

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

class DiGraph(DiGraphBase):
    """
    DiGraph(n_nodes)
    """

    def __init__(self, n_nodes):
        super(DiGraph, self).__init__()

        self.pred = np.empty(n_nodes, dtype=object)
        self.succ = np.empty(n_nodes, dtype=object)

        for i in xrange(n_nodes):
            self.pred.itemset(i, list())
            self.succ.itemset(i, list())

        self.n_nodes = n_nodes
        self.n_arcs  = 0

    def nbytes(self):
        nbytes  = sum(sys.getsizeof(x) for x in self.pred)
        nbytes += sum(sys.getsizeof(x) for x in self.succ)
        nbytes += self.pred.nbytes
        nbytes += self.pred.nbytes
        return nbytes

    def successors(self, u):
        return self.succ[u]

    def predecessors(self, v):
        return self.pred[v]

    def indegree(self, v):
        return len(self.pred[v])

    def outdegree(self, u):
        return len(self.succ[u])

    def add_arcs_from(self, iterable):
        """
        Pass on a iterable to add arcs to the graph
        """

        for u, v in iterable:
            self.pred[v].append(u)
            self.succ[u].append(v)
            self.n_arcs += 1

class CDiGraph(DiGraphBase):
    """
    CompactDiGraph(store_dir, [G])
    """

    def __init__(self, store_dir, G=None):
        super(CDiGraph, self).__init__()

        self.p_indptr  = None
        self.p_indices = None
        self.s_indptr  = None
        self.s_indices = None

        if G is None:
            assert isdir(store_dir)

            with open(join(store_dir, "base.pickle"), "rb") as fobj:
                self.n_nodes, self.n_arcs = load(fobj)

            self._mmap(store_dir, "r")
        else:
            if not exists(store_dir):
                os.mkdir(store_dir, 0755)

            self.n_nodes  = G.n_nodes
            self.n_arcs   = G.n_arcs

            with open(join(store_dir, "base.pickle"), "wb") as fobj:
                dump((self.n_nodes, self.n_arcs), fobj, -1)

            self._mmap(store_dir, "w+")
            self._copy(G)

    def _mmap(self, store_dir, mode):
        """
        Initialize the memory mapped files
        """

        assert np.iinfo(DTYPE).max > self.n_arcs

        mmap = lambda x, y : np.memmap(join(store_dir, x), mode=mode,
                                    dtype=DTYPE, shape=y)

        self.p_indptr  = mmap("p_indptr.dat", self.n_nodes + 1)
        self.p_indices = mmap("p_indices.dat", self.n_arcs)

        self.s_indptr  = mmap("s_indptr.dat", self.n_nodes + 1)
        self.s_indices = mmap("s_indices.dat", self.n_arcs)

    def _copy(self, G):
        """
        Copy the given graph onto this one
        """

        self.p_indptr[0] = 0
        for i, x in enumerate(G.pred):
            self.p_indptr[i + 1] = self.p_indptr[i] + len(x)
            self.p_indices[self.p_indptr[i]:self.p_indptr[i + 1]] = x

        self.s_indptr[0] = 0
        for i, x in enumerate(G.succ):
            self.s_indptr[i + 1] = self.s_indptr[i] + len(x)
            self.s_indices[self.s_indptr[i]:self.s_indptr[i + 1]] = x

        self.p_indptr.flush()
        self.p_indices.flush()
        self.s_indptr.flush()
        self.p_indices.flush()

    def nbytes(self):
        nbytes  = self.p_indptr.nbytes
        nbytes += self.p_indices.nbytes
        nbytes += self.s_indptr.nbytes
        nbytes += self.s_indices.nbytes
        return nbytes

    def successors(self, u):
        start = self.s_indptr.item(u)
        stop  = self.s_indptr.item(u + 1)
        return self.s_indices[start:stop]

    def predecessors(self, v):
        start = self.p_indptr.item(v)
        stop  = self.p_indptr.item(v + 1)
        return self.p_indices[start:stop]

    def indegree(self, v):
        start = self.p_indptr.item(v)
        stop  = self.p_indptr.item(v + 1)
        return stop - start

    def outdegree(self, u):
        start = self.s_indptr.item(u)
        stop  = self.s_indptr.item(u + 1)
        return stop - start

