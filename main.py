import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
#%matplotlib inline

from my_project import *

import time 

def time_decorator(function):
    def new_func(*args, **kwargs):
        start = time.time()
        value = function(*args, **kwargs)
        stop = time.time()
        print(f"Execution Time {function.__name__}: {stop-start} secs")
        return value
    return new_func

def main(G):

    ''' Controllo dei parametri 
    if len(sys.argv) != 2:
        print ("Usage: python3 main.py <int arg>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print ("Usage: python3 main.py <int arg>")
        sys.exit(1)
    '''


    ''' Creazione del Grafo Bow-Tie '''
    
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



    pagerank_centrality = nx.pagerank(G)
    print("PageRank Centrality:")
    for node, pc in sorted(pagerank_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {pc}")
    print("\n")


    # misura calcolabile solo attraverso un grafo indiretto e completamento connesso
    try:
        start = time.time()
        betweenness_current_flow = nx.current_flow_betweenness_centrality(UG)
        stop = time.time()
        print(f"Execution Time {nx.current_flow_betweenness_centrality.__name__}: {stop-start} secs")
        print("Betweenness Centrality (Current Flow):")
        for node, bcf in sorted(betweenness_current_flow.items(), key = lambda item: item[1], reverse = True):
            print(f"Node {node}: {bcf}")
        print("\n")
    except:
        print("The Graph do not support the requirements for the Current Flow Betweenness Centrality")

    random_centrality = get_random_walk(G)
    print("Random Walk Betweenness Centrality (ULTIMA VERSIONE):")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")

    random_centrality = get_random_walk_bc(G)
    print("Random Walk Betweenness Centrality (1):")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")

    random_centrality = get_random_walk_bc_prof(G)
    print("Random Walk Betweenness Centrality (2):")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")


    random_centrality = get_random_walk_bc_prof_opt(G)
    print("Random Walk Betweenness Centrality (3):")
    for node, rc in sorted(random_centrality.items(), key = lambda item: item[1], reverse = True):
        print(f"Node {node}: {rc}")
    print("\n")






    ''' Funzioni di Visualizzazione del Grafo '''
    plt.subplot(121)
    nx.draw(G, pos=node_layout, node_color=node_colors, arrowsize=10, with_labels=True, font_color='white')

    plt.scatter(0, 0, label="IN", color='blue')
    plt.scatter(0, 0, label="OUT", color='green')
    plt.scatter(0, 0, label="CORE", color='red')
    plt.scatter(0, 0, label="Tentacoli & Co", color='gray')
    plt.legend()

    #QUESTO CAMBIA DA QUALCHE VERSIONE
    plt.get_current_fig_manager().canvas.setWindowTitle('Bow-tie Structure')

    plt.subplot(122)
    nx.draw(UG, pos=node_layout, node_color=node_colors, arrowsize=10, with_labels=True, font_color='white')
    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type = str, help="Nome del file da importare per la creazione del grafo")
    parser.add_argument('-n', '--numero', type = int, help='Numero di nodi che compongono il grafo che si vuole creare')

    args = parser.parse_args()

    if  args.file is not None and args.numero is not None:
        print("Inserire una sola opzione alla volta!!")
        sys.exit(1)
    
    if args.file:
        G = create_graph_file(args.file)
        if G is None:
            sys.exit(1)

    elif args.numero:
        G = create_graph_number(args.numero)

    else:
        print("Inserire almeno un argomento posizionale (-f <filename>, -n <numero nodi>)")
        sys.exit(1)


    main(G)
    
