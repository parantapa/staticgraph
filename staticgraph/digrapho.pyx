"""
Faster implementation of DiGraph and CompactDiGraph

This module defines subclasses of the above classes with some of the methods
optimized.
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

from staticgraph import digraph

class DiGraph(digraph.DiGraph):
    def __init__(self, node_reserve, arc_reserve):
        super(DiGraph, self).__init__(node_reserve, arc_reserve)

    def add_arcs(self, object arc_gen):
        """
        Add an arc from node u to node v
        """

        cdef:
            size_t u
            size_t v
            size_t head
            size_t n_arcs = self.n_arcs
            np.ndarray[DTYPE_t, ndim=2] pred = self.pred
            np.ndarray[DTYPE_t, ndim=2] succ = self.succ
            np.ndarray[DTYPE_t, ndim=1] p_head = self.p_head
            np.ndarray[DTYPE_t, ndim=1] s_head = self.s_head
            np.ndarray[DTYPE_t, ndim=1] m_indegree = self.m_indegree
            np.ndarray[DTYPE_t, ndim=1] m_outdegree = self.m_outdegree

        for u, v in arc_gen:
            new = n_arcs

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

            n_arcs += 1

        self.n_arcs = n_arcs

class CompactDiGraph(digraph.CompactDiGraph):
    def __init__(self, store_dir, data=None):
        super(CompactDiGraph, self).__init__(store_dir, data)

    def _copy(self, data):
        """
        Copy the given graph onto this one
        """

        cdef:
            size_t u
            size_t v
            size_t i
            size_t idx
            size_t n_nodes = self.n_nodes

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
        for u in range(n_nodes):
            self_s_head[u] = idx
            i = data_s_head[u]
            while i != INVALID:
                self_succ[idx] = data_succ[i, 0]
                i = data_succ[i, 1]
                idx += 1

        idx = 0
        for v in range(n_nodes):
            self_p_head[v] = idx
            i = data_p_head[v]
            while i != INVALID:
                self_pred[idx] = data_pred[i, 0]
                i =  data_pred[i, 1]
                idx += 1

