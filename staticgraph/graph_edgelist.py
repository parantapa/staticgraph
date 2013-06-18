"""
Routines for fast edgelist manipulation.
"""

from numpy import array, zeros, empty, resize, cumsum

def make_deg(n_nodes, edges):
    """
    Create the degree distribution of nodes.
    """

    deg = zeros(n_nodes, dtype="u4")
    
    for u, v in edges:
        if u == v:
            continue
        deg[u] += 1
        deg[v] += 1
    
    return deg

def make_comp(n_nodes, n_edges, edges, deg):
    """
    Create the compressed arrays for edgelist.
    """

    indptr = empty(n_nodes + 1, dtype="u8")
    indices = empty(2 * n_edges, dtype="u4")

    indptr[0]  = 0
    indptr[1:] = cumsum(deg)
    idxs = array(indptr[:-1], dtype="u8")
    
    #Creating the edgelist
    for u, v in edges:
        if u == v:
            continue

        indices[idxs[u]] = v
        idxs[u] += 1
        
        indices[idxs[v]] = u
        idxs[v] += 1

    #Sorting the edgelist
    for u in range(n_nodes):
        start = indptr[u]
        stop  = indptr[u + 1]
        indices[start:stop].sort()
    
    # Eliminating parallel edges

    i, j, del_ctr = 0, 1, 0  
    for u in range(n_nodes):
        if(indptr[u] == indptr[u + 1]):
            continue
        indices[i] = indices[i + del_ctr]
        stop  = indptr[u + 1]
        while j < stop:
            if indices[i] == indices[j]:
                j += 1
                del_ctr += 1
            else:
                indices[i + 1] = indices[j]
                i += 1
                j += 1
                
        indptr[u + 1] = i + 1
        i += 1
        j += 1
    indices = resize(indices, indptr[-1])
    return indptr, indices
