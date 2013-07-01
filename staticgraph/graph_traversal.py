"""
Module implementing the standard traversal techniques for an undirected graph
"""

from numpy import uint32, zeros, empty, int64
from itertools import imap
from staticgraph.exceptions import StaticGraphNodeAbsentException

def bfs_all(G, s, maxdepth = (2 ** 16) - 1):
    """
    Returns a sequence of vertices for 
    staticgraph G in a breadth-first-search order starting at source s.
    
    Parameters
    ----------
    G        : An undirected staticgraph.
    s        : Source node to start the bfs traversal.
    maxdepth : Optional parameter denoting the maximum depth for traversal.
    
    Returns
    -------
    bfs_indices : A numpy uint32 array returning a sequence of vertices in 
                  BFS traversal starting from s.
             
    bfs_indptr  :  A numpy uint32 array returning the starting index pointers of a 
                   particular depth in bfs_indices.
    
    Notes
    ------

    It is mandatory that G be undirected.
    """
    
    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    
    order = G.order()
    dist = empty(order , dtype = uint32)
    dist[:] = (2 ** 32) - 1
    
    queue = empty(order, dtype = uint32)
    bfs_indices = empty((order), dtype = uint32)
    bfs_indptr = empty((maxdepth + 2), dtype = int64)
    bfs_indptr[:] = (2 ** 32) - 1
    front = rear = 0
    queue[rear] = s
    dist[s] = 0
    bfs_indptr[0] = 0
    rear = 1
    index = 0
    depth = 0
    
    while (front != rear and depth <= maxdepth):
        u = queue[front]
        bfs_indices[index] = u
        if bfs_indptr[dist[u]] == (2 ** 32) - 1:
             bfs_indptr[dist[u]] = index
             depth += 1
        index += 1
        front += 1
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if dist[v] == (2 ** 32) - 1:
                dist[v] = dist[u] + 1
                queue[rear] = v
                rear = rear + 1
    if depth <= maxdepth:
        depth += 1
    bfs_indptr[depth] = index
    return bfs_indptr[:depth + 1], bfs_indices[:index]

def traverse_dfs(G, s):
    """
    Returns a sequence of vertices alongwith their predecessors for 
    staticgraph G in a depth-first-search order starting at source s.

    Parameters
    ----------
    G : An undirected staticgraph.
    s : Source node to start the dfs traversal.
    
    Returns
    -------
    res :A 2-Dimensional numpy int32 array.
          1st row: A sequence of vertices in BFS traversal starting from s.
          2nd row: The immediate predecessors of the vertices traversed.

    Notes
    ------

    It is mandatory that G be undirected.
    Predecessor is -1 for the source node.
    """

    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    
    order = G.order()
    pred = zeros(order, dtype = int32)
    pred -= 1
    
    res = zeros((2, order), dtype = int32)
    stack = zeros(order, dtype = int32)

    index = 1
    top = 0
    res[0, 0] = stack[top] = s
    res[1, 0] = -1
    
    while top >= 0:
        u = stack[top]
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if pred[v] == -1 and v != s:
                pred[v] = u
                top = top + 1
                res[0, index] = stack[top] = v
                res[1, index] = u
                index = index + 1
                break
        else:
            top = top - 1  
    return res[:, :index]
