
def get_node_colors(G, bowtie_components):
    node_colors = []
    for i, node in enumerate(G.nodes):
        if node in bowtie_components["IN"]:
            node_colors.append('blue')
        elif node in bowtie_components["S"]:
            node_colors.append('red')
        elif node in bowtie_components["OUT"]:
            node_colors.append('green')
        else:
            node_colors.append('grey')
    return node_colors