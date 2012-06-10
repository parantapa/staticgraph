"""
Handle creation and loading of digraph arrays
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

import os
from os.path import join, exists, isdir
import cPickle as pk
import numpy as np

from staticgraph.digraph import DiGraph
from staticgraph.types import ATYPE, NTYPE

def alloc_digraph(n_nodes, n_arcs, store):
    """
    Make arrays for storing
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
