
def open_pajek(G):
    import networkx as nx

    nx.write_pajek(G, "network.net")
    
    view_pajek("network.net")


def view_pajek(filename):
    import subprocess, sys

    try:
        pajek_exe = "my_project/pajek/Pajek/Pajek.exe"
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