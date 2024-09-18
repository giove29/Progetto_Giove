import sys, os, re
from .create_graph import *
from .bow_tie_detection import *
from .pajek import *
import random

PERCENTAGE_PROB_AVALANCHE = 1
RATE = 1
RATE_SHOCK = 0.5

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def bowtie_to_partitions(bowtie_components):
    partitions = {}
    for section, nodes in bowtie_components.items():
        if section == "S":
            for node in nodes:
                partitions[node] = 1
        elif section == "IN":
            for node in nodes:
                partitions[node] = 2
        elif section == "OUT":
            for node in nodes:
                partitions[node] = 3
        else:
            for node in nodes:
                partitions[node] = 4

    return partitions

def results_to_avalanche(results):
    avalanche = set()
    for node, a in results.items():
        avalanche.update(a)

    return avalanche

def avalanche_to_partitions(G, avalanche):
    partitions = {}
    for node in G.nodes():
        if node in avalanche:
            partitions[node] = 2
        else:
            partitions[node] = 1
    
    return partitions

def prob_avalanche(G, output_file="prob_avalanche.txt", percentage=PERCENTAGE_PROB_AVALANCHE):
    all_nodes = list(G.nodes)
    num_nodes_to_select = int(len(all_nodes) * percentage)
    selected_nodes = random.sample(all_nodes, num_nodes_to_select)

    with open(output_file, "w") as outfile:
        outfile.write("True\nFalse\n")
        for node in selected_nodes:
            outfile.write(f"{node}\n")
        
    print("A possible avalanche has been generated into \"prob_avalanche.txt\" file ")



def exe_case_1(G):
    UG = G.to_undirected()
    bowtie_components = get_bowtie_components(G)
    #node_colors = get_node_colors(G, bowtie_components)
    #node_layout = get_bow_tie_layout(bowtie_components)

    create_excel(G, UG, bowtie_components)

    partitions = bowtie_to_partitions(bowtie_components)

    partitions_file = "partitions.clu"

    create_pajek_partitions_file(partitions_file, G, partitions)

    open_pajek(G, partitions_file)

    prob_avalanche(G)

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
    avalanche = set()
    if flag:
        print("Single Avalanche Mode!")
        results = {}
        for node in list_nodes:
            single_avalanche(G, node, results, shock)
        result(G, results)
        avalanche = results_to_avalanche(results)
        
    else:
        print("Multiple Avalanche Mode!")
        avalanche = multiple_avalanches(G, list_nodes, shock)

    partitions = avalanche_to_partitions(G, avalanche)

    partitions_file = "partitions_avalanche.clu"

    create_pajek_partitions_file(partitions_file, G, partitions)

    open_pajek(G, partitions_file)

def case_2():

    filename_graph = input("Type the file of the network (.txt or .net)>> ")
    G = create_graph_file(filename_graph)
    if G is None:
        return False
    filename = input("Type the file of the perturbated nodes>> ")
    try:
        list_nodes = []
        file = open(filename, "r")
        flag = file.readline().strip().lower() == 'true' #First bool -> True: Single; False: Multiple
        shock = file.readline().strip().lower() == 'true' #Second bool -> True: Shock ON; False: Shock OFF
        for line in file:
            cleaned_line = line.rstrip('\n')
            list_nodes.append(str(cleaned_line))

        if flag is not None and list_nodes is not None:
            exe_case_2(G, flag, list_nodes, shock)
        else:    
            print(f"Error reading file: \"{filename}\"")
    except Exception as e:
        print(f"Errore nell'apertura del file \"{filename}\" (controlla che il file esista e che sia formattato correttemente, o che siano presenti i giusti permessi)\n", e)


def single_avalanche(G, start_node, results, shock):
    rate = RATE
    rate_shock = RATE_SHOCK
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
    ''' Creates a file of the avalanche of each node
    node_edited = str(start_node).replace("/", "")
    filename = str(node_edited) + ".txt"
    folder = "avalanches"

    file_path = os.path.join(folder, filename)
    try:

        with open(file_path, "w") as file:
            for n in avalanche:
                file.write(f"{n}\n")
    except ValueError as e:
        print(f"Error: {e}")
    '''

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
    except ValueError as e:
        print(f"Error: {e}")

    return avalanche

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
    except Exception as e:
        print("Excel not created due to errors!\n" + str(e))


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


def exe_case_4(G):
    bowtie_components = get_bowtie_components(G)
    
    partitions = bowtie_to_partitions(bowtie_components)

    partitions_file = "partitions.clu"

    create_pajek_partitions_file(partitions_file, G, partitions)

    open_pajek(G, partitions_file)

    prob_avalanche(G)

def case_4():
    choice = input("How would you create the network?\n1) By File(.txt or .net)\n2) By giving the total of nodes\n>> ")
    if choice == "1":
        filename = input("Type the file name >> ")
        G = create_graph_file(filename)
        if G is not None:
            exe_case_4(G)
            
    elif choice == "2":
        num = input("Type the number of nodes in the network you want to generate >> ")
        try:
            num = int(num)
            G = create_graph_number(num)
            if G is not None:
                exe_case_4(G)
        except ValueError:
            print("Expected an Integer!")
    else:
        print("Not supported option")