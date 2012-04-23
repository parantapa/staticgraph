"""
Space efficient Directed Graph implementation

This module features two very restricted graph implementations, which on the
plus side are very space efficient. Both use adjacency list implementation.
Storage is handled by NumPy. The implementation at its current stage is not very
CPU efficient (every thing is pure Python).

Use this if you already have a static graph. There is almost no support for
modifying the graph at runtime.

DiGraph can store 50 million nodes and 2 billion edges using 30 GB memory.
StaticDiGraph can store the same using about 16 GB memory.

NOTE: Since 32 bit unsigned storage is used, this graph is unable to handle more
than 4 Billion edges or nodes (2^32-1 to be more precise).
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"
__version__ = "0.1"

import os
from os.path import join, exists, isdir
from cPickle import load, dump

import numpy as np
DTYPE   = np.uint32

cimport numpy as np
cimport cython
ctypedef np.uint32_t DTYPE_t
cdef DTYPE_t INVALID = 4294967295

cdef class DiGraphBase:
    """
    Base class for DiGraph and StaticDiGraph

    Abstract class; Don't use directly.
    """

    cdef:
        np.ndarray pred         # Storage for the predecessor lists
        np.ndarray succ         # Storage for the successor lists
        np.ndarray p_head       # List head pointer for predecessors
        np.ndarray s_head       # List head pointer for successors
        np.ndarray m_indegree   # Out degree of a node
        np.ndarray m_outdegree  # In degree of a node
        size_t n_nodes          # Number of nodes
        size_t n_arcs           # Number of arcs

    def nbytes(self):
        """
        Returns the total bytes used to store internal arrays
        """

        bytes_n  = self.pred.nbytes
        bytes_n += self.succ.nbytes
        bytes_n += self.p_head.nbytes
        bytes_n += self.s_head.nbytes
        bytes_n += self.m_indegree.nbytes
        bytes_n += self.m_outdegree.nbytes

        return bytes_n

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
        Return in degree of node v
        """

        return self.m_indegree[v]

    def outdegree(self, u):
        """
        Return out degree of node u
        """

        return self.m_outdegree[u]

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
            for u in self.nodes():
                for v in self.successors(u):
                    yield (u, v)
        else:
            for v in self.nodes():
                for u in self.predecessors(v):
                    yield (u, v)

    def has_node(self, u):
        """
        Check if node u exists
        """

        return (0 <= u < self.n_nodes)

    def has_arc(self, u, v):
        """
        Check if arc (u, v) exists
        """

        for x in self.successors(u):
            if x == v:
                return True
        return False

cdef class DiGraph(DiGraphBase):
    """
    DiGraph(node_reserve, arc_reserve)

    Make sure to pass appropriate values to node_reserve and arc_reserve. Memory
    is preallocated based on these parameters. There are no options to change
    this at runtime. Nodes are represented using simple unsigned integers and
    are in the range [0, node_reserve). Arcs have to be added later using
    add_arc method.
    """

    cdef size_t node_reserve
    cdef size_t arc_reserve

    def __init__(self, node_reserve, arc_reserve):

        self.node_reserve = node_reserve
        self.arc_reserve  = arc_reserve

        self.pred = np.empty((arc_reserve, 2), dtype=DTYPE)
        self.succ = np.empty((arc_reserve, 2), dtype=DTYPE)

        self.p_head = np.empty(node_reserve, dtype=DTYPE)
        self.s_head = np.empty(node_reserve, dtype=DTYPE)
        self.p_head.fill(INVALID)
        self.s_head.fill(INVALID)

        self.m_indegree  = np.zeros(node_reserve, dtype=DTYPE)
        self.m_outdegree = np.zeros(node_reserve, dtype=DTYPE)

        self.n_nodes = node_reserve
        self.n_arcs  = 0

    def add_arcs(self, object arc_gen):
        """
        Add an arc from node u to node v
        """

        cdef:
            size_t u
            size_t v
            size_t head
            size_t new = self.n_arcs
            np.ndarray[DTYPE_t, ndim=2] pred = self.pred
            np.ndarray[DTYPE_t, ndim=2] succ = self.succ
            np.ndarray[DTYPE_t, ndim=1] p_head = self.p_head
            np.ndarray[DTYPE_t, ndim=1] s_head = self.s_head
            np.ndarray[DTYPE_t, ndim=1] m_indegree = self.m_indegree
            np.ndarray[DTYPE_t, ndim=1] m_outdegree = self.m_outdegree

        for u, v in arc_gen:
            new = self.n_arcs

            head = p_head[v]
            pred[new, 0] = u
            pred[new, 1] = head
            p_head[v] = new
            m_indegree[v] += 1

            head = s_head[u]
            succ[new, 0] = v
            succ[new, 1] = head
            s_head[u] = new
            m_outdegree[u] += 1

            self.n_arcs += 1

    def successors(self, u):
        """
        Return a generator that yields successors of u
        """

        i = self.s_head[u]

        while i != INVALID:
            yield self.succ[i, 0]
            i = self.succ[i, 1]

    def predecessors(self, v):
        """
        Return a generator that yields predecessors of v
        """

        i = self.p_head[v]

        while i != INVALID:
            yield self.pred[i, 0]
            i = self.pred[i, 1]

cdef class StaticDiGraph(DiGraphBase):
    """
    StaticDiGraph(store_dir, [data])

    Persistent static DiGraph implementation. store_dir is the directory where
    the data will be stored. In case data parameter is not given, it must point
    to a valid directory. In case data parameter is given, the directory must
    not exist, it will be created.

    Takes half memory for arcs than DiGraph. Memory mapped files are used for
    storage. Storage can be reduced because during creation, ind egree and
    out degree of nodes are known. So instead of using linked list, we use
    contiguous storage.
    """

    def __init__(self, store_dir, data=None):

        if data is None:
            assert isdir(store_dir)

            with open(join(store_dir, "base.pickle"), "rb") as fobj:
                self.n_nodes, self.n_arcs = load(fobj)

            self._memmap(store_dir, "r")
        else:
            assert not exists(store_dir)
            os.mkdir(store_dir, 0755)

            self.n_nodes  = data.order()
            self.n_arcs   = data.size()

            with open(join(store_dir, "base.pickle"), "wb") as fobj:
                dump((self.n_nodes, self.n_arcs), fobj, -1)

            self._memmap(store_dir, "w+")
            self._copy(data)

    def _memmap(self, store_dir, mode):
        """
        Initialize the memory mapped files
        """

        self.pred = np.memmap(join(store_dir, "pred.dat"), mode=mode,
                               dtype=DTYPE, shape=(self.n_arcs,),)
        self.succ = np.memmap(join(store_dir, "succ.dat"), mode=mode,
                               dtype=DTYPE, shape=(self.n_arcs,))

        self.p_head = np.memmap(join(store_dir, "p_head.dat"), mode=mode,
                              dtype=DTYPE, shape=(self.n_nodes,))
        self.s_head = np.memmap(join(store_dir, "s_head.dat"), mode=mode,
                              dtype=DTYPE, shape=(self.n_nodes,))

        self.m_indegree  = np.memmap(join(store_dir, "m_indegree.dat"),
                                     mode=mode, dtype=DTYPE,
                                     shape=(self.n_nodes,))
        self.m_outdegree = np.memmap(join(store_dir, "m_outdegree.dat"),
                                     mode=mode, dtype=DTYPE,
                                     shape=(self.n_nodes,))

    cdef _copy(self, DiGraph data):
        """
        Copy the given graph onto this one
        """

        cdef:
            size_t u
            size_t v
            size_t i
            size_t idx

            np.ndarray[DTYPE_t, ndim=1] self_pred = self.pred
            np.ndarray[DTYPE_t, ndim=1] self_succ = self.succ
            np.ndarray[DTYPE_t, ndim=1] self_p_head = self.p_head
            np.ndarray[DTYPE_t, ndim=1] self_s_head = self.s_head
            np.ndarray[DTYPE_t, ndim=1] self_m_indegree = self.m_indegree
            np.ndarray[DTYPE_t, ndim=1] self_m_outdegree = self.m_outdegree

            np.ndarray[DTYPE_t, ndim=2] data_pred = data.pred
            np.ndarray[DTYPE_t, ndim=2] data_succ = data.succ
            np.ndarray[DTYPE_t, ndim=1] data_p_head = data.p_head
            np.ndarray[DTYPE_t, ndim=1] data_s_head = data.s_head
            np.ndarray[DTYPE_t, ndim=1] data_m_indegree = data.m_indegree
            np.ndarray[DTYPE_t, ndim=1] data_m_outdegree = data.m_outdegree

        self_m_indegree[:]  = data_m_indegree[:]
        self_m_outdegree[:] = data_m_outdegree[:]

        idx = 0
        for u in range(self.n_nodes):
            self_s_head[u] = idx
            i = data_s_head[u]
            while i != INVALID:
                self_succ[idx] = data_succ[i, 0]
                i = data_succ[i, 1]
                idx += 1

        idx = 0
        for v in range(self.n_nodes):
            self_p_head[v] = idx
            i = data_p_head[v]
            while i != INVALID:
                self_pred[idx] = data_pred[i, 0]
                i =  data_pred[i, 1]
                idx += 1

    def successors(self, u):
        """
        Return an iterable which yields successors of u
        """

        start = self.s_head[u]
        stop  = start + self.m_outdegree[u]

        return self.succ[start:stop]

    def predecessors(self, v):
        """
        Return an iterabl which yields predecessors of v
        """

        start = self.p_head[v]
        stop  = start + self.m_indegree[v]

        return self.pred[start:stop]

