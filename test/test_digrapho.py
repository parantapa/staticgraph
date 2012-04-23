"""
Tests for static graph modules
"""

from __future__ import division

import os
import tempfile
from random import randint
from numpy.testing import assert_equal as np_equal

from staticgraph import digraph
from staticgraph import digrapho

G1, G2, H1, H2 = None, None, None, None
STORE_DIR1, STORE_DIR2 = None, None

def setup_module(module):
    """
    Create the graphs
    """

    global G1, G2, H1, H2, STORE_DIR1, STORE_DIR2

    node_reserve = 100
    arc_reserve = 10000

    G1 = digraph.DiGraph(node_reserve, arc_reserve)
    G2 = digrapho.DiGraph(node_reserve, arc_reserve)

    ARC_GEN = []
    for _ in xrange(arc_reserve):
        u = randint(0, node_reserve -1)
        v = randint(0, node_reserve -1)
        ARC_GEN.append((u, v))

    G1.add_arcs(ARC_GEN)
    G2.add_arcs(ARC_GEN)

    STORE_DIR1 = tempfile.mkdtemp()
    STORE_DIR2 = tempfile.mkdtemp()

    H1 = digraph.CompactDiGraph(STORE_DIR1, G1)
    H2 = digrapho.CompactDiGraph(STORE_DIR2, G2)

def teardown_module(module):
    """
    Remove the created temporary directory
    """

    os.remove(os.path.join(STORE_DIR1, "base.pickle"))
    os.remove(os.path.join(STORE_DIR1, "pred.dat"))
    os.remove(os.path.join(STORE_DIR1, "succ.dat"))
    os.remove(os.path.join(STORE_DIR1, "p_head.dat"))
    os.remove(os.path.join(STORE_DIR1, "s_head.dat"))
    os.remove(os.path.join(STORE_DIR1, "m_indegree.dat"))
    os.remove(os.path.join(STORE_DIR1, "m_outdegree.dat"))
    os.rmdir(STORE_DIR1)

    os.remove(os.path.join(STORE_DIR2, "base.pickle"))
    os.remove(os.path.join(STORE_DIR2, "pred.dat"))
    os.remove(os.path.join(STORE_DIR2, "succ.dat"))
    os.remove(os.path.join(STORE_DIR2, "p_head.dat"))
    os.remove(os.path.join(STORE_DIR2, "s_head.dat"))
    os.remove(os.path.join(STORE_DIR2, "m_indegree.dat"))
    os.remove(os.path.join(STORE_DIR2, "m_outdegree.dat"))
    os.rmdir(STORE_DIR2)

def test_digraph():
    """
    Test internal data sturctures are equal
    """

    np_equal(G1.pred, G2.pred)
    np_equal(G1.succ, G2.succ)
    np_equal(G1.p_head, G2.p_head)
    np_equal(G1.s_head, G2.s_head)
    np_equal(G1.m_indegree, G2.m_indegree)
    np_equal(G1.m_outdegree, G2.m_outdegree)

    assert G1.n_nodes == G2.n_nodes
    assert G1.n_arcs == G2.n_arcs

def test_compactdigraph():
    """
    Test internal data sturctures are equal
    """
    np_equal(H1.pred, H2.pred)
    np_equal(H1.succ, H2.succ)
    np_equal(H1.p_head, H2.p_head)
    np_equal(H1.s_head, H2.s_head)
    np_equal(H1.m_indegree, H2.m_indegree)
    np_equal(H1.m_outdegree, H2.m_outdegree)

    assert H1.n_nodes == H2.n_nodes
    assert H1.n_arcs == H2.n_arcs

