def get_bowtie_components(graph):
    '''Classifying the nodes of a network into a bow-tie structure.
    Here we follow the definition of a bow-tie as in: 
    "Bow-tie Decomposition in Directed Graphs" - Yang et al. IEEE (2011) 
    
    input:  NetworkX directed graph or numpy adjacency matrix(not implemented)
    output: sets of nodes in the specified partitions (following the 
            NetworkX input graph node labelling or labelled according to
            the order of the adjacency matrix [0, n-1])
    '''
    import networkx as nx
    
    # Verify graph input format
    #input_formats = [nx.DiGraph, np.ndarray, np.matrix]
    input_formats = [nx.DiGraph]
    assert type(graph) in input_formats, 'Input should be a NetworkX directed graph'
    if type(graph) == nx.classes.digraph.DiGraph:
        G = graph.copy()
    #if (type(graph) == np.ndarray) | (type(graph) == np.matrix):  #in case of a numpy adjacency matrix
        #G = nx.from_numpy_matrix(np.matrix(graph), create_using=nx.DiGraph())
    
    GT = nx.reverse(G, copy=True)
    
    strongly_con_comp = list(nx.strongly_connected_components(G))    
    strongly_con_comp = max(strongly_con_comp, key=len)

    S = strongly_con_comp

    v_any = list(S)[0]
    DFS_G = set(nx.dfs_tree(G,v_any).nodes())
    DFS_GT = set(nx.dfs_tree(GT,v_any).nodes())
    OUT = DFS_G - S
    IN = DFS_GT - S
    V_rest = set(G.nodes()) - S - OUT - IN

    TUBES = set()
    INTENDRILS = set()
    OUTTENDRILS = set()
    OTHER = set()
    for v in V_rest:
        irv = len(IN & set(nx.dfs_tree(GT,v).nodes())) != 0 # "True" se esiste almeno un nodo in comune tra l'insieme "IN" e il sottoalbero di "GT" radicato dal nodo "v"
        vro = len(OUT & set(nx.dfs_tree(G,v).nodes())) != 0
        if irv and vro:
            TUBES.add(v)
        elif irv and not vro:
            INTENDRILS.add(v)
        elif not irv and vro:
            OUTTENDRILS.add(v)
        elif not irv and not vro:
            OTHER.add(v)
            
    return {"S": S, "IN": IN, "OUT": OUT, "TUBES": TUBES, "INTENDRILS": INTENDRILS, "OUTTENDRILS": OUTTENDRILS, "OTHER": OTHER}