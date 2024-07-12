import time 

def time_decorator(function):
    def new_func(*args, **kwargs):
        start = time.time()
        value = function(*args, **kwargs)
        stop = time.time()
        print(f"Execution Time {function.__name__}: {stop-start} secs")
        return value
    return new_func

@time_decorator
def get_random_walk_bc(graph):
    import networkx as nx
    import random

    input_formats = [nx.DiGraph]
    assert type(graph) in input_formats, 'Input should be a NetworkX directed graph'
    if type(graph) == nx.classes.digraph.DiGraph:
        G = graph.copy()

    rw_betweenness = {node: 0 for node in G.nodes()}
    
    num_walks = G.number_of_nodes() * 500
    walk_length = G.number_of_edges() * 500
    i = 0

    for walk_num in range(num_walks):
        current_node = random.choice(list(G.nodes()))

        for step_num in range(walk_length):
            successors = list(G.successors(current_node))
            if not successors:
                break
            else:
                next_node = random.choice(successors)
                rw_betweenness[current_node] += 1
            i+=1
            current_node = next_node
    
    for node in rw_betweenness:
        rw_betweenness[node] /= (i) # (Normalization) -> how many times it has passed by / totals passages from a node to another 
    
    return rw_betweenness

@time_decorator
def get_random_walk_bc_prof(graph):
    import networkx as nx
    import random

    input_formats = [nx.DiGraph]
    assert type(graph) in input_formats, 'Input should be a NetworkX directed graph'
    if type(graph) == nx.classes.digraph.DiGraph:
        G = graph.copy()

    rw_betweenness = {node: 0 for node in G.nodes()}
    entry_nodes = {node: False for node in G.nodes()}
    
    num_walks = G.number_of_nodes() * 50
    walk_length = G.number_of_edges() * 500
    i = 0

    for walk_num in range(num_walks):
        current_node = random.choice(list(G.nodes()))
        entry_nodes[current_node] = True

        for step_num in range(walk_length):
            successors = list(G.successors(current_node))
            if not successors:
                next_node = get_a_new_node(G, current_node, entry_nodes)
                if next_node is None:
                    break
            else:
                next_node = random.choice(successors)
                rw_betweenness[current_node] += 1
            i+=1
            current_node = next_node
    
    for node in rw_betweenness:
        rw_betweenness[node] /= (i) # (Normalization) -> how many times it has passed by / totals passages from a node to another 
    
    return rw_betweenness

@time_decorator
def get_random_walk_bc_prof_opt(graph):
    import networkx as nx
    import random

    input_formats = [nx.DiGraph]
    assert type(graph) in input_formats, 'Input should be a NetworkX directed graph'
    if type(graph) == nx.classes.digraph.DiGraph:
        G = graph.copy()

    rw_betweenness = {node: 0 for node in G.nodes()}
    
    num_walks = G.number_of_nodes() * 50
    walk_length = G.number_of_edges() * 500
    i = 0

    for walk_num in range(num_walks):
        current_node = random.choice(list(G.nodes()))

        for step_num in range(walk_length):
            successors = list(G.successors(current_node))
            if not successors:
                next_node = get_a_new_node_opt(G, current_node)
                if next_node is None:
                    break
            else:
                next_node = random.choice(successors)
                rw_betweenness[current_node] += 1
            i+=1
            current_node = next_node
    
    for node in rw_betweenness:
        rw_betweenness[node] /= (i) # (Normalization) -> how many times it has passed by / totals passages from a node to another 
    
    return rw_betweenness

@time_decorator
def get_random_walk(graph):
    import networkx as nx
    import random, itertools

    assert isinstance(graph, nx.DiGraph), 'Input should be a NetworkX directed graph'

    G = graph.copy()

    rw_betweenness = {node: 0 for node in G.nodes()}

    nodes = list(G.nodes)
    all_combinations = [(u, v) for u, v in itertools.product(nodes, repeat=2) if u != v and nx.has_path(G, u, v)] #elimina direttamente le coppie con nodi uguali e che non sono collegati nel grafo

    for start, end in all_combinations:
        queue = []
        visited = []
        next_node = random.choice(list(G.successors(start)))
        queue.append(next_node)
        path = [(start, next_node)]
        walk_length = G.number_of_edges() * 500
        while(True):
            node = queue.pop()
            if node == end:
                break

            if len(list(G.successors(node))) > 0 and len(path) < walk_length:
                next_node = random.choice(list(G.successors(node)))
                visited.append(node)
                path = path + [(node, next_node)]
                queue.append(next_node)
                    
            else:
                next_node = random.choice(list(G.successors(start)))
                path = [(start, next_node)]
                visited = []
                queue.append(next_node)

        for v in set(visited):
            rw_betweenness[v] += 1
        
    count = sum(rw_betweenness.values())

    for node in rw_betweenness:
        rw_betweenness[node] /= (count)

    return rw_betweenness

# returns a new node different from the passed one, with at least one predecessor and not already randomly accessed
def get_a_new_node(G, current_node, entry_nodes):
    import random
    num_walks = G.number_of_nodes()

    if all(entry_nodes.values()):
        return None

    for i in range(num_walks):
        new_node = random.choice(list(G.nodes()))
        if new_node != current_node and not entry_nodes[new_node] and list(G.predecessors(new_node)):
            entry_nodes[new_node] = True
            return new_node
    return None

# returns a new node different from the passed one and with at least one predecessor
def get_a_new_node_opt(G, current_node):
    import random
    num_walks = G.number_of_nodes()

    while True:
        new_node = random.choice(list(G.nodes()))
        if new_node != current_node and list(G.predecessors(new_node)):
            return new_node