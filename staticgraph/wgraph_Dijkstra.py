"""
Module implementing the standard shortest path algorithms for unweighted graphs
"""

from numpy import arange, uint32, zeros, empty, float64, uint8
from itertools import imap
from staticgraph.exceptions import StaticGraphNodeAbsentException
from math import floor

def isEmpty(prior_queue):
    return prior_queue[0] == (2 ** 32) - 1

def min_heapify(heap, weights, i, heap_size):
    left = 2 * i
    right = (2 * i) + 1
    smallest = i
    if left < heap_size and weights[heap[left - 1]] < weights[heap[i - 1]]:
        smallest = left
    if right < heap_size and weights[heap[right - 1]] < weights[heap[i - 1]]:
        smallest = right
        
    if smallest != i:
        heap[i - 1], heap[smallest - 1] = heap[smallest - 1], heap[i - 1]
        min_heapify(heap, weights, smallest, heap_size)

def build_min_heap(p_queue, weights):
    heap_size = p_queue.size
    index = int(floor(p_queue.size / 2))
    for i in range(index, 1):
        min_heapify(p_queue, weights, i, heap_size)

def extract_min_dist(p_queue, weights, heap_size):
    minimum = p_queue[0]
    p_queue[0] = p_queue[heap_size - 1]
    p_queue[heap_size - 1] = (2 ** 32) - 1
    heap_size -= 1
    min_heapify(p_queue, weights, 1, heap_size)
    return minimum

def dijkstra_all(G, s, maxdepth = 2 ** 32 - 1):
    """
    Returns a sequence of vertices alongwith the length of their 
    shortest paths from source node s for an undirected 
    weighted staticgraph G.
    
    This function uses the Dijkstra's algorithm to find 
    single-source shortest paths for the Graph G.
    Parameters
    ----------
    G : An undirected weighted staticgraph.
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
    nodes = arange(order, dtype = uint32)
    weights = empty(order, dtype = float64)
    visited = zeros(order, dtype = uint8)
    weights[:] = 2 ** 32 -1
    weights[s] = 0
    build_min_heap(nodes, weights)
    
    heap_size = order
    while isEmpty(nodes) == False:
        u = extract_min_dist(nodes, weights, heap_size)
        visited[u] = 1
        heap_size -= 1
        for v in G.neighbours(u):
            if visited[v] == 0:
                if weights[v] > (weights[u] + G.weight(u, v)):
                    weights[v] = (weights[u] + G.weight(u, v))
        nodes = arange(order, dtype = uint32)
    sort_indices = weights.argsort()
    weights = weights[sort_indices]
    nodes = nodes[sort_indices]
    return nodes, weights
