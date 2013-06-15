"""
Module implementing the standard shortest path algorithms for unweighted graphs
"""

from numpy import arange, int32, zeros
from itertools import imap
from staticgraph.exceptions import StaticGraphNodeAbsentException

def single_source_shortest_path(G, s):
    """
    Returns a sequence of vertices alongwith the length of their 
    shortest paths from source node s for an undirected staticgraph G.
    
    Parameters
    ----------
    G : An undirected staticgraph.
    s : Source node.
    
    Returns
    -------
    path : A 2-dimensional numpy int32 array.
          1st row: The set of vertices.
          2nd row: Corresponding predecessors in shortest path from the source
          3rd row: Corresponding distances from the source in the shortest path

    Notes
    ------

    It is mandatory that G be undirected.
    """
    
    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    
    order = G.order()
    path = arange((order * 3), dtype = int32)
    path[order : order * 3] = -1
    path = path.reshape(3, order)
    
    queue = zeros(order, dtype = int32)
    
    front = rear = 0
    queue[rear] = s
    path[2, s] = 0
    rear = 1
    
    while (front != rear):
        u = queue[front]
        front = front + 1
        start = G.n_indptr[u]
        stop = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if path[1, v] == -1 and v != s:
                path[1, v] = u
                path[2, v] = path[2, u] + 1
                queue[rear] = v
                rear = rear + 1
    return path
