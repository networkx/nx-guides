import numpy as np
import networkx as nx
from spektral.datasets import TUDataset
import matplotlib.pyplot as plt
import timeit
import pandas as pd


def tud_to_networkx(ds_name):
    pre = ds_name + "/"
    
    with open("datasets/" +   ds_name + "_graph_indicator.txt", "r") as f:
        graph_indicator = [int(i) - 1 for i in list(f)]
    f.closed

    # Nodes.
    num_graphs = max(graph_indicator)
    node_indices = []
    offset = []
    c = 0

    for i in range(num_graphs + 1):
        offset.append(c)
        c_i = graph_indicator.count(i)
        node_indices.append((c, c + c_i - 1))
        c += c_i

    graph_db = []
    for i in node_indices:
        g = nx.Graph()
        for j in range(i[1] - i[0]+1):
            g.add_node(j)

        graph_db.append(g)

    # Edges.
    with open("datasets/" +  ds_name + "_A.txt", "r") as f:
        edges = [i.split(',') for i in list(f)]
    f.closed

    edges = [(int(e[0].strip()) - 1, int(e[1].strip()) - 1) for e in edges]
    edge_list = []
    edgeb_list = []
    for e in edges:
        g_id = graph_indicator[e[0]]
        g = graph_db[g_id]
        off = offset[g_id]

        # Avoid multigraph (for edge_list)
        if ((e[0] - off, e[1] - off) not in list(g.edges())) and ((e[1] - off, e[0] - off) not in list(g.edges())):
            g.add_edge(e[0] - off, e[1] - off)
            edge_list.append((e[0] - off, e[1] - off))
            edgeb_list.append(True)
        else:
            edgeb_list.append(False)

    # Node labels.
    with open("datasets/" +  ds_name + "_node_labels.txt", "r") as f:
        node_labels = [str.strip(i) for i in list(f)]
    f.closed

    node_labels = [i.split(',') for i in node_labels]
    int_labels = [];
    for i in range(len(node_labels)):
        int_labels.append([int(j) for j in node_labels[i]])

    i = 0
    for g in graph_db:
        for v in range(g.number_of_nodes()):
            g.nodes[v]['labels'] = int_labels[i]
            i += 1

    # Node Attributes.
    with open("datasets/" +  ds_name + "_node_attributes.txt", "r") as f:
        node_attributes = [str.strip(i) for i in list(f)]
    f.closed

    node_attributes = [i.split(',') for i in node_attributes]
    float_attributes = [];
    for i in range(len(node_attributes)):
        float_attributes.append([float(j) for j in node_attributes[i]])
    i = 0
    for g in graph_db:
        for v in range(g.number_of_nodes()):
            g.nodes[v]['attributes'] = float_attributes[i]
            i += 1

    # Classes.
    with open("datasets/" +  ds_name + "_graph_labels.txt", "r") as f:
        classes = [str.strip(i) for i in list(f)]
    f.closed
    classes = [i.split(',') for i in classes]
    cs = [];
    for i in range(len(classes)):
        cs.append([int(j) for j in classes[i]])

    i = 0
    for g in graph_db:
        g.graph['classes'] = cs[i]
        i += 1

    return graph_db

def main():
    n = int(input("How many graphs do you want to test?"))
    reps = int(input("Enter the number of repetitions"))

    dataset = 'PROTEINS'
    data = TUDataset(dataset) #Load Dataset 
    graph_db = tud_to_networkx(dataset) #NetworkX Data
    
    #Sort graphs by size 
    graph_sizes = [len(graph_db[i].nodes) for i in range(0, len(graph_db))]
    sizes_sorted = np.sort(graph_sizes)
    
    order = np.argsort(graph_sizes)
    graph_db_sorted = np.array(graph_db, dtype=object)[order]

    #Measure time execution of VF2 and VF2++
    vf2_all_times_graphs = []  # VF2 time measurements on graphs
    vf2pp_all_times_graphs = []  # VF2++ time measurements on graphs

    for i in range(0,n):
        G = graph_db_sorted[i]

        med = np.array(np.zeros(reps))
        for j in range(0, reps):
            start = timeit.default_timer()

            nx.is_isomorphic(G, G) #VF2

            stop = timeit.default_timer()
            total_time = stop - start
            mins, secs = divmod(total_time, 60)
            med[j] = secs 

        vf2_all_times_graphs.append(np.median(med))

        med = np.array(np.zeros(reps))
        for j in range(0, reps):
            start = timeit.default_timer()

            nx.vf2pp_is_isomorphic(G, G) #VF2++

            stop = timeit.default_timer()
            total_time = stop - start
            mins, secs = divmod(total_time, 60)
            med[j] = secs 
        
        vf2pp_all_times_graphs.append(np.median(med))
    
    #Create dataset with time measurements 
    p = pd.DataFrame()
    p["size"] = sizes_sorted[0:n]
    p["vf2"] = vf2_all_times_graphs
    p["vf2++"] = vf2pp_all_times_graphs

    #Calculate the median between all values by size 
    median = p.groupby(['size']).median() 

    # Plot experiment results 
    
    plt.plot(median["vf2"], label = "vf2")
    plt.plot(median["vf2++"], label = "vf2++")
    plt.legend(title= "Algorithms")
    plt.title("VF2 vs. VF2++ on PROTEINS dataset", fontweight="bold")
    plt.ylabel("Execution Time (seconds)")
    plt.xlabel("Number of nodes")
    plt.savefig('ex_PROTEINS.png')
    plt.show()

if __name__ == "__main__":
    main()
