"""
Functions for the standard distance measures for directed graphs.
"""

import staticgraph as sg
from numpy import empty, uint32, amax, amin, array
from random import sample

def eccentricity(G, n_nodes, v=None):
    """
    Return the eccentricity of nodes in G.

    The eccentricity of a node v is the maximum distance from v to
    all other nodes in a subgraph of GG.

    Parameters
    ----------
    G :       A directed staticgraph

    n_nodes : Total no.of nodes of subgraph.

    v :       node, optional
              Return value of specified node       

    Returns
    -------
    ecc : A 2D numpy array.
          Row 1: Node labels
          Row 2: Eccentricity of corresponding nodes.
    """

    if v != None and v >= G.order():
        raise sg.exceptions.StaticGraphNodeAbsentException("given node absent in graph!!")
    
    order = G.order()
    edgelist = empty((n_nodes ** 2, 2), dtype = uint32) 
    index = 0

    nodes = sample(xrange(order), n_nodes)    
    nodes = array(nodes, dtype = uint32)
    
    if v != None:
        if v not in nodes:
            nodes[0] = v

    if v != None:
        sp = sg.digraph_traversal.bfs_all(G, v)
        if G.out_degree(v) == 0:
            return (2 ** 32) - 1
        return sp[0].size - 2

    ecc = empty((2, n_nodes), dtype = uint32)
    index = 0
    for i in xrange(n_nodes):
        sp = sg.digraph_traversal.bfs_all(G, nodes[i])
        ecc[0, i] = nodes[i]
        if G.out_degree(nodes[i]) == 0:
            ecc[1, i] = (2 ** 32) - 1
        else:
            ecc[1, i] = sp[0].size - 2

    return ecc

def diameter(G,  n_nodes, e = None):
    """
    Return the diameter of a subgraph of G.

    The diameter is the maximum eccentricity.

    Parameters
    ----------
    G : A directed staticgraph

    n_nodes : Total no.of nodes of subgraph.

    e : eccentricity numpy 2D array, optional
      A precomputed numpy 2D array of eccentricities.

    Returns
    -------
    Diameter of graph

    See Also
    --------
    eccentricity
    """
    
    if e is None:
        e = eccentricity(G , n_nodes)
    e = e[1]
    if e.size == 0:
        return None
    return amax(e)

def radius(G, n_nodes, e = None):
    """
    Return the radius of a subgraph of G.

    The radius is the minimum eccentricity.

    Parameters
    ----------
    G : A directed staticgraph

    n_nodes : Total no.of nodes of subgraph.

    e : eccentricity numpy 2D array, optional
      A precomputed numpy 2D array of eccentricities.

    Returns
    -------
    Radius of graph

    See Also
    --------
    eccentricity
    """

    if e is None:
        e = eccentricity(G, n_nodes)
    e = e[1]
    if e.size == 0:
        return None
    return amin(e)

def periphery(G, n_nodes, e = None):
    """
    Return the periphery of a subgraph of G. 

    The periphery is the set of nodes with eccentricity equal to the diameter. 

    Parameters
    ----------
    G : A directed staticgraph

    n_nodes : Total no.of nodes of subgraph.

    e : eccentricity numpy 2D array, optional
      A precomputed numpy 2D array of eccentricities.

    Returns
    -------
    p : numpy array of nodes in periphery
    """
    
    if e is None:
        e = eccentricity(G, n_nodes)

    sort_indices = e[1].argsort()
    e[0] = e[0][sort_indices]
    e[1] = e[1][sort_indices]

    i = e[0].size - 1
    while i >= 0:
        if e[1, i] < e[1, -1]:
            break
        i -= 1

    return e[0][i + 1:]

def center(G, n_nodes, e = None):
    """
    Return the center of a subgraph of G. 

    The center is the set of nodes with eccentricity equal to the radius. 

    Parameters
    ----------
    G : A directed staticgraph

    n_nodes : Total no.of nodes of subgraph.

    e : eccentricity numpy 2D array, optional
      A precomputed numpy 2D array of eccentricities.

    Returns
    -------
    p : numpy array of nodes in center
    """
    
    if e is None:
        e = eccentricity(G, n_nodes)

    sort_indices = e[1].argsort()
    e[0] = e[0][sort_indices]
    e[1] = e[1][sort_indices]

    i = 0
    while i < e[0].size:
        if e[1, i] > e[1, 0]:
            break
        i += 1

    return e[0][:i]
