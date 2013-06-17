"""
Module implementing the standard traversal techniques for a directed graph
"""

from numpy import int32, zeros
from itertools import imap
from staticgraph.exceptions import StaticGraphNodeAbsentException

def traverse_bfs(G, s):
    """
    Returns a sequence of vertices alongwith their predecessors for 
    staticgraph G in a breadth-first-search order starting at source s.
    
    Parameters
    ----------
    G : A directed staticgraph.
    s : Source node to start the bfs traversal.
    
    Returns
    -------
    res : A 2-Dimensional numpy int32 array.
          1st row: A sequence of vertices in BFS traversal starting from s.
          2nd row: The immediate predecessors of the vertices traversed.

    Notes
    ------

    It is mandatory that G be directed.
    Predecessor is -1 for the source node.
    """
    
    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    
    order = G.order()
    pred = zeros(order , dtype = int32)
    pred -= 1
    
    queue = zeros(order, dtype = int32)
    res = zeros((2, order), dtype = int32)
    
    front = rear = 0
    queue[rear] = s
    rear = 1
    index = 0
    
    while (front != rear):
        u = queue[front]
        res[0, index] = u
        res[1, index] = pred[u]
        index = index + 1
        front = front + 1
        start = G.s_indptr[u]
        stop  = G.s_indptr[u + 1]
        for v in imap(int, G.s_indices[start:stop]):
            if pred[v] == -1 and v != s:
                pred[v] = u
                queue[rear] = v
                rear = rear + 1
    return res[:, :index]

def traverse_dfs(G, s):
    """
    Returns a sequence of vertices alongwith their predecessors for 
    staticgraph G in a depth-first-search order starting at source s.

    Parameters
    ----------
    G : A directed staticgraph.
    s : Source node to start the dfs traversal.
    
    Returns
    -------
    res :A 2-Dimensional numpy int32 array.
          1st row: A sequence of vertices in BFS traversal starting from s.
          2nd row: The immediate predecessors of the vertices traversed.

    Notes
    ------

    It is mandatory that G be directed.
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
        start = G.s_indptr[u]
        stop  = G.s_indptr[u + 1]
        for v in imap(int, G.s_indices[start:stop]):
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
