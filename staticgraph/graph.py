"""
Space efficient Undirected Graph implementation
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"
__version__ = "0.1"

import os
from os.path import join, exists, isdir
import cPickle as pk
from itertools import islice

import numpy as np

class Graph(object):
    """
    Graph(store_dir)
    """

    def __init__(self, indptr, indices,
                       n_nodes, n_edges):
        self.indptr  = indptr
        self.indices = indices
        self.n_nodes = n_nodes
        self.n_edges = n_edges

    def nbytes(self):
        """
        Returns the total bytes used to store internal arrays
        """

        nbytes  = self.indptr.nbytes
        nbytes += self.indices.nbytes
        return nbytes

    def neighbors(self, u):
        """
        Yield neighbors of u
        """

        start = self.indptr.item(u)
        stop  = self.indptr.item(u + 1)
        return self.indices[start:stop]

    def degree(self, u):
        """
        Return degree of node u
        """

        start = self.indptr.item(u)
        stop  = self.indptr.item(u + 1)
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

        return self.n_edges

    def nodes(self):
        """
        Return a iterable that generates the nodes of the graph
        """

        return xrange(self.n_nodes)

    def edges(self, bothways=True):
        """
        Return an iterable that yields the edges of the graph

        If bothways is True return (a, b) along with (b, a).
        NOTE: if bothways is False, self loops are not returned.
        """

        return ((u, v) for u in self.nodes()
                       for v in self.neighbors(u)
                       if bothways or u < v)

    def has_node(self, u):
        """
        Check if node u exists
        """

        return (0 <= u < self.n_nodes)

    def has_edge(self, u, v):
        """
        Check if edge (u, v) exists
        """

        return sum(1 for vv in self.neighbors(u) if v == vv)

def make(store_dir, n_nodes, n_edges, iterable, dtype=np.uint32):
    """
    Make a Graph
    """

    assert np.iinfo(dtype).max > n_nodes
    assert np.iinfo(dtype).max > 2 * n_edges
    invalid = np.iinfo(dtype).max

    # Load all the stuff into our own lists
    head = np.empty(n_nodes, dtype=dtype)
    nxt  = np.empty(2 * n_edges, dtype=dtype)
    data = np.empty(2 * n_edges, dtype=dtype)

    head.fill(invalid)

    i = 0
    for u, v in islice(iterable, n_edges):
        tmp = head[u]
        data[i] = v
        nxt[i] = tmp
        head[u] = i
        i += 1

        tmp = head[v]
        data[i] = u
        nxt[i] = tmp
        head[v] = i
        i += 1
    n_edges = i / 2

    # The final data is stored using mmap array
    if not exists(store_dir):
        os.mkdir(store_dir, 0755)

    mmap = lambda x, y : np.memmap(join(store_dir, x), mode="w+",
                                   dtype=dtype, shape=y)

    indptr  = mmap("indptr.dat", n_nodes + 1)
    indices = mmap("indices.dat", 2 * n_edges)

    # Copy stuff into the mmapped arrays
    indptr[0] = 0
    i = 0
    for v in xrange(n_nodes):
        j = head[v]
        while j != invalid:
            indices[i] = data[j]
            j = nxt[j]
            i += 1
        indptr[v + 1] = i

    # Make sure stuff is saved so others can read
    with open(join(store_dir, "base.pickle"), "wb") as fobj:
        pk.dump((n_nodes, n_edges, dtype), fobj, -1)

    indptr.flush()
    indices.flush()

    # Finally create our graph
    G = Graph(indptr, indices, n_nodes, n_edges)
    return G

def load(store_dir):
    """
    Load a Graph
    """

    assert isdir(store_dir)

    with open(join(store_dir, "base.pickle")) as fobj:
        n_nodes, n_edges, dtype = pk.load(fobj)

    mmap = lambda x, y : np.memmap(join(store_dir, x), mode="r",
                                   dtype=dtype, shape=y)

    indptr  = mmap("indptr.dat", n_nodes + 1)
    indices = mmap("indices.dat", 2 * n_edges)

    G = Graph(indptr, indices, n_nodes, n_edges)
    return G

