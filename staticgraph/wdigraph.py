"""
Simple memory efficient weighted undirected graph.
"""

from os import mkdir
from os.path import join, exists
import cPickle as pk
from itertools import imap

import numpy as np
import staticgraph.wdigraph_edgelist as edgelist

class WDiGraph(object):
    """
    Simple undirected weighted graph.

    n_nodes   - # nodes
    n_edges   - # edges
    p_indptr  - index pointers for predecessors
    p_indices - indices for predecessors
    s_indptr  - index pointers for succesors
    s_indices - indices for successors
    weights   - corresponding weights of edges of graph
    """

    def __init__(self, n_nodes, n_edges, p_indptr, p_indices, 
                               s_indptr, s_indices, weights):

        self.n_nodes   = n_nodes
        self.n_edges   = n_edges
        self.p_indptr  = p_indptr
        self.p_indices = p_indices
        self.s_indptr  = s_indptr
        self.s_indices = s_indices
        self.weights = weights

    @property
    def nbytes(self):
        """
        Return total size of internal arrays in bytes.
        """

        nbytes  = self.n_indptr.nbytes
        nbytes += self.n_indices.nbytes
        nbytes += self.weights.nbytes
        return nbytes

    def successors(self, u, weight = False):
        """
        Return iterable for successors of node u.
        """

        start = self.s_indptr[u]
        stop  = self.s_indptr[u + 1]
        for index in xrange(start, stop):
            if weight == False:
                yield  self.s_indices[index]
            else: 
                yield self.s_indices[index], self.weights[index]

    def predecessors(self, u):
        """
        Return iterable for predecessors of node u.
        """

        start = self.p_indptr[u]
        stop  = self.p_indptr[u + 1]
        return imap(int, self.p_indices[start:stop])

    def in_degree(self, v):
        """
        Return in-degree of node v.
        """

        start = self.p_indptr[v]
        stop  = self.p_indptr[v + 1]
        return int(stop - start)

    def out_degree(self, v):
        """
        Return out-degree of node v.
        """

        start = self.s_indptr[v]
        stop  = self.s_indptr[v + 1]
        return int(stop - start)

    def order(self):
        """
        Return number of nodes in the graph.
        """

        return self.n_nodes

    def size(self):
        """
        Return number of edges in the graph.
        """

        return self.n_edges

    def nodes(self):
        """
        Return iterable for nodes of the graph.
        """

        return xrange(self.n_nodes)

    def edges(self, weight = False):
        """
        Return iterable for edges of the graph.
        """

        for u in self.nodes():
            for v in self.successors(u):
                if u < v:
                    if weight == False:
                        yield u, v
                    else: 
                        yield u, v, self.weight(u, v)

    def weight(self, u, v):
        """
        Return weight of the edge (u,v) if it exists
        """
        start = self.s_indptr[u]
        stop = self.s_indptr[u + 1]
        for i in xrange(start, stop):
            if self.s_indices[i] == v:
                return self.weights[i]
        return None

    def has_node(self, u):
        """
        Check if node u exists.
        """

        return (0 <= u < self.n_nodes)

    def has_edge(self, u, v):
        """
        Check if edge (u, v) exists.
        """

        return (v in self.successors(u))

def load(store):
    """
    Load a graph from disk.

    store - directory where the graph is stored
    """

    # Load basic info
    fname = join(store, "base.pickle")
    with open(fname, "rb") as fobj:
        n_nodes, n_edges = pk.load(fobj)

    # define load shortcut
    do_load = lambda fname : np.load(join(store, fname), "r")

    # Make the arrays
    p_indptr  = do_load("p_indptr.npy")
    p_indices = do_load("p_indices.npy")
    s_indptr  = do_load("s_indptr.npy")
    s_indices = do_load("s_indices.npy")
    weights = do_load("weights.npy")
    # Create the graph
    G = WDiGraph(n_nodes, n_edges, p_indptr, p_indices,
                          s_indptr, s_indices, weights)
    
    return G

def save(store, G):
    """
    Save the graph to disk.

    store - the directory where the graph will be stored
    G     - the weighted graph
    """

    # Create the directory
    if not exists(store):
        mkdir(store)

    # Save basic info
    fname = join(store, "base.pickle")
    with open(fname, "wb") as fobj:
        pk.dump((G.n_nodes, G.n_edges), fobj, -1)

    # define save shortcut
    do_save = lambda fname, arr : np.save(join(store, fname), arr)

    # Make the arrays
    do_save("p_indptr.npy", G.p_indptr)
    do_save("p_indices.npy", G.p_indices)
    do_save("s_indptr.npy", G.s_indptr)
    do_save("s_indices.npy", G.s_indices)
    do_save("weights.npy", G.weights)

def make_deg(n_nodes, edges):
    """
    Return the degree distribution of the Weighted Graph
    """

    return edgelist.make_deg(n_nodes, edges)

def make(n_nodes, n_edges, edges, deg):
    """
    Make a Weighted Graph.

    n_nodes - # nodes in the graph.
              The graph contains all nodes form 0 to (n_nodes - 1)
    n_edges - an over estimate of the number of edges
    edges   - an iterable producing the edges of the graph
    deg     - a numpy uint32 array containing the degree of all vertices.
    """

    n_nodes = int(n_nodes)
    n_edges = int(n_edges)
    p_deg, s_deg = deg

    # Create and Compact the edgelist
    p_indptr, p_indices, s_indptr, s_indices, weights = edgelist.make_comp(n_nodes, n_edges, edges, p_deg, s_deg)

    # Create the graph
    G = WDiGraph(n_nodes, len(s_indices), p_indptr, p_indices, s_indptr, s_indices, weights)
    return G
