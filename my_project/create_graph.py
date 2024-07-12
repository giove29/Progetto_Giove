def create_graph_number(n):
    import networkx as nx
    G = nx.DiGraph(nx.scale_free_graph(n)) #nx.scale_free_graph(n, seed=14) for a controlled random generator
    return G

def create_graph_file(filename):
    import networkx as nx
    try:
        G = nx.DiGraph()
        file = open(filename, "r")
        next(file)
        for line in file:
            line = line.strip().split(";")
            from_node = line[1].strip()
            to_node = line[2].strip()
            G.add_edge(from_node, to_node)
        file.close()
        return G

    except IOError:
        print(f"Errore nell'apertura del file \"{filename}\" (controlla che il file esista o che siano presenti i giusti permessi)")
        return None
    