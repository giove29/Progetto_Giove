
def get_bow_tie_layout(bowtie_components):
    pos = {}
    x = 0
    y = 0

    # Disposizione dei nodi di S al centro
    for i, node in enumerate(bowtie_components["S"]):
        pos[node] = (x - (0.1 * (i%2)), y + 0.1 * i)
    
    # Disposizione dei nodi di OUT a destra
    for i, node in enumerate(bowtie_components["OUT"]):
        pos[node] = (x + 2 + 0.1 * i, y + 0.1 * i)
    
    # Disposizione dei nodi di IN a sinistra
    for i, node in enumerate(bowtie_components["IN"]):
        pos[node] = (x - 2 - 0.1 * i, y - 0.1 * i)

    # Disposizione degli altri nodi sotto S
    for i, node in enumerate(bowtie_components["TUBES"] | bowtie_components["INTENDRILS"] | bowtie_components["OUTTENDRILS"] | bowtie_components["OTHER"]):
        pos[node] = (x + 1, y - 2 - 0.1 * i)

    return pos