"""
Module implementing the standard traversal techniques for an undirected graph
"""

from numpy import arange, int32, zeros
from itertools import imap
from staticgraph.exceptions import StaticGraphNodeAbsentException

def traverse_bfs(G, s):
    """
    Returns a sequence of vertices alongwith their predecessors for 
    an undirected staticgraph G in a breadth-first-search order starting at source s.
    
    Parameters
    ----------
    G : An undirected staticgraph.
    s : Source node to start the bfs traversal.
    
    Returns
    -------
    res : A numpy int32 array.

    Notes
    ------

    It is mandatory that G be undirected.
    """
    
    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    
    order = G.order()
    visited = arange((order * 2), dtype = int32)
    visited[order : order * 2] = 0
    visited = visited.reshape(2, order)
    
    queue = zeros((2, order), dtype = int32)
    res = zeros((2, order), dtype = int32)
    
    front = rear = 0
    queue[0, rear] = s
    queue[1, rear] = -1
    rear = 1
    visited[1, s] = 1
    index = 0
    
    while (front != rear):
        u = queue[0, front]
        res[0, index] = u
        res[1, index] = queue[1, front]
        index = index + 1
        front = front + 1
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if visited[1, v] == 0:
                visited[1, v] = 1
                queue[0, rear] = v
                queue[1, rear] = u
                rear = rear + 1
    return res

def traverse_dfs(G, s):
    """
    Returns a sequence of vertices alongwith their predecessors for 
    an undirected staticgraph G in a depth-first-search order starting at source s.

    Parameters
    ----------
    G : An undirected staticgraph.
    s : Source node to start the dfs traversal.
    
    Returns
    -------
    res : A numpy int32 array.

    Notes
    ------

    It is mandatory that G be undirected.
    """

    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    
    order = G.order()
    visited = arange((order * 2), dtype = int32)
    visited[order : order * 2] = 0
    visited = visited.reshape(2, order)
    
    res = zeros((2, order), dtype = int32)
    stack = zeros((2, order), dtype = int32)

    visited[1, s] = 1
    index = 1
    top = 0
    res[0, 0] = stack[0, top] = s
    res[1, 0] = stack[1, top] = -1
    
    while top >= 0:
        u = stack[top]
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if visited[1, v] == 0:
                visited[1, v] = 1
                top = top + 1
                res[0, index] = stack[0, top] = v
                res[1, index] = stack[1, top] = u
                index = index + 1
                break
        else:
            top = top - 1  
    return res
