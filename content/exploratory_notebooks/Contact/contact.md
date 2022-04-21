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

# Social Network Analysis 
## Subject: Kenyan Household Contact Network
In this notebook we will be analysing a social network in our case we will be analysing the contact network of house.
This will provide us with a network approach for integrating and analyzing all collected contact records via a simple network graph.Our dataset is gotten from http://www.sociopatterns.org/datasets/kenyan-households-contact-network/ 

The data shows contact pattern between different people. Our dataset contains data of people within the same household as well as data of people across household. For the purpose of this notebook, we will focus more on the data of those within the house hold. The name of the file has been renamed to ease its usage in this explanatory session.

## Objective
Our goal is to see how we can analyse real world data using `Networkx`.

Our case study here is amongst people in a household and not across households. With aim of the data can be to analyse the spread of diseases or who contaminates the other. The network holds data of people and the different people the came in contact with. This data was gotten with the help of sensors, the sensors here are  wearable devices that exchange ultra-low power radio packets and can detect close proximity of individuals wearing them. In a nutshell the `nodes` represent people while the `edges` represent the different contact made by this individuals.







Importing our necessary libraries, we have:

```python
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

```

Reading our data with `pandas` and `networkx` we have:

```python
df = pd.read_csv("within.csv")
G =nx.from_pandas_edgelist(df, source="m1", target="m2")

```

```python
type(G) # This tells us the type of graph we have
```

## Visualizing the Graph
We will look at some visualization of the graph. This will help us to put a picture in our mind of how the different individuals connect with each other.

```python
fig, ax = plt.subplots(figsize=(15, 10))
ax = ax
options = {"width": 70, "with_labels": False, "width": 0.25}
nx.draw_networkx(G, pos=nx.random_layout(G), ax=ax, **options)
```

```python
fig, ax = plt.subplots(figsize=(15, 10))
options = {"width": 70, "with_labels": True, "width": 0.45}
nx.draw_networkx(G, pos=nx.circular_layout(G), ax=ax, **options)
```

## Basic Information from the Graph
Having our graph, let's look at some basic informations which can be derived from the graph. For instance:

The number of nodes can tell us the size of the network.

The number of edges can tell you how busy the network is, it can tell us how connected the different nodes are related.

```python
print("number of nodes for graph G is ", nx.number_of_nodes(G))

print("number of edges for graph G is ", nx.number_of_edges(G))

```

With this little piece of information, we are already able to analyse and draw some conclusion from the graph since we have the possibility to comment on some factors like the size of the network, and how busy are the network is.


## Density
The density of the graph tells us to which extent the graph are interconnected. It is a measure of how many ties between nodes exists to how many ties between actors are possible.

```python
nx.density(G)
nx.is_directed(G)
```

### Degree
The degree shows how connected a particular node is i.e how connected node A is to other nodes in the network. It indicates the number of lines that enter the vertex. We will be able to tell if a graph is traversable by looking once we have the degree of each vertex by looking at the odd and even vertices. A graph is said to be traversable when you can trace over all the arcs of a graph exactly without lifting your pen.

In general the degree of a vertex will be up to the number of vetices in the grpah  minus 1. It can be regarded in 2 case:
- Directed Graph
- Undirected Graph
For the purpose of graph G which is undirected we will analyse it as undirected at this level but eventully as we move down we will examine the case of directed Graph.

deg(V) = n - 1 for all V element in G

```python
deg = dict(nx.degree(G))
print(deg)
```

From here se can say deduce that node 2 has 15 connections while node 4 has 37 connections. 
But `nx.degree(G)` is not really explicit. Let's make it sorted so that we can see better. 

```python
{k: v for k, v in sorted(deg.items(), key=lambda item: item[1])}


```

This shows us that node 46 has a lot of connections. In our case where we are looking at how people relate with each other we can say that node 46 has the least number of connection which is 6.


## Degree Centrality
Degree Centrality tell you how influential a node is, it helps find the popular individuals who are likely to connect with the wider networfwhere the higher the degree the more influential the person is and vice versa . It helps us to find  Degree centrality assigns an importance score based simply on the number of links held by each node. But why degree centrality when we already have the degree? 
The degree of a node is simply a count of how many social connections it has while the degree centrality of a node is simply its degree.

```python
degreee = sorted((d for n, d in G.degree()), reverse=True)
```

```python
nx.degree_centrality(G)
```

Let's plot a histogram for the degree of centrality.

```python
degreeCentrality = nx.degree_centrality(G)
fig2, ax = plt.subplots(figsize =(10, 7))
ax.hist(list(degreeCentrality.values()), color='#2D5500',edgecolor='white')
ax.set_title("Degree Centrality Values")
plt.show()
```

## Eigen vector centrality tells the most important link or connection
Unlike degree centrality, eigen vector centrality identifies nodes with influence over the whole network and not those just directly connected to it.

```python
eigen_vector= nx.eigenvector_centrality(G)
# sorting it we have
{k: v for k, v in sorted(eigen_vector.items(), key=lambda item: item[1])}


```

## shortest path
It is the shortes path between a graph it can be done as
nx.shortest_graph(G, 'A', 'B')



While analysing our network, let's assume the case monitoring the flow of disease we can know that the shortest path from person A to D might be A C D, and if it was a case of a road network then travelling from A to D will be short by passing through C

```python
nx.shortest_path(G)
```

## Betweener centrality
It's a bridge or connector. It measures the number of times a node lies on the system. It helps to find individual who influence the flow around the system

```python
nx.betweenness_centrality(G)
```

## Communicability

A large sugraph communicability bettween two nodes A and B indicates that information flow easily between them

```python
nx.communicability(G)
```

```python
plt.hist(list(nx.communicability(G)))
```

## Distance Measures
The different distance meausures helps us a lot and tells us a lot in social analysis. 
### Eccentricity
It shows the maximum distance between a vertex to all other vertices. 
In our analysis this will tell us the the furthest distance of a person to another. Again with the reasons of the network analysis you might just be able to get the limits of a particular person.

```python
nx.eccentricity(G)
```

```python
plt.hist(list(nx.eccentricity(G).values()))
```

```python
nx.eccentricity(G, v=[26,27, 28, 29])# This gives us the eccentricity of nodes [26 - 29]

```

## Diameter 
The diameter of a graph shows the maximum eccentricity of any vertex in the graph. 
The simplest way going about this is `nx.diameter(G)` 

Visualizing the diameters of the graph we have:

```python
nx.eccentricity(G)
```

## Radius
While the diameter cares about the distance of the distant nodes, the radius talks about the distance of the closest nodes.

```python
color_map = []
for node in G:
    if node == (nx.radius(G)):
        color_map.append('yellow')
    else:
        color_map.append('purple')
nx.draw(G, node_color=color_map, with_labels="True")
```

```python
color_map = []
for node in G:
    if node == (nx.diameter(G)):
        color_map.append('yellow') # The nodes in yellow are the nodes which represent the diameter of graph G
    else:
        color_map.append('purple')
nx.draw(G, node_color=color_map, with_labels="True")
```

But why the interest in diameter? Diameter can help in social network analysis to give a statement on the number of nodes. This is due to the tendency of a graph with high availability of nodes having a more smaller diameter compared to a network with fewer nodes, well this is just a school of thought and there will always be exceptions. The most prominent information that the diameter of a grpah will give you, is the distance of the most distant nodes in the graph, and it will help in analysing our data for instance in a case of travel network the diameter can tell how far apart two different location are and in the case of analysis it tellss us the distance of two individual so it will be relatively more difficult for the node with diameter 3 to communicate compare to the others with eccentricites of 2.


## Subgroup
It retrieves all nodes connected to a given  node withing a graph
nx.bfs_tree(G, 'A')

```python
H = nx.bfs_tree(G, 1)

```

Yay!! now we have a subgroup which is a directed graph. A directed graph is a type of graph that contains ordered pairs of vertices while an undirected graph is a type of graph that contains unordered pairs of vertices. We can confirm that a graph is directed by using `is_directed` in networkx which returns True if the graph is a directed graph and False other wise. 

```python
nx.is_directed(H)
```

## Visualizing the Graph


```python
nx.draw_planar(H)
```

```python
fig, ax = plt.subplots(figsize=(15, 10))
options = {"node_size": 20, "with_labels": True, "width": 0.15}
nx.draw_networkx(H, pos=nx.planar_layout(H), ax=ax, **options)
```

```python
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.gnp_random_graph(100, 0.02, seed=10374196)

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree of a random graph", figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc, seed=10396953)
nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
ax0.set_title("Connected components of G")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

fig.tight_layout()
plt.show()
```
