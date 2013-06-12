"""
Module implementing the standard traversal techniques for an undirected graph
"""

from numpy import arange, int32, zeros
from itertools import imap

def traverse_bfs(G, s):
    """
    Return a sequence of vertices of undirected staticgraph G 
    in a breadth-first-search order starting at source s.
    """

    order = G.order()
    nodes = arange((order * 2), dtype = int32)
    nodes[order : order * 2] = 0
    nodes = nodes.reshape(2, order)
    
    queue = zeros((order), dtype = int32)
    res = zeros((order), dtype = int32)
    
    front = rear = 0
    queue[rear] = s
    rear = 1
    nodes[1, s] = 1
    index = 0
    
    while (front != rear):
        u = queue[front]
        front = front + 1
        res[index] = u
        index = index + 1
        start = G.n_indptr[u]
        stop  = G.n_indptr[u + 1]
        for v in imap(int, G.n_indices[start:stop]):
            if nodes[1, v] == 0:
                nodes[1, v] = 1
                queue[rear] = v
                rear = rear + 1
    return res
