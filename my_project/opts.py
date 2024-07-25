import sys, os, re
from .create_graph import *
from .bow_tie_detection import *
from .pajek import *

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def exe_case_1(G):
    UG = G.to_undirected()
    bowtie_components = get_bowtie_components(G)
    #node_colors = get_node_colors(G, bowtie_components)
    #node_layout = get_bow_tie_layout(bowtie_components)

    create_excel(G, UG, bowtie_components)

    open_pajek(G)

def case_1():
    choice = input("How would you create the network?\n1) By File(.txt or .net)\n2) By giving the total of nodes\n>> ")
    if choice == "1":
        filename = input("Type the file name >> ")
        G = create_graph_file(filename)
        if G is not None:
            exe_case_1(G)
            
    elif choice == "2":
        num = input("Type the number of nodes in the network you want to generate >> ")
        try:
            num = int(num)
            G = create_graph_number(num)
            if G is not None:
                exe_case_1(G)
        except ValueError:
            print("Expected an Integer!")
    else:
        print("Not supported option")

def exe_case_2(G, flag, list_nodes, shock):
    #check if all nodes in list_nodes are in the Graph
    directory = "avalanches"
    trash_files = re.compile(r'^.*\.(xlsx|txt)$')
    for filename in os.listdir(directory):
        if trash_files.match(filename):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
            except:
                pass

    missing_nodes = [node for node in list_nodes if node not in G.nodes]
    if missing_nodes:

        print("Some nodes are not in the Network...Stopped the permutation mode!")
        for n in missing_nodes:
            print(n + "\n")
        return False
    if shock:
        print("Shock ON!")
    else:
        print("Shock OFF!")
    if flag:
        print("Single Avalanche Mode!")
        results = {}
        for node in list_nodes:
            single_avalanche(G, node, results, shock)
        result(G, results)
    else:
        print("Multiple Avalanche Mode!")
        multiple_avalanches(G, list_nodes, shock)

def case_2():

    filename = input("Type the file of the network (.txt or .net)>> ")
    G = create_graph_file(filename)
    if G is None:
        return False
    filename = input("Type the file of the perturbated nodes>> ")
    try:
        list_nodes = []
        file = open(filename, "r")
        flag = file.readline().strip().lower() == 'true'
        shock = file.readline().strip().lower() == 'true'
        for line in file:
            list_nodes.append(line.strip())

        if flag is not None and list_nodes is not None:
            exe_case_2(G, flag, list_nodes, shock)
        else:    
            print(f"Error reading file: \"{filename}\"")
    except:
        print(f"Errore nell'apertura del file \"{filename}\" (controlla che il file esista e che sia formattato correttemente, o che siano presenti i giusti permessi)")


def single_avalanche(G, start_node, results, shock):
    rate = 0.5
    rate_shock = 0.5
    avalanche = set()
    avalanche.add(start_node)
    #we're going to check only the successors of the nodes in the avalanche at every cycle
    nodes_to_check = set(G.successors(start_node))
    if shock:
        nodes_to_check = nodes_to_check.union(G.predecessors(start_node))

    changes = True
    while changes:
        changes = False
        nodes_to_add = set()
        for node in nodes_to_check:
            if node not in avalanche:
                predecessors = list(G.predecessors(node))
                if shock:
                    successors = list(G.successors(node))
                    influenced_successors = [suc for suc in successors if suc in avalanche]
                    if len(successors) > 0 and len(influenced_successors) >= len(successors) * rate_shock:
                        nodes_to_add.add(node)
                influenced_predecessors = [pred for pred in predecessors if pred in avalanche]
                #if the node is not in the avalanche, we check if, for a certain threshold (rate), its predecessors are already in the avalanche, if so then it will be inserted
                if len(predecessors) > 0 and len(influenced_predecessors) >= len(predecessors) * rate:
                    nodes_to_add.add(node)

        if nodes_to_add:
            changes = True
            avalanche.update(nodes_to_add)
            #after adding the nodes in the avalanche, we insert their successors into "nodes_to_check"
            new_nodes_to_check = set()
            for node in nodes_to_add:
                new_nodes_to_check.update(G.successors(node))
                if shock:
                    new_nodes_to_check.update(G.predecessors(node))
            nodes_to_check = new_nodes_to_check

    results[start_node] = avalanche
    filename = str(start_node) + ".txt"
    folder = "avalanches"

    file_path = os.path.join(folder, filename)
    try:

        with open(file_path, "w") as file:
            for n in avalanche:
                file.write(f"{n}\n")
    except:
        print("Error...")



def multiple_avalanches(G, list_nodes, shock):
    rate = 0.5
    rate_shock = 0.5
    avalanche = set(list_nodes)

    nodes_to_check = set()

    if shock:
        for node in avalanche:
            nodes_to_check.update(G.successors(node))
            nodes_to_check = nodes_to_check.union(G.predecessors(node))
    else:
        for node in avalanche:
            nodes_to_check.update(G.successors(node))

    changes = True
    while changes:
        changes = False
        nodes_to_add = set()
        for node in nodes_to_check:
            if node not in avalanche:
                predecessors = list(G.predecessors(node))
                if shock:
                    successors = list(G.successors(node))
                    influenced_successors = [suc for suc in successors if suc in avalanche]
                    if len(successors) > 0 and len(influenced_successors) >= len(successors) * rate_shock:
                        nodes_to_add.add(node)
                influenced_predecessors = [pred for pred in predecessors if pred in avalanche]
                #if the node is not in the avalanche, we check if, for a certain threshold (rate), its predecessors are already in the avalanche, if so then it will be inserted
                if len(predecessors) > 0 and len(influenced_predecessors) >= len(predecessors) * rate:
                    nodes_to_add.add(node)

        if nodes_to_add:
            changes = True
            avalanche.update(nodes_to_add)
            #after adding the nodes in the avalanche, we insert their successors into "nodes_to_check"
            new_nodes_to_check = set()
            for node in nodes_to_add:
                new_nodes_to_check.update(G.successors(node))
                if shock:
                    new_nodes_to_check.update(G.predecessors(node))
            nodes_to_check = new_nodes_to_check

    filename = "multiple_avalanches.txt"
    folder = "avalanches"

    file_path = os.path.join(folder, filename)

    try:
        with open(file_path, "w") as file:
            for n in avalanche:
                file.write(f"{n}\n")
    except:
        print("Error...")



def result(G, results):
    import pandas as pd

    nodes_in_avalanche = {node: 0 for node in G.nodes()} #how many times each node appears in a avalanche
    nodes_power = {node: 0 for node in G.nodes()} #how many nodes have been influenced by each node

    for node, avalanche in results.items():
        nodes_power[node] = len(avalanche)
        for n in avalanche:
            nodes_in_avalanche[n] += 1

    filename = "results.xlsx"
    folder = "avalanches"

    file_path = os.path.join(folder, filename)
    
    data = []

    for node in G.nodes():
        node_data = {
            "ID": node,
            "Prone to avalanches": nodes_in_avalanche[node],
            "Size of its avalanche": nodes_power[node]
        }
        data.append(node_data)
    df = pd.DataFrame(data)
    try:
        df.to_excel(file_path, index = False)
        print(f"Excel created as \"{filename}\"")
    except:
        print("Excel not created due to errors!")


def case_3():
    import os

    filename = input("Type the filename of the Pajek file you'd like to open >> ")

    if filename.endswith(".net"):
        if os.path.isfile(filename):
            view_pajek(filename)
        else:
            print("Not existing file!")

    else:
        print("The file must end with .net ")