def create_graph_number(n):
    import networkx as nx
    G = nx.DiGraph(nx.scale_free_graph(n)) #nx.scale_free_graph(n, seed=14) for a controlled random generator
    return G

def create_graph_file(filename):
    import networkx as nx
    if filename.lower().endswith(".net"):
        try:
            G = nx.read_pajek(filename)
            G = nx.DiGraph(G)
            return G
        except:
            print(f"Errore nell'apertura del file \"{filename}\" (controlla che il file esista o che siano presenti i giusti permessi)")
            return None
    else:
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

        except Exception:
            print(f"Errore nell'apertura del file \"{filename}\" (controlla che il file esista e che sia formattato correttemente, o che siano presenti i giusti permessi)")
            return None
    
def create_excel(G, UG, bowtie_components):
    from .random_walk_betweenness_centrality import get_random_walk
    import pandas as pd
    import networkx as nx
    data = []
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    pagerank_centrality = nx.pagerank(G)
    try:
        betweenness_current_flow = nx.current_flow_betweenness_centrality(UG)
    except:
        betweenness_current_flow = {node: 0 for node in G.nodes()}
    random_centrality = get_random_walk(G)
    for section, nodes in bowtie_components.items():
        for node in nodes:
            node_data = {
                "ID": node,
                "Number of predecessors": G.in_degree(node),
                "Number of successors": G.out_degree(node),
                "Bow-Tie Section": section,
                "Degree Centrality": degree_centrality[node],
                "Closeness Centrality": closeness_centrality[node],
                "Betweenness Centrality": betweenness_centrality[node],
                "PageRank Centrality": pagerank_centrality[node],
                "CurrentFlow Centrality": betweenness_current_flow[node],
                "RandomWalk Centrality": random_centrality[node]
            }
            data.append(node_data)
    df = pd.DataFrame(data)
    try:
        df.to_excel("network.xlsx", index = False)
        print("Excel created as \"network.xlsx\"")
    except:
        print("Excel not created due to errors!")