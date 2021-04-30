---
jupytext:
  notebook_metadata_filter: all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
language_info:
  codemirror_mode:
    name: ipython
    version: 3
  file_extension: .py
  mimetype: text/x-python
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
  version: 3.8.3
---

# Facebook Network Analysis
This notebook contains a social network analysis mainly executed with the library of NetworkX. In detail, the facebook circles (friends lists) of ten people will be examined and scrutinized in order to extract all kinds of valuable information. The dataset can be found [here](http://snap.stanford.edu/data/ego-Facebook.html). Moreover, as known, a facebook network is undirected and has no weights because one user can become friends with another user just once. Looking at the dataset from a graph analysis perspective:
* Each node represents an anonymized facebook user that belongs to one of those ten friends lists.
* Each edge corresponds to the friendship of two facebook users that belong to this network. In other words, two users must become friends on facebook in order for them to be connected in the particular network.

Note: Nodes $0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980$ are the ones whose friends list will be examined. That means that they are in the spotlight of this analysis. Those nodes are considered the `spotlight nodes`

+++

* Now, the necessary libraries are imported

```{code-cell} ipython3
%matplotlib inline
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
```

* The edges are downloaded from the [stanford website](http://snap.stanford.edu/data/ego-Facebook.html) and saved in a dataframe. Each edge is a new row and for each edge there is a `start_node` and an `end_node` column

```{code-cell} ipython3
facebook = pd.read_csv('http://snap.stanford.edu/data/facebook_combined.txt.gz', compression='gzip', sep=' ', names=['start_node', 'end_node'])
facebook
```

* The graph is created from the `facebook` dataframe of the edges:

```{code-cell} ipython3
G = nx.from_pandas_edgelist(facebook, 'start_node', 'end_node')
```

## Graph representation
* The graph is drawn in order to get a better understanding of how the facebook circles look

```{code-cell} ipython3
plt.figure(figsize=(15,9)) #setting up the plot size
plt.axis('off')  #remove border around the graph
nx.draw_networkx(G, node_size=10, with_labels=False, width=0.15)
plt.show()
```

## Basic topological attributes
* Total number of nodes in network:

```{code-cell} ipython3
G.number_of_nodes()
```

* Total number of edges:

```{code-cell} ipython3
G.number_of_edges()
```

Also, the average degree of a node can be seen. 
* On average, a node is connected to almost 44 other nodes, also known as neighbors of the node. 
* This has been calculated by creating a list of all the degrees of the nodes and using `numpy.array` to find the mean of created list.

```{code-cell} ipython3
np.array(list(dict(G.degree()).values())).mean()
```

* The diameter is calculated now. As known, it is the longest shortest path of the graph. That means in order to connect from any node to another one we would have to traverse 8 edges or less.

```{code-cell} ipython3
nx.diameter(G)
```

* Next up, the average path length is found. In detail, it is defined as the average of the shortest paths for all pairs of nodes. That means that generally in order to reach from one node to another node, 3 or 4 edges will be crossed.

```{code-cell} ipython3
nx.average_shortest_path_length(G)
```

Now a histogram of the shortest paths lenghts' relative frequencies will be created to see how those lenghts are distributed.
* Firstly, all the shortest paths will be found
* Then, a list `frequencies` will be created to store the frequency of each path length
* Next, every shortest path will be checked and the frequency of its length will be increased by 1
* Lastly, the percentages of each frequency will be calculated. Even though the frequencies are doubled (because each shortest path between two specific nodes n1 and n2 was calculated twice, once from n1 to n2 and once from n2 to n1), the percentages remain correct.

```{code-cell} ipython3
shortest_paths = nx.shortest_path(G) #saving all shortest paths in a dictionary
frequencies = [0 for i in range (nx.diameter(G))] #list that will contain the different frequencies
for node_start in shortest_paths.keys():
    for path in shortest_paths.get(node_start).values():
        path_length = len(path) - 1 #path is a list of nodes, so the length consists of edges equal to one less node
        if path_length > 0: #paths with 0 length are no use
            frequencies[path_length-1] += 1 #increase the frequency of the particular path length by one
frequencies = [num/sum(frequencies) for num in frequencies] # finding the percentage of each path length
```

* Showcasing the results. Clearly, the distribution of the percentages is skewed on the right. The majority of the shortest path lengths are from $2$ to $5$ edges long. Also, it's highly unlikely for a pair of nodes to have a shortest path of length 8 (diameter length) as the likelihood is less than $0.1$%.

```{code-cell} ipython3
plt.figure(figsize=(15,8))
ax = plt.bar(x= [ i+1 for i in range (8)] , 
            height=frequencies)
plt.title('Percentages of Shortest Path Lengths', fontdict ={'size': 35}, loc='center') 
plt.xlabel('Shortest Path Length', fontdict ={'size': 22})
plt.ylabel('Percentage',fontdict ={'size': 22})
plt.show()
```

* The graph's density is calculated here. Clearly, the graph is a very sparse one as: $density < 1$

```{code-cell} ipython3
nx.density(G)
```

## Centrality measures
Now the centrality measures will be examined for the facebook graph

+++

### Degree Centrality
Degree centrality assigns an importance score based simply on the number of links held by each node. In this analysis, that means that the higher the degree centrality of a node is, the more edges are connected to the particular node and thus the more neighbor nodes (facebook friends) this node has. In fact, the degree of centrality of a node is the fraction of nodes it is connected to. In other words, it is the percentage of the network that the particular node is connected to meaning being friends with.
* Starting, we find the nodes with the highest degree centralities. Specifically, the nodes with the 8 highest degree centralities are shown below together with the degree centrality:

```{code-cell} ipython3
degree_centrality = nx.centrality.degree_centrality(G) #saving results in a variable to use again 
(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True))[:8]
```

That means that node $107$ has the highest degree centrality with $0.259$, meaning that this facebook user is friends with around the 26% of the whole network. Similarly, nodes $1684, 1912, 3437$ and $0$ also have very high degree centralities. However, that is well expected as those nodes are the ones whose circles we examine. Very interesting is the fact that the nodes $2543, 2347, 1888$ have some of the top 8 highest degree centralities even though we do not investigate their circles. In other words, those three nodes are very popular among the circles we examine now, meaning they have the most facebook friends inside this network apart from the spotlight nodes.
* Now we can also see the number of neighbors for the nodes with the highest degree centralities:

```{code-cell} ipython3
(sorted(G.degree, key=lambda item: item[1], reverse=True))[:8]
```

As expected, node $107$ has $1045$ facebook friends which is the most any facebook user has in this analysis. Moreover, nodes $1684$ and $1912$ have more than $750$ facebook friends in this network. Also, nodes $3437$ and $0$ have the following highest number of facebook friends in this network with $547$ and $347$ respectively. Lastly, the two most popular friends of spotlight nodes have around $290$ facebook friends in this network.


Now the distribution of degree centralities will be plotted:

```{code-cell} ipython3
plt.figure(figsize=(15,8))
plt.hist(degree_centrality.values(), bins=25)
plt.xticks(ticks=[0, 0.025, 0.05, 0.1, 0.15, 0.2]) #setting the x axis ticks
plt.title('Degree Centrality Histogram ', fontdict ={'size': 35}, loc='center') 
plt.xlabel('Degree Centrality', fontdict ={'size': 20})
plt.ylabel('Counts',fontdict ={'size': 20})
plt.show()
```

It is visible that the vast majority of facebook users have degree centralities of less than $0.05$. In fact the majority has less than $0.0125$. Actually, that makes sense because the network consists of friends lists of particular nodes, which are obviously the ones with the highest degree centralities. In other words, because only the friends list of particular nodes were used to create this particular network, plenty of nodes have extremely low degree centralities as they are not very interconnected in this network

Now let's check the users with highest degree centralities from the size of their nodes:

```{code-cell} ipython3
node_size =  [v * 1000 for v in degree_centrality.values()] #setting up nodes size for a nice graph representation
plt.figure(figsize=(15,8))
nx.draw_networkx(G, node_size=node_size, with_labels=False, width=0.15)
plt.axis('off')
plt.show()
```
