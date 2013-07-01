import staticgraph as sg
from numpy import zeros, empty, uint32, uint64
from random import randint

def eccentricity(G, v=None):
    """
    Return the eccentricity of nodes in G.

    The eccentricity of a node v is the maximum distance from v to
    all other nodes in G.

    Parameters
    ----------
    G : An undirected staticgraph

    v : node, optional
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
    n_nodes = randint(0, order)
    nodes = empty(n_nodes, dtype = uint32)
    edgelist = empty((n_nodes ** 2, 2), dtype = uint32) 
    index = 0

    if v != None:
        nodes[0] = v
        index = 1

    while index < n_nodes:
        rnd = randint(0, order - 1)
        if rnd in nodes:
            continue
        nodes[index] = rnd
        index += 1

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
        return sp[0].size - 2

    ecc = empty((2, n_nodes), dtype = uint32)
    index = 0
    for u in xrange(n_nodes):
        sp = sg.graph_traversal.bfs_all(b, u)
        ecc[0, index] = nodes[u]
        ecc[1, index] = sp[0].size - 2
        index += 1

    return ecc
