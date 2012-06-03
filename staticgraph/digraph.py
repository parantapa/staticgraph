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
NTYPE = np.uint32
ATYPE = np.uint64

NEND = np.iinfo(NTYPE).max
AEND = np.iinfo(ATYPE).max

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

def _make_el(n_arcs, iterable):
    """
    Make the sorted edge list
    """

    # Allocate memory
    a = np.empty((n_arcs, 2), dtype=NTYPE)

    # Load all arcs into memory
    i = 0
    for u, v in islice(iterable, n_arcs):
        a[i, 0] = u
        a[i, 1] = v
        i += 1
    n_arcs = i

    # Create a view for sorting
    dt = [('c0', NTYPE), ('c1', NTYPE)]
    b = a.ravel().view(dt)

    # Sort the array
    b.sort(order=['c0','c1'])

    return n_arcs, a

def _make_graph(indptr, indices, n_nodes, n_arcs, el, simple, fwd):
    """
    Make compact representation of the graph
    """

    x, y = (0, 1) if fwd else (1, 0)

    indptr[0] = 0
    i, j, k = 0, 0, 0
    while i < n_nodes:
        while j < n_arcs and el[j, x] == i:
            # Skip self loops
            if simple and el[j, y] == i:
                j += 1
                continue

            # Skip parallel edges
            if simple and k != 0 and el[j, y] == indices[k - 1]:
                j += 1
                continue

            indices[k] = el[j, y]
            k += 1
            j += 1

        indptr[i + 1] = k
        i += 1

            
def make(store_dir, n_nodes, n_arcs, iterable, simple=False):
    """
    Make a DiGraph
    """

    assert NEND > n_nodes
    assert AEND > n_arcs

    # Load the edgelist to memory
    n_arcs, el = _make_el(n_arcs, iterable)

    if store_dir != ":memory:":
        # The final data is stored using mmap array
        if not exists(store_dir):
            os.mkdir(store_dir, 0755)

        mmap = lambda x, y, z : np.memmap(join(store_dir, x), mode="w+",
                                          shape=y, dtype=z)
    else:
        mmap = lambda _, y, z : np.empty(shape=y, dtype=z)

    p_indptr  = mmap("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = mmap("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = mmap("s_indices.dat", n_arcs, NTYPE)

    # Copy stuff into the mmapped arrays
    _make_graph(s_indptr, s_indices, n_nodes, n_arcs, el, simple, True)
    _make_graph(p_indptr, s_indices, n_nodes, n_arcs, el, simple, False)

    n_arcs = s_indptr[n_nodes]

    if store_dir != ":memory:":
        # Make sure stuff is saved so others can read
        with open(join(store_dir, "base.pickle"), "wb") as fobj:
            pk.dump((n_nodes, n_arcs), fobj, -1)

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
        n_nodes, n_arcs = pk.load(fobj)

    mmap = lambda x, y, z : np.memmap(join(store_dir, x), mode="r",
                                      shape=y, dtype=z)

    p_indptr  = mmap("p_indptr.dat", n_nodes + 1, ATYPE)
    p_indices = mmap("p_indices.dat", n_arcs, NTYPE)
    s_indptr  = mmap("s_indptr.dat", n_nodes + 1, ATYPE)
    s_indices = mmap("s_indices.dat", n_arcs, NTYPE)

    G = DiGraph(p_indptr, p_indices, s_indptr, s_indices, n_nodes, n_arcs)
    return G
