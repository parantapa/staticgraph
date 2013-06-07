"""
Simple memory efficient undirected graph.
"""

from os import mkdir
from os.path import join, exists
import cPickle as pk
from itertools import imap

import numpy as np
import staticgraph.edgelist as edgelist

class Graph(object):
    """
    Simple undirected graph.

    n_nodes   - # nodes
    n_edges   - # edges
    n_indptr  - index pointers for nodes of graph
    n_indices - indices of nodes of graph
    """

    def __init__(self, n_nodes, n_edges, n_indptr, n_indices):

        self.n_nodes   = n_nodes
        self.n_edges   = n_edges
        self.n_indptr  = n_indptr
        self.n_indices = n_indices

    @property
    def nbytes(self):
        """
        Return total size of internal arrays in bytes.
        """

        nbytes  = self.n_indptr.nbytes
        nbytes += self.n_indices.nbytes
        return nbytes

    def neighbours(self, u):
        """
        Return iterable for neighbours of node u.
        """

        start = self.n_indptr[u]
        stop  = self.n_indptr[u + 1]
        return imap(int, self.n_indices[start:stop])

    def degree(self, v):
        """
        Return degree of node v.
        """

        start = self.n_indptr[v]
        stop  = self.n_indptr[v + 1]
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

    def edges(self):
        """
        Return iterable for edges of the graph.
        """

        for u in self.nodes():
            for v in self.neighbours(u):
                yield u, v

    def has_node(self, u):
        """
        Check if node u exists.
        """

        return (0 <= u < self.n_nodes)

    def has_edge(self, u, v):
        """
        Check if edge (u, v) exists.
        """
        if v > u:
            u, v = v, u

        return (v in self.neighbours(u))
        
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
    n_indptr  = do_load("n_indptr.npy")
    n_indices = do_load("n_indices.npy")
    
    # Create the graph
    G = Graph(n_nodes, n_edges, n_indptr, n_indices)
    return G

def save(store, G):
    """
    Save the graph to disk.

    store - the directory where the graph will be stored
    G     - the direceted graph
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
    do_save("n_indptr.npy", G.n_indptr)
    do_save("n_indices.npy", G.n_indices)
    
def make(n_nodes, n_edges, edges):
    """
    Make a Graph.

    n_nodes - # nodes in the graph.
              The graph contains all nodes form 0 to (n_nodes - 1)
    n_edges - an over estimate of the number of edges
    edges   - an iterable producing the edges of the graph
    """

    n_nodes = int(n_nodes)
    n_edges = int(n_edges)

    # Create the edgelist
    es = edgelist.make(n_nodes, n_edges, edges)

    # Compact the edgelist
    n_indptr, n_indices = edgelist.compact(n_nodes, es)

    # Create the graph
    G = Graph(n_nodes, len(es), n_indptr, n_indices)
    return G
