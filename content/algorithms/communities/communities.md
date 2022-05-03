---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3.8.10 64-bit
    language: python
    name: python3
---

# Communities in Network Analysis using Networkx
In this tutorial we will look at communities in Network Analysis. We are going to analyse graphs to better understand communities in networkx. 

A community can be defined as a subset of nodes within the graph such that connections between the nodes are denser than connections with the rest of the network. The detection of the community structure in a network is generally intended as a procedure for mapping the netork into a tree. Knowing the community structures in a network is very relevant for different domains and disciplines including biological enquiries, technological problems and social tasks etc.



## Importing our modules.
One thing to know about about communities in networkx, the functions are not imported onto the top-level networkx namespace. So we are going to access it by importing the `networkx.algorithms.community` modules.

```python
import networkx as nx
from networkx.algorithms import community
import pandas as pd
import matplotlib.pyplot as plt
```

Here is our welcoming example to demonstrate communites in networkx. More fun demonstration below.

```python
H = nx.karate_club_graph()
nx.draw(H) # drawing the graph for visualization
com = sorted(community.greedy_modularity_communities(H), key=len)
print("There are {} communities in the karate club graph".format(len(com)))
```

## Communities
Looking at another example. Let's assume the following nodes are group of people who know each other, they could be classmates, business associates or  even friends. This can be a typical example of our day to day life where I know John and Peter, Peter knows Elizabeth and so on. From the graph it is easier to see that some set of nodes (people) are more connected to others.

```python
G = nx.Graph()
G.add_edges_from([
    ('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'),('C', 'D'), ('A', 'D'), ('C', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'G'), ('E', 'H'), ('H', 'J'), ('J', 'K'), ('K', 'M'), ('M', 'L'), ('L', 'K'),('M', 'J'), ('M', 'N'), ('N', 'A'), ('O', 'P'), ('O', 'R'), ('R', 'P'), ('R', 'F')])
```

```python
fig, ax = plt.subplots(figsize=(15, 10))
ax = ax
options = {"width": 70, "with_labels": True, "width": 0.25}
nx.draw_networkx(G, pos=nx.spring_layout(G), ax=ax, **options)
```

Now we have our simple graph and we know how our graph looks like. Let's use our networkx algrotithm to know how many communities we have present. 

```python

def number_of_communities(Graph):
    com = community.greedy_modularity_communities(Graph)
    return "There are {} communities in the graph ".format(len(com))
print(number_of_communities(G))
```

## Kernighan_lin_bisection
This function will divide our graph into two communities.

```python
bisec = nx.community.kernighan_lin_bisection(G)
# code to color each section seperately
```

## K clique
A
k-clique is a subset of vertices C such that, for every i, j∈ C, the distance d(i, j)
≤ k. The 1-clique is identical to a clique, because the distance between the
vertices is one edge. The 2-clique is the maximal complete sub-graph with a
path length of one or two edges. The path distance of two can be exemplified
by the “friend of a friend” connection in social relationships. In social websites,
like the LinkedIn, each member can reach his own connections as well as the 
6
ones two and three degrees away. The increase of the value k corresponds to
a gradual relaxation of the criterion of clique membership


A clique is  a set of users having favourite, atttibutes, or goals. Identifying cliques is a very important aspect in social networks. Because it tells you about the common attributes of some nodes. 

```python
def kClique(Graph, k):
    kcliq = list(nx.community.k_clique_communities(Graph, k)) # This gives the number of communities which form at least a clique made up of k nodes
    print("There are {} k clique communities in the graph with k equal to {}" .format(len(kcliq), k))
    return kcliq

print(kClique(G, 3))
    

```

We can always get the different nodes which form a clique with another using `nx.find_cliques`

```python
k =  list((nx.find_cliques(G, nodes=['G', 'H']))) # returns an error if nodes don't form a clique
print(k)
```

## Modularity Based Community
Modularity is a measure of the structure of networks or graphs which measures the strength of division of a network into modules (also called groups, clusters or communities). Networks with high modularity have dense connections between the nodes within modules but sparse connections between nodes in different modules.

```python
kk = nx.community.greedy_modularity_communities(G, resolution=2, cutoff=9)
# best_n works
# cutoff works
# n_communities work
print(kk)
```

```python
nx.community.lukes_partitioning(G, max_size = 2)
```

Community Detection vs Clustering
One can argue that community detection is similar to clustering. Clustering is a machine learning technique in which similar data points are grouped into the same cluster based on their attributes. Even though clustering can be applied to networks, it is a broader field in unsupervised machine learning which deals with multiple attribute types. On the other hand, community detection is specially tailored for network analysis which depends on a single attribute type called edges. Also, clustering algorithms have a tendency to separate single peripheral nodes from the communities it should belong to. However, both clustering and community detection techniques can be applied to many network analysis problems and may raise different pros and cons depending on the domain.



## Clustering example


```python
for node in G.nodes:
  print(node, nx.clustering(G,node))
```

```python
print(nx.info(G))
```

```python
## not useful
plt.figure(figsize=(10,10))

nx.draw(G, 
        with_labels=True,
        pos=nx.spring_layout(G), # spring_layout is the default layout
        cmap=plt.cm.coolwarm,
        node_size=1000)

# Save the graph

```

## Label Propagation

```python
H = list(nx.community.asyn_lpa_communities(G))
print(H)
```

```python
list(nx.community.label_propagation_communities(G))
```

## References
https://www.pnas.org/doi/10.1073/pnas.0400054101#:~:text=Qualitatively%2C%20a%20community%20is%20defined,1).

