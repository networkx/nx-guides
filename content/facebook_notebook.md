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
* This has been calculated by creating a list of all the degrees of the nodes and using `numpy.array` to find the mean of the created list.

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

* The graph's number of components are found below. As expected, the network consists of one giant compoenent:

```{code-cell} ipython3
nx.number_connected_components(G)
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

### Betweenness Centrality
Betweenness centrality measures the number of times a node lies on the shortest path between other nodes, meaning it acts as a bridge. In detail, betweenness centrality of a node $v$ is the percentage of all the shortest paths of any two nodes (apart from $v$), which pass through $v$. Specifically, in the facebook graph this measure is associated with the user's ability to influence others. A user with a high betweenness centrality acts as a bridge to many users that are not friends and thus has the ability to influence them by conveying information (e.g. by posting something or sharing a post) or even connect them via the user's circle (which would reduce the user's betweeness centrality after).
* Now, the nodes with the $8$ highest betweenness centralities will be calculated and shown with their centrality values:

```{code-cell} ipython3
betweenness_centrality = nx.centrality.betweenness_centrality(G) #saving results in a variable to use again 
(sorted(betweenness_centrality.items(), key=lambda item: item[1], reverse=True))[:8]
```

Looking at the results, the node $107$ has a betweenness centrality of $0.48$, meaning it lies on almost half of the total shortest paths between other nodes. Also, combining the knowledge of the degree centrality:
* Nodes $0, 107, 1684, 1912, 3437$ have both the highest degree and betweenness centralities and are `spotlight nodes`. That indicates that those nodes are both the most popular ones in this network and can also influence and spread information in the network. However, those are some of the nodes whose friends list consist the network and as a result it is an expected finding.
* Nodes $567, 1085$ are not spotlight nodes, have some of the highest betweenness centralities and have not the highest degree centralities. That means that even though those nodes are not the most popular users in the network, they have the most influence in this network among friends of spotlight nodes when it comes to spreading information.
* Node $698$ is a `spotlight node` and has a very high betweenness centrality even though it has not the highest degree centralities. In other words, this node does not have a very large friends list on facebook. However, the user's friend list and thus the user could connect different circles in this network by being the middleman.

Moving on, the distribution of betweenness centralities will be plotted:

```{code-cell} ipython3
plt.figure(figsize=(15,8))
plt.hist(betweenness_centrality.values(), bins=100)
plt.xticks(ticks=[0, 0.02, 0.1, 0.2, 0.3, 0.4, 0.5]) #setting the x axis ticks
plt.title('Betweenness Centrality Histogram ', fontdict ={'size': 35}, loc='center') 
plt.xlabel('Betweenness Centrality', fontdict ={'size': 20})
plt.ylabel('Counts',fontdict ={'size': 20})
plt.show()
```

As we can see, the vast majority of betweenness centralities is below $0.01$. That makes sense as the graph is very sparse and thus most nodes do not act as bridges in shortest paths. However, that also results in some nodes having extremely high betweenness centralities as for example node $107$ with $0.48$ and node $1684$ with $0.34$ betweenness centrality.

We can also get an image on the nodes with the highest betweenness centralities and where they are located in the network. It is clear that they are the bridges from one community to another:

```{code-cell} ipython3
node_size =  [v * 1200 for v in betweenness_centrality.values()]  #setting up nodes size for a nice graph representation
plt.figure(figsize=(15,8))
nx.draw_networkx(G, node_size=node_size, with_labels=False, width=0.15)
plt.axis('off')
plt.show()
```

### Closeness Centrality
Closeness centrality scores each node based on their ‘closeness’ to all other nodes in the network. For a node $v$, its closeness centrality measures the average farness to all other nodes. In other words, the higher the closeness centrality of $v$, the closer it is located to the center of the network.

The closeness centrality measure is very important for the monitoring of the spread of false information (e.g. fake news) or viruses (e.g. malicious links that gain control of the facebook account in this case). Let's examine the example of fake news. If the user with the highest closeness centrality measure started spreading some fake news information (sharing or creating a post), the whole network would get missinformed the quickest possible. However, if a user with very low closeness centrality would try the same, the spread of the missinformation to the whole network would be much slower. That is because the false information would have to firstly reach a user with high closeness centrality that would spread it to many different parts of the network.
* The nodes with the highest closeness centralities will be found now:

```{code-cell} ipython3
closeness_centrality = nx.centrality.closeness_centrality(G) #saving results in a variable to use again 
(sorted(closeness_centrality.items(), key=lambda item: item[1], reverse=True))[:8]
```

Inspecting the users with the highest closeness centralities, we understand that there is not a huge gap between them in contrast to the previous metrics. Also, the nodes $107, 1684, 348$ are the only `spotlight nodes` found in the ones with the highest closeness centralities. That means that a node that has many friends is not necessary close to the center of the network.

Also, the average distance of a particular node $v$ to any other node can be found easily with the formula:

$$\frac{1}{closeness\,centrality(v)}$$

```{code-cell} ipython3
1 / closeness_centrality[107]
```

The distance from node $107$ to a random node is around two hops


Furthermore, the distribution of the closeness centralities:

```{code-cell} ipython3
plt.figure(figsize=(15,8))
plt.hist(closeness_centrality.values(), bins=60)
plt.title('Closeness Centrality Histogram ', fontdict ={'size': 35}, loc='center') 
plt.xlabel('Closeness Centrality', fontdict ={'size': 20})
plt.ylabel('Counts',fontdict ={'size': 20})
plt.show()
```

The closeness centralities are distributed over various values from $0.17$ to $0.46$. In fact, the majority of them are found between $0.25$ and $0.3$. That means that the majority of nodes are relatively close to the center of the network and thus close to other nodes in general. However, there are some communities that are located further away, whose nodes would have the minimum closeness centralities, as seen below:

```{code-cell} ipython3
node_size =  [v * 50 for v in closeness_centrality.values()]  #setting up nodes size for a nice graph representation
plt.figure(figsize=(15,8))
nx.draw_networkx(G, node_size=node_size, with_labels=False, width=0.15)
plt.axis('off')
plt.show()
```

### Eigenvector Centrality
Eigenvector centrality is the metric to show how connected a node is to other important nodes in the network. It measures a node's influence based on how well it is connected inside the network and how many links its connections have and so on. This measure can identify the nodes with the most influence over the whole network. A high eigenvector centrality means that the node is connected to other nodes who themselves have high eigenvector centralities. In this facebook analysis, the measure is associated with the users ability to influence the whole graph and thus the users with the highest eigenvector centralities are the most important nodes in this network.

* The nodes with the highest eigenvector centralities will be examined now:

```{code-cell} ipython3
eigenvector_centrality = nx.centrality.eigenvector_centrality(G) #saving results in a variable to use again 
(sorted(eigenvector_centrality.items(), key=lambda item: item[1], reverse=True))[:10]
```

Checking the results:
* Node $1912$ has the highest eigenvector centrality with $0.095$. This node is also a `spotlight node` and can surely be considered the most important node in this network in terms of overall influence to the whole network. In fact, this node also has some of the highest degree centralities and  betweenness centralities, making the user very popular and influencious to other nodes. 
* Nodes $1993, 2078, 2206, 2123, 2142, 2218, 2233, 2266, 2464$, even though they are not spotlight nodes, have some of the highest eigenvector centralities with around $0.83-0.87$. Very interesting is the fact that all those nodes are identified for the first time, meaning they have neither the heighest degree, betweenness or closeness centralities in this graph. That leads to the conclusion that those nodes are very likely to be connected to the node $1912$ and as a result have very high eigenvector centralities.

Checking if those nodes are connected to the most important node $1912$, the hypothesis is correct:

```{code-cell} ipython3
high_eigenvector_centralities = ((sorted(eigenvector_centrality.items(), key=lambda item: item[1], reverse=True))[1:10]) #2nd to 10th heighest eigenvector centralities
high_eigenvector_nodes = [tuple[0] for tuple in high_eigenvector_centralities]  # sets list as [2266, 2206, 2233, 2464, 2142, 2218, 2078, 2123, 1993]
neighbors_1912 = [n for n in G.neighbors(1912)]  #list with all nodes connected to 1912
all(item in neighbors_1912 for item in high_eigenvector_nodes) #check if items in list high_eigenvector_nodes exist in list neighbors_1912
```

Let's check the distribution of the eigenvector centralities:

```{code-cell} ipython3
plt.figure(figsize=(15,8))
plt.hist(eigenvector_centrality.values(), bins=60)
plt.xticks(ticks=[0, 0.01, 0.02, 0.04, 0.06, 0.08]) #setting the x axis ticks
plt.title('Eigenvector Centrality Histogram ', fontdict ={'size': 35}, loc='center') 
plt.xlabel('Eigenvector Centrality', fontdict ={'size': 20})
plt.ylabel('Counts',fontdict ={'size': 20})
plt.show()
```

As shown in the distribution histogram, the vast majority of eigenvector centralities are below $0.005$ and are actually almost $0$. However, we can also see different values of eigenvector centralities as there are tiny bins all over the x axis.

Now we can identify the eigenvector centralities of nodes based on their size in the following representation:

```{code-cell} ipython3
node_size =  [v * 4000 for v in eigenvector_centrality.values()]  #setting up nodes size for a nice graph representation
plt.figure(figsize=(15,8))
nx.draw_networkx(G, node_size=node_size, with_labels=False, width=0.15)
plt.axis('off')
plt.show()
```

## Clustering Effects
The clustering coefficient of a node $v$ is defined as the probability that two randomly selected friends of $v$ are friends with each other. As a result, the average clustering coefficient is the average of clustering coefficients of all the nodes. The closer the average clustering coefficient is to $1$, the more complete the graph will be because there's just one giant component. Lastly, it is a sign of triadic closure because the more complete the graph is, the more triangles will usually arise.

```{code-cell} ipython3
nx.average_clustering(G)
```

Now the clustering coefficient distribution will be displayed:

```{code-cell} ipython3
plt.figure(figsize=(15,8))
plt.hist(nx.clustering(G).values(), bins=50)
plt.title('Clustering Coefficient Histogram ', fontdict ={'size': 35}, loc='center') 
plt.xlabel('Clustering Coefficient', fontdict ={'size': 20})
plt.ylabel('Counts',fontdict ={'size': 20})
plt.show()
```

 $50$ bins were used to showcase the distribution. The bin with the highest counts concerns nodes with clustering coefficient close to $1$ as there are more than two-hundred-fifty nodes in that bin. In addition, the bins of clustering coefficient between $0.4$ and $0.8$ contain the majority of nodes by far. 
 
 The number of unique triangles in the network are found next:

```{code-cell} ipython3
sum(list(nx.triangles(G).values())) / 3  #dividing by 3 because each triangle is counted once for each node
```

 Now the average number of triangles that a node is a part of:

```{code-cell} ipython3
np.mean(list(nx.triangles(G).values()))
```

Due to having some nodes that belong to a great many triangles, the metric of median will give us a better understanding:

```{code-cell} ipython3
np.median(list(nx.triangles(G).values()))
```

In fact, the median value is just $161$ triangles, when the mean is around $1197$ triangles that a node is part of. That means that the majority of nodes of the network belong to extremely few triangles, whereas some nodes are part of a plethora of triangles (which are extreme values that increase the mean)

In conclusion, the high average clustering coefficient together with the huge number of triangles are signs of the triadic closure. In detail, the triadic closure means that as time goes on, new edges tend to form between two users that have one or more mutual friends. That can be explained by the fact that Facebook usually suggests new friends to a user when there are many mutual friends between the user and the new friend to be added. Also, there is a source of latent stress. For example, if node $A$ is friends with
node $B$ and $C$,  some tension builds up if $B$ and $C$ are not friends with each other.

+++

## Bridges
First of all, an edge joining two nodes A and B in the graph is considered a bridge, if deleting the edge would cause A and B to lie in two different components. Now it is checked if there are any bridges in this network:

```{code-cell} ipython3
nx.has_bridges(G)
```

Actually, there are bridges in the network. Now the edges that are bridges will be saved in a list and the number of them is printed:

```{code-cell} ipython3
bridges = []
for edge in nx.bridges(G):
    bridges.append(edge)
len(bridges)
```

The existence of so many bridges is due to the fact that this network only contains the spotlight nodes and the friends of them. As a result, some friends of spotlight nodes are only connected to a spotlight node, making that edge a bridge.

Also, the edges that are local bridges are saved in a list and their number is printed. In detaill, an edge joining two nodes $C$ and $D$ 
in a graph is a local bridge, if its endpoints $C$ and $D$ have no friends in common. Very importantly, an edge that is a bridge is also a local bridge. Thus, this list contains all the above bridges as well:

```{code-cell} ipython3
local_bridges = []
for edge in nx.local_bridges(G):
    local_bridges.append(eval( '(' + str(edge[0]) + '),(' + str(edge[1]) + ')' )) # saving the local bridge as a tuple
len(local_bridges)
```

Showcasing the bridges and local bridges in the network now. The bridges can be seen with the red color and the local bridges with the green color. Black edges are neither local bridges nor bridges.

* It is clear that all the bridges concern nodes that are only connected to a spotlight node (have a degree of $1$)

```{code-cell} ipython3
pos = nx.spring_layout(G)  # positions for all nodes
plt.figure(figsize=(15,8))
nx.draw_networkx(G, pos=pos, node_size=10, with_labels=False, width=0.15)
nx.draw_networkx_edges(G, pos, edgelist=local_bridges, width=0.5, edge_color="lawngreen")  # green color for local bridges 
nx.draw_networkx_edges(G, pos, edgelist=bridges, width=0.5, edge_color="r") # red color for bridges
plt.axis('off')
plt.show()
```

## Assortativity
Assortativity describes the preference for a network's nodes to attach to others that are similar in some way.
* The assortativity in terms of nodes degrees is found with two ways:

```{code-cell} ipython3
nx.degree_assortativity_coefficient(G)
```

```{code-cell} ipython3
nx.degree_pearson_correlation_coefficient(G) # uses the potentially faster scipy.stats.pearsonr function.
```

In fact, the assortativity coefficient is the Pearson correlation coefficient of degree between pairs of linked nodes. That means that it takes values from $-1$ to $1$. In detail, a positive assortativity coefficient indicates a correlation between nodes of similar degree, while a negative indicates correlation between nodes of different degrees.

In our case the assortativity coefficient is around $0.064$, which is almost 0. That means that the network is almost non-assortative, and we cannot correlate linked nodes based on their degrees. In other words, we can not draw conclusions on the number of friends of a user from his/her friends' number of friends (friends degree). That makes sense since we only use the friends list of spotlight nodes, non spotlight nodes will tend to have much fewer friends while also occasionally being connected to each other.
