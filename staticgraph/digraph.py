"""
Space efficient Directed Graph implementation
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"
__version__ = "0.1"

import os
from os.path import join, exists, isdir
import cPickle as pk
from itertools import islice

import numpy as np

class DiGraph(object):
    """
    DiGraph(store_dir)
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

def make(store_dir, n_nodes, n_arcs, iterable, dtype=np.uint32):
    """
    Make a DiGraph
    """

    assert np.iinfo(dtype).max > n_nodes
    assert np.iinfo(dtype).max > n_arcs
    invalid = np.iinfo(dtype).max

    # Load all the stuff into our own lists
    p_head = np.empty(n_nodes, dtype=dtype)
    p_next = np.empty(n_arcs, dtype=dtype)
    p_data = np.empty(n_arcs, dtype=dtype)
    s_head = np.empty(n_nodes, dtype=dtype)
    s_next = np.empty(n_arcs, dtype=dtype)
    s_data = np.empty(n_arcs, dtype=dtype)

    p_head.fill(invalid)
    s_head.fill(invalid)

    iterable = iter(iterable)
    for i in xrange(n_arcs):
        u, v = next(iterable)

        head = p_head[v]
        p_data[i] = u
        p_next[i] = head
        p_head[v] = i

        head = s_head[u]
        s_data[i] = v
        s_next[i] = head
        s_head[u] = i

    # The final data is stored using mmap array
    if not exists(store_dir):
        os.mkdir(store_dir, 0755)

    mmap = lambda x, y : np.memmap(join(store_dir, x), mode="w+",
                                   dtype=dtype, shape=y)

    p_indptr  = mmap("p_indptr.dat", n_nodes + 1)
    p_indices = mmap("p_indices.dat", n_arcs)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1)
    s_indices = mmap("s_indices.dat", n_arcs)

    # Copy stuff into the mmapped arrays
    p_indptr[0] = 0
    i = 0
    for v in xrange(n_nodes):
        j = p_head[v]
        while j != invalid:
            p_indices[i] = p_data[j]
            j = p_next[j]
            i += 1
        p_indptr[v + 1] = i

    s_indptr[0] = 0
    i = 0
    for u in xrange(n_nodes):
        j = s_head[u]
        while j != invalid:
            s_indices[i] = s_data[j]
            j = s_next[j]
            i += 1
        s_indptr[u + 1] = i

    # Make sure stuff is saved so others can read
    with open(join(store_dir, "base.pickle"), "wb") as fobj:
        pk.dump((n_nodes, n_arcs, dtype), fobj, -1)

    p_indptr.flush()
    p_indices.flush()
    s_indptr.flush()
    s_indices.flush()

    # Finally create our graph
    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G

def load(store_dir):
    """
    Load a DiGraph
    """

    assert isdir(store_dir)

    with open(join(store_dir, "base.pickle")) as fobj:
        n_nodes, n_arcs, dtype = pk.load(fobj)

    mmap = lambda x, y : np.memmap(join(store_dir, x), mode="r",
                                   dtype=dtype, shape=y)

    p_indptr  = mmap("p_indptr.dat", n_nodes + 1)
    p_indices = mmap("p_indices.dat", n_arcs)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1)
    s_indices = mmap("s_indices.dat", n_arcs)

    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G

