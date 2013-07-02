import staticgraph as sg
from numpy import zeros, empty, uint32, amax, amin, array, argsort
from random import randint, sample

def eccentricity(G, n_nodes, v=None):
    """
    Return the eccentricity of nodes in G.

    The eccentricity of a node v is the maximum distance from v to
    all other nodes in a subgraph of GG.

    Parameters
    ----------
    G :       An undirected staticgraph

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

    if v != None:
        nodes[0] = v
        index = 1

    nodes = sample(xrange(order), n_nodes)
    nodes = array(nodes, dtype = uint32)

    index = 0

    for i in xrange(n_nodes):
        for j in xrange(n_nodes):
            if G.has_edge(nodes[i], nodes[j]):
                edgelist[index] = (i, j)
                index += 1

    edgelist = edgelist[:index]
    deg = sg.graph.make_deg(n_nodes, iter(edgelist))
    b = sg.graph.make(n_nodes, index, iter(edgelist), deg)

    if v!= None:
        sp = sg.graph_traversal.bfs_all(b, 0)
        if G.degree(v) == 0:
            return (2 ** 32) - 1
        return sp[0].size - 2

    ecc = empty((2, n_nodes), dtype = uint32)
    index = 0
    for u in xrange(n_nodes):
        sp = sg.graph_traversal.bfs_all(b, u)
        ecc[0, index] = nodes[u]
        if G.degree(u) == 0:
            ecc[1, index] = (2 ** 32) - 1
        else:
            ecc[1, index] = sp[0].size - 2
        index += 1

    return ecc

def diameter(G,  n_nodes, e = None):
    """
    Return the diameter of a subgraph of G.

    The diameter is the maximum eccentricity.

    Parameters
    ----------
    G : A static graph

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
        e = eccentricity(G,n_nodes)
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
    G : A static graph

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

def periphery(G, n_nodes, e=None):
    """
    Return the periphery of a subgraph of G. 

    The periphery is the set of nodes with eccentricity equal to the diameter. 

    Parameters
    ----------
    G : An undirected staticgraph

    n_nodes : Total no.of nodes of subgraph.

    e : eccentricity numpy 2D array, optional
      A precomputed numpy 2D array of eccentricities.

    Returns
    -------
    p : numpy array of nodes in periphery
    """
    
    if e is None:
        e=eccentricity(G, n_nodes)

    sort_indices = e[1].argsort()
    e[0] = e[0][sort_indices]
    e[1] = e[1][sort_indices]

    i = e[0].size - 1
    while i >= 0:
        if e[1, i] < e[1, -1]:
            break
        i -= 1

    return e[0][i + 1:]

def center(G, n_nodes, e=None):
    """
    Return the center of a subgraph of G. 

    The center is the set of nodes with eccentricity equal to the radius. 

    Parameters
    ----------
    G : An undirected staticgraph

    n_nodes : Total no.of nodes of subgraph.

    e : eccentricity numpy 2D array, optional
      A precomputed numpy 2D array of eccentricities.

    Returns
    -------
    p : numpy array of nodes in center
    """
    
    if e is None:
        e=eccentricity(G, n_nodes)

    sort_indices = e[1].argsort()
    e[0] = e[0][sort_indices]
    e[1] = e[1][sort_indices]

    i = 0
    while i < e[0].size:
        if e[1, i] > e[1, 0]:
            break
        i += 1

    return e[0][:i]
