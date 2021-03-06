"""
Module implementing the Dijkstra shortest path algorithm for weighted graphs
"""

from numpy import arange, uint32, zeros, empty, float64, uint8
from staticgraph.exceptions import StaticGraphNodeAbsentException

def isEmpty(prior_queue):
    """
    Returns whether the priority queue is empty or not.
    """

    return prior_queue[0] == (2 ** 32) - 1

def min_heapify(heap, weights, i, heap_size):
    """
    Module that maintains heap property of the heap.
    """

    left = (2 * i) + 1
    right = (2 * i) + 2
    smallest = i
    if left < heap_size and weights[heap[left]] < weights[heap[i]]:
        smallest = left
    if right < heap_size and weights[heap[right]] < weights[heap[smallest]]:
        smallest = right
        
    if smallest != i:

        #exchanging the values in the heap
        heap[i], heap[smallest] = heap[smallest], heap[i]
        min_heapify(heap, weights, smallest, heap_size)

def build_min_heap(p_queue, heap_size, weights):
    """
    Module to create a heap from an unsorted array p_queue
    according to the corresponding values of weights.
    """

    for i in range(heap_size // 2, -1, -1):
        min_heapify(p_queue, weights, i, heap_size)

def extract_min_dist(p_queue, weights, heap_size):
    """
    Module to extract the minimum element from the heap
    """

    minimum = p_queue[0]
    p_queue[0] = p_queue[heap_size - 1]
    p_queue[heap_size - 1] = (2 ** 32) - 1
    heap_size -= 1
    
    #Restoring heap property
    min_heapify(p_queue, weights, 0, heap_size)
    return minimum

def dijkstra_all(G, s, directed = False):
    """
    Returns a sequence of vertices alongwith the length of their 
    shortest paths from source node s for a weighted staticgraph G.
    
    This function uses the Dijkstra's algorithm to find 
    single-source shortest paths for the Graph G.

    Parameters
    ----------
    G : An undirected weighted staticgraph.
    s : Source node.
    
    Returns
    -------
    path : 2 numpy arrays.

           nodes : A numpy uint32 array containing the sequence of vertices 
                   sorted according to distance from the source.

           weights : A numpy float64 array containing the corresponding 
                     cumulative weights in the shortest path from the source.
    
    
    Notes
    ------

    weights[i] = (2 ** 64) : implies that the node i is unreachable from the source.
    directed must be set to True for directed graphs.
    """
    
    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")

    order = G.order()
    nodes = arange(order, dtype = uint32)
    weights = empty(order, dtype = float64)
    visited = zeros(order, dtype = uint8)
    weights[:] = (2 ** 64) -1
    weights[s] = 0
    heap_size = order
    build_min_heap(nodes, heap_size, weights)

    while isEmpty(nodes) == False:
        u = extract_min_dist(nodes, weights, heap_size)
        visited[u] = 1
        heap_size -= 1

        #if graph is undirected
        if directed == False:    
            for v in G.neighbours(u):
                if visited[v] == 0:
                    if weights[v] > (weights[u] + G.weight(u, v)):
                        weights[v] = (weights[u] + G.weight(u, v))
                    
        #if graph is directed
        else:
             for v in G.successors(u):
                 if visited[v] == 0:
                     if weights[v] > (weights[u] + G.weight(u, v)):
                         weights[v] = (weights[u] + G.weight(u, v))
        
        build_min_heap(nodes, heap_size, weights)

    nodes = arange(order, dtype = uint32)
    sort_indices = weights.argsort()
    weights = weights[sort_indices]
    nodes = nodes[sort_indices]
    return nodes, weights

def dijkstra_search(G, s, t, directed = False):
    """
    Returns a sequence of vertices source node s to target node t for a 
    weighted staticgraph G.
    
    This function uses the Dijkstra's algorithm to find 
    single-source shortest paths for the Graph G from s to t.

    Parameters
    ----------
    G : An undirected weighted staticgraph.
    s : Source node.
    t : Target node
    
    Returns
    -------
    nodes : 2 numpy arrays.

           nodes : A numpy uint32 array containing the sequence of vertices 
                   in dijkstra's algorithm from the source to target

           distance : The distance from s to t.
    
    
    Notes
    ------

    returns None if target is unreachable from source.
    directed keyword must be set to True for directed graphs.
    """
    
    if s >= G.order():
        raise StaticGraphNodeAbsentException("source node absent in graph!!")

    order = G.order()
    nodes = arange(order, dtype = uint32)
    weights = empty(order, dtype = float64)
    visited = zeros(order, dtype = uint8)
    pred = empty(order, dtype = uint32)
    pred[:] = (2 ** 32) - 1
    weights[:] = (2 ** 64) -1
    weights[s] = 0
    heap_size = order
    build_min_heap(nodes, heap_size, weights)
    flag = 0

    while isEmpty(nodes) == False:
        u = extract_min_dist(nodes, weights, heap_size)
        if u == t:
            flag = 1
            break
        visited[u] = 1
        heap_size -= 1

        #if graph is undirected
        if directed == False:    
            for v in G.neighbours(u):
                if visited[v] == 0:
                    if weights[v] > (weights[u] + G.weight(u, v)):
                        weights[v] = (weights[u] + G.weight(u, v))
                        pred[v] = u
       
                    
        #if graph is directed
        else:
             for v in G.successors(u):
                 if visited[v] == 0:
                     if weights[v] > (weights[u] + G.weight(u, v)):
                         weights[v] = (weights[u] + G.weight(u, v))
                         pred[v] = u

        build_min_heap(nodes, heap_size, weights)

    if flag == 0:
        return None, None

    u = t
    index = 0
    while u != s:
        nodes[index] = u
        index += 1
        u = pred[u]
    nodes[index] = s

    distance = weights[t]
    return nodes[index::-1], distance
