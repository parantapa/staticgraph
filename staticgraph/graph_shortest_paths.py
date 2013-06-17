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
    Precessor is -1 for the source node.
    distance = -1 implies that the node is unreachable from the source.
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

def floyd_warshall(G):
    """
    Find all-pairs shortest path lengths using Floyd-Warshall's algorithm.

    Parameters
    ----------
    G : An undirected unweighted simple staticgraph

    Returns
    -------
    Matrix : A 3-Dimensional NumPy Array.
             
             Matrix(:, :, 0) represents the distances of shortest paths 
             among all the pairs of vertices in G.

             Matrix(:, :, 1) represents the immediate predecessors
             in the corresponding shortest paths. 
             
    Notes
    ------
    Floyd's algorithm is appropriate for finding shortest paths in
    dense graphs or graphs with negative weights when Dijkstra's
    algorithm fails.  This algorithm can still fail if there are
    negative cycles.  It has running time O(n^3) with running space of O(n^2).
    
    G must be undirected, simple and unweighted.

    Distance > G.order() for node pair (i, j) if j is unreachable from i.
    Predecessor is -1 for node pair (i, j) if j is not reachable from i.
    """
    
    order = G.order()
    matrix = zeros((order, order, 2), dtype = int32)
    matrix[:, :, 0] = order + 1
    matrix[:, :, 1] = -1
    for (i, j) in G.edges():
        matrix[i, j, 0] = matrix[j, i, 0] = 1
        matrix[i, j, 1] = i
        matrix[j, i, 1] = j
    for k in xrange(order):
        for i in xrange(order):
            for j in xrange(order):
                if matrix[i, j, 0] > (matrix[i, k, 0] + matrix[k, j, 0]):
                    matrix[i, j, 0] = (matrix[i, k, 0] + matrix[k, j, 0])
                    matrix[i, j, 1] = matrix[k, j, 1]
    return matrix
