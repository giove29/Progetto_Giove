
def open_pajek(G, partitions_file = None):
    import networkx as nx
    import os

    if partitions_file and (not partitions_file.endswith(".clu") or not os.path.isfile(partitions_file)):
        print("Error in the passed partitions file")
        return False
    
    nx.write_pajek(G, "network.net")
    if partitions_file:
        view_pajek("network.net", partitions_file)
    else:
        view_pajek("network.net")


def view_pajek(filename, partitions_file = None):
    import subprocess, sys, os

    if partitions_file and (not partitions_file.endswith(".clu") or not os.path.isfile(partitions_file)):
        print("Error in the passed partitions file")
        return False
    
    try:
        pajek_exe = "my_project/pajek/Pajek/Pajek.exe"
        if partitions_file:
            subprocess.run([pajek_exe, filename, partitions_file])
        else:
            subprocess.run([pajek_exe, filename])
        print(f"Network graph saved as \"{filename}\"")
        clean_pajek_logs()
    except:
        print("Errore nell'apertura di Pajek!")
        sys.exit(1)


def clean_pajek_logs():
    import os, re
    directory = os.getcwd()
    trash_files = re.compile(r'^.*\.(ini|rep|log)$')
    for filename in os.listdir(directory):
        if trash_files.match(filename):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
            except:
                pass


def create_pajek_partitions_file(filename, G, partitions):
    if filename.endswith(".clu"):
        with open(filename, "w") as f:
            f.write(f"*Vertices {len(G)}\n")
            for node in G.nodes():
                f.write(f"{partitions[node]}\n")
    else:
        print("File must end with .clu")
