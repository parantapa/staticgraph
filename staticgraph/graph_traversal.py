"""
Module implementing the standard traversal techniques for an undirected graph
"""

from numpy import uint32, zeros, empty
from itertools import imap
from staticgraph.exceptions import StaticGraphNodeAbsentException

def bfs_all(G, s, maxdepth = (2 ** 32) - 1):
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
    bfs_indices = empty(order, dtype = uint32)
    bfs_indptr = empty(order, dtype = uint32)
    bfs_indptr[:] = (2 ** 32) - 1
    front = rear = 0
    queue[rear] = s
    dist[s] = 0
    bfs_indptr[0] = 0
    rear = 1
    index = 0
    depth = 0
    
    while (front != rear):
        u = queue[front]
        if bfs_indptr[dist[u]] == (2 ** 32) - 1:
             bfs_indptr[dist[u]] = index
             depth += 1
             if depth > maxdepth:
                 break
        bfs_indices[index] = u
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

def bfs_search(G, s, t, maxdepth = (2 ** 32) - 1):
    """
    Returns the path from source to target in BFS
    
    Parameters
    ----------
    G        : An undirected staticgraph.
    s        : Source node to start the BFS.
    t        : Target node to start the BFS.
    maxdepth : Optional parameter denoting the maximum depth for BFS.
    
    Returns
    -------
    path : A numpy uint32 array returning a sequence of vertices in 
           BFS from s to t.
              
    Notes
    ------

    It is mandatory that G be undirected.
    Returns None on failure to find target node.
    """

    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    if t >= G.order():
        raise StaticGraphNodeAbsentException("target node absent in graph!!")
    
    order = G.order()
    path = empty(order , dtype = uint32)
    path[:] = (2 ** 32) - 1
    pred = empty(order , dtype = uint32)
    pred[:] = (2 ** 32) - 1
    queue = empty(order, dtype = uint32)
    front = rear = 0
    queue[rear] = s
    rear = 1
    depth = path[s] = 0

    while front != rear and pred[t] == (2 ** 32) - 1 and depth < maxdepth:
        u = queue[front]
        front += 1
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if pred[v] == (2 ** 32) - 1:
                pred[v] = u
                path[v] = path[u] + 1
                if depth < path[v]:
                    depth += 1
                queue[rear] = v
                rear = rear + 1
            if v == t:
                break
    
    if pred[t] == (2 ** 32) - 1:
        return None
    
    u = t
    index = 0
    while u != s:
        path[index] = u
        index += 1
        u = pred[u]
    path[index] = s
    
    return path[index::-1]

def dfs_search(G, s, t, maxdepth = (2 ** 32) - 1):
    """
    Returns the path from source to target in DFS
    
    Parameters
    ----------
    G        : An undirected staticgraph.
    s        : Source node to start the DFS.
    t        : Target node to start the DFS.
    maxdepth : Optional parameter denoting the maximum depth for DFS.
    
    Returns
    -------
    path : A numpy uint32 array returning a sequence of vertices in 
           DFS from s to t.
              
    Notes
    ------

    It is mandatory that G be undirected.
    Returns None on failure to find target node.
    """

    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")
    if t >= G.order():
        raise StaticGraphNodeAbsentException("target node absent in graph!!")
    
    order = G.order()
    path = empty(order , dtype = uint32)
    path[:] = (2 ** 32) - 1
    pred = empty(order , dtype = uint32)
    pred[:] = (2 ** 32) - 1
    stack = empty(order, dtype = uint32)
    top = 0
    stack[top] = s
    path[s] = 0
    flag = 0

    while top >= 0:
        if flag == 1:
            break
        u = stack[top]
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if pred[v] == (2 ** 32) - 1:
                pred[v] = u
                path[v] = path[u] + 1
                if path[v] >= maxdepth:
                    break
                if v == t:
                    flag = 1
                    break
                top = top + 1
                stack[top] = v
                break
        else:
            top -= 1

    if pred[t] == (2 ** 32) - 1:
        return None
        
    u = t
    index = 0
    while u != s:
        path[index] = u
        index += 1
        u = pred[u]
    path[index] = s
    
    return path[index::-1]
