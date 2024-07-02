import sys
import networkx as nx
import matplotlib.pyplot as plt
#%matplotlib inline

from my_project import *

def main():

    ''' Controllo dei parametri '''
    if len(sys.argv) != 2:
        print ("Usage: python3 main.py <int arg>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print ("Usage: python3 main.py <int arg>")
        sys.exit(1)


    ''' Creazione del Grafo Bow-Tie '''
    G = nx.DiGraph(nx.scale_free_graph(n)) #nx.scale_free_graph(n, seed=14) for a controlled random generator
    UG = G.to_undirected()
    bowtie_components = get_bowtie_components(G)
    node_colors = get_node_colors(G, bowtie_components)
    node_layout = get_bow_tie_layout(bowtie_components)

    
    ''' Calcolo delle Centralità '''
    degree_centrality = nx.degree_centrality(G)
    print("Degree Centrality:")
    for node, dc in sorted(degree_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {dc}")
    print("\n")

    closeness_centrality = nx.closeness_centrality(G)
    print("Closeness Centrality:")
    for node, cc in sorted(closeness_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {cc}")
    print("\n")

    betweenness_centrality = nx.betweenness_centrality(G) # attributo per il peso sugli archi weight='weight'
    print("Betweenness Centrality (Standard):")
    for node, bc in sorted(betweenness_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {bc}")
    print("\n")

    random_centrality = get_random_walk_bc(G)
    print("Random Walk Betweenness Centrality:")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")

    random_centrality = get_random_walk_bc_prof(G)
    print("Random Walk Betweenness Centrality (PROF):")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")

    '''
    random_centrality = get_random_walk_bc_prof_opt(G)
    print("Random Walk Betweenness Centrality (PROF OPTIMIZED):")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")
    '''

    # misura calcolabile solo attraverso un grafo indiretto e completamento connesso
    try:
        betweenness_current_flow = nx.current_flow_betweenness_centrality(UG)
        print("Betweenness Centrality (Current Flow):")
        for node, bcf in sorted(betweenness_current_flow.items(), key = lambda item: item[1], reverse = True):
            print(f"Node {node}: {bcf}")
        print("\n")
    except:
            print("The Graph do not support the requirements for the Current Flow Betweenness Centrality")
    
    pagerank_centrality = nx.pagerank(G)
    print("PageRank Centrality:")
    for node, pc in sorted(pagerank_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {pc}")
    print("\n")





    ''' Funzioni di Visualizzazione del Grafo '''
    plt.subplot(121)
    nx.draw(G, pos=node_layout, node_color=node_colors, arrowsize=10, with_labels=True, font_color='white')

    plt.scatter(0, 0, label="IN", color='blue')
    plt.scatter(0, 0, label="OUT", color='green')
    plt.scatter(0, 0, label="CORE", color='red')
    plt.scatter(0, 0, label="Tentacoli & Co", color='gray')
    plt.legend()

    plt.get_current_fig_manager().canvas.set_window_title('Bow-tie Structure')

    plt.subplot(122)
    nx.draw(UG, pos=node_layout, node_color=node_colors, arrowsize=10, with_labels=True, font_color='white')
    
    plt.show()

if __name__ == "__main__":
    main()
    
