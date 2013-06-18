"""
Routines for fast edgelist manipulation.
"""

from numpy import array, zeros, empty, resize, cumsum

def make_deg(n_nodes, edges):
    """
    Create the degree distribution of nodes.
    """

    p_deg = zeros(n_nodes, dtype="u4")
    s_deg = zeros(n_nodes, dtype="u4")
    for u, v in edges:
        if u == v:
            continue
        s_deg[u] += 1
        p_deg[v] += 1
    
    return p_deg, s_deg

def make_comp(n_nodes, n_edges, edges, deg):
    """
    Create the compressed arrays for edgelist.
    """

    p_deg, s_deg = deg
    p_indptr = empty(n_nodes + 1, dtype="u8")
    p_indices = empty(n_edges, dtype="u4")
    s_indptr = empty(n_nodes + 1, dtype="u8")
    s_indices = empty(n_edges, dtype="u4")
    p_indptr[0]  = s_indptr[0] = 0
    p_indptr[1:] = cumsum(p_deg)
    s_indptr[1:] = cumsum(s_deg)
    p_idxs = array(p_indptr[:-1], dtype="u8")
    s_idxs = array(s_indptr[:-1], dtype="u8")
    
    #Creating the edgelist
    for u, v in edges:
        if u == v:
            continue

        s_indices[s_idxs[u]] = v
        s_idxs[u] += 1
        
        p_indices[p_idxs[v]] = u
        p_idxs[v] += 1

    #Sorting the edgelist
    for u in range(n_nodes):
        start = p_indptr[u]
        stop  = p_indptr[u + 1]
        p_indices[start:stop].sort()
        start = s_indptr[u]
        stop  = s_indptr[u + 1]
        s_indices[start:stop].sort()

   # Eliminating parallel edges    

    i, j, del_ctr = 0, 1, 0
    for u in range(n_nodes):
        if(p_indptr[u] == p_indptr[u + 1]):
            continue
        p_indices[i] = p_indices[i + del_ctr]
        stop  = p_indptr[u + 1]
        while j < stop:
            if p_indices[i] == p_indices[j]:
                j += 1
                del_ctr += 1
            else:
                p_indices[i + 1] = p_indices[j]
                i += 1
                j += 1
                
        p_indptr[u + 1] = i + 1
        i += 1
        j += 1
    p_indices = resize(p_indices, p_indptr[-1])
   
    i, j, del_ctr = 0, 1, 0
    for u in range(n_nodes):
        if(s_indptr[u] == s_indptr[u + 1]):
            continue
        s_indices[i] = s_indices[i + del_ctr]
        stop  = s_indptr[u + 1]
        while j < stop:
            if s_indices[i] == s_indices[j]:
                j += 1
                del_ctr += 1
            else:
                s_indices[i + 1] = s_indices[j]
                i += 1
                j += 1
                
        s_indptr[u + 1] = i + 1
        i += 1
        j += 1
    s_indices = resize(s_indices, s_indptr[-1])

    return p_indptr, p_indices, s_indptr, s_indices
