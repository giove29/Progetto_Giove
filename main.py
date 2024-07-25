
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
#%matplotlib inline

from my_project import *

def main():
    while True:
        choice = input("\nNETWORK MENU\n1) Generate a network and its centrality calculations\n2) Perturbation mode\n3) Open a .net file with Pajek\n4) Exit\nSelect an option >> ")
        if choice == "1":
            clear_screen()
            case_1()
            
        elif choice == "2":
            clear_screen()
            case_2()

        elif choice == "3":
            clear_screen()
            case_3()
            
        elif choice == "4":
            clear_screen()
            print("Bye...")
            sys.exit(1)
        else:
            clear_screen()
            print("Not supported option!")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type = str, help="Nome del file da importare per la creazione del grafo")
    parser.add_argument('-n', '--numero', type = int, help='Numero di nodi che compongono il grafo che si vuole creare')

    args = parser.parse_args()
    flag = False


    if  args.file is not None and args.numero is not None:
        print("Inserire una sola opzione alla volta!!")
        sys.exit(1)
    
    if args.file:
        G = create_graph_file(args.file)
        if G is None:
            print("Grafo vuoto!")
            sys.exit(1)
        exe_case_1(G)

    elif args.numero:
        G = create_graph_number(args.numero)
        exe_case_1(G)

    else:
        print("Inserire almeno un argomento posizionale (-f <filename>, -n <numero nodi>)")
        main()
    
