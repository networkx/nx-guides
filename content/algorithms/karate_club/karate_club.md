---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Zachary’s Karate Club graph: Spectral analysis 

Graphs can be represented using different structures like adjacency matrixes or dict of dicts. Every representation works best for a specific application. Some matrix representations are particularly interesting because we can use properties from linear algebra to analyze graphs. In this notebook, we will do a spectral analysis of the Karate Club graph.

+++

##  Zachary’s Karate Club graph

The network has 34 nodes, one for each member of the karate club, and the edges represent the relationships between the pairs of members who interacted outside the club. During the study, there was a conflict between the administrator "John A"(node 0) and instructor "Mr. Hi" (node 33), which led to the split of the club into two. Half of the members formed a new club around Mr. Hi; members from the other part found a new instructor or gave up karate. We will use different methods to cut this graph and then compare our results with the actual split that happened in the real situation. 

### Let's explore this graph
First, we can draw this graph with different layouts to understand some initial properties. 
- *Circular layout:* Al nodes are positioned in a circular layout. We can use this layout to see which nodes have more connections. In this example, we can clearly see that nodes located on the right side have more connections.
 
- *Spring layout:* This layout simulates a force-directed representation of the network treating edges as springs holding nodes close and treating nodes as repelling objects. This layout can be used to find "central nodes" as other nodes will position around them. In this example, We can see that nodes are arranged around nodes 0 and 33. This is clearly not an accurate way to identify these nodes but can be used as a first approach.

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

K = nx.karate_club_graph()

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.set_size_inches(10, 6)

ax1.set_title("Spring layout", fontweight = "bold")
nx.draw_spring(K, with_labels = True, node_color = "c", ax = ax1) #Spring layout

ax2.set_title("Circular layout", fontweight = "bold")
nx.draw_circular(K, with_labels = True, node_color = "m", ax=ax2) #Circular layout 
```

But visualizations are not always an option, for example, when graphs are too big. Another great way to identify the nodes with more connections is by using the **degree centrality**.

The degree centrality for a node $u$ is the fraction of nodes it is connected to. 

$$ degree\_centrality(u) = \frac{deg(u)}{n_{G}-1} $$

So the nodes with a higher degree centrality are the ones that have more edges. Essentially degree centrality gives us a notion of how edges are distributed in the graph.

```{code-cell} ipython3
import matplotlib.cm as cm
from matplotlib.colors import Normalize, rgb2hex

def color_map_color(value, cmap_name="magma", vmin=0, vmax=1):
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)
    rgb = cmap(norm(abs(value)))[:3]
    color = rgb2hex(rgb)
    return color

degrees = list(nx.degree_centrality(K).values())

degree_colors = [color_map_color(degrees[i]) for i in range(34)] #Translate the degree value of each node into a value 
                                                           #that can be interpreted as a color

fig, ax = plt.subplots()

ax.bar(x = list(range(0,  34)), height= degrees, color = degree_colors)
plt.title("Degree centrality of the Karate club", fontweight = "bold")
plt.xlabel("Node labels")
plt.ylabel("Degree centrality")
plt.show()
```

In the previous plot, we can again identify that nodes 0 and 33 corresponding to the administrator and the instructor are the ones with a higher degree centrality. But we can't identify wich nodes are closer to the Administrator or the Instructor.

Another way to find the central nodes is by using the eigenvector centrality. This measure gives us more information that the degree of centrality because it is computed using the centrality of the neighbors of each node. The eigenvector centrality for node i is the i-th element of the vector defined by the equation
$$ Ax = \lambda x$$ 

where 
- $A$ is the adjacency matrix of the graph $G$. 
- $\lambda $ is the largest eigenvalue of the matrix $A$.

```{code-cell} ipython3
degrees = list(nx.eigenvector_centrality(K).values())

degree_colors = [color_map_color(degrees[i]) for i in range(34)] #Translate the degree value of each node into a value 
                                                           #that can be interpreted as a color

plt.bar(x = list(range(0,  34)), height= degrees, color = degree_colors)
plt.title("Eigenvector centrality of the Karate club", fontweight = "bold")
plt.xlabel("Node labels")
plt.ylabel("Eigenvector centrality")
plt.show()
```

Again we can see that nodes 0 and 33 are the most important but also there are some other nodes that are important because they are connected to "powerful" nodes. This gives us a notion that there are some nodes "closer" to the influential ones.

+++

## Matrix representation: Laplacian Matrix 
The laplacian matrix of a graph is a matrix representation of a graph. The matrix is defined as 

$$ L_{i,j} =  
\begin{cases}
deg(i) &  i = j\\
-1 & \text{there's an edge between } v_i \text{ and } v_j \\
0  & else
\end{cases}
$$

Also can be expressed as $L = D - A$ where $D$ is a diagonal matrix with the degree of each node and $A$ is the adjacency matrix. Essentially, the matrix will have the degree of each node in the diagonal and a -1 in the position (i, j) if nodes i and j are connected in the graph. 

The Laplacian matrix is particularly interesting because it captures information about both the specific connections between the nodes and also about the amount of them. In other words, this matrix also captures information about the centrality of the nodes in the network. Also, this matrix has some very interesting mathematical properties that can be used to analyze graphs. 

The Lapacian Matrix is used in many real-world applications as: 

- It can be use to construct low dimensional embeddings that appear in many machine learning applications. 
- Spectral layout in graph drawing. 
- Graph-based signal processing. 

Let's see what the laplacian matrix of a small matrix looks like using a heatmap:

```{code-cell} ipython3
G = nx.barbell_graph(3, 1) #Two complete graphs of 3 nodes connected with a path of 1 node

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.set_title("Barbell Graph", fontweight = "bold")
nx.draw(G, with_labels = True, ax = ax1, node_color = "c")

L = nx.laplacian_matrix(G).toarray() #Create Laplacian matrix 

#Create heatmap
im = ax2.imshow(L, cmap= "viridis")
# Loop over data dimensions and create text annotations.
for i in range(len(G.nodes)):
    for j in range(len(G.nodes)):
        if(L[i,j] != 3 and L[i, j] != 2):
            text = ax2.text(j, i, L[i, j], ha="center", va="center", color="w")
        else: 
             text = ax2.text(j, i, L[i, j], ha="center", va="center", color="b")
                
ax2.set_title("Laplacian Matrix of Barbell graph", fontweight = "bold")
fig.tight_layout()
plt.show()
```

Heatmaps are particularly helpful to visualize bigger matrices especially when we don't need to see the specific values in the matrix but the magnitudes. Let's visualize the Laplacian Matrix of the Karate club graph.

```{code-cell} ipython3
L = nx.laplacian_matrix(K, weight = None) #Create laplacian matrix 

#plot heatmap 
fig, ax = plt.subplots()
fig.set_size_inches(8, 8)
im = ax.imshow(L.toarray(), cmap = "cividis")

ax.set_title("Laplacian Matrix of the Karate Club Graph", fontweight = "bold")
plt.colorbar(im)
plt.show()
```

In this heatmap, we can see:
1) In the diagonal that nodes 0 and 33 are the nodes with  higher degrees.  
2) The graph is pretty sparse as the darker blue squares are not predominant. 
3) Most connections happen between two nodes with a low label or two nodes with a higher label. 

In the Karate club, there was a conflict between the administrator and the instructor that resulted in the split of the club into two groups. Observation 3) can give us a naive approach that we can use to cut this network in half. Let’s see what it looks like to cut the network using the labels.

+++

### Partition the graph: Naive Approach

We will define two new graphs using the labels. One graph will have all nodes with labels from 0 to 16 and the induced edges. The other will have all the remaining nodes and induced edges. 

This method is obviously not recommended for general use because usually labels don’t include information about the network structure. But it’s always important to try some naive approach first and then test if our refined approach is actually better or not. Sometimes, especially in real-world applications, simple approaches can do a job that is good enough and is a less costly solution.

```{code-cell} ipython3
#Create 2 Karate graphs
K1_naive = nx.karate_club_graph()
K2_naive = nx.karate_club_graph()

#Remove nodes using labels 
K1_naive.remove_nodes_from(list(n for n in K1_naive.nodes if n >= 17))
K2_naive.remove_nodes_from(list(n for n in K2_naive.nodes if n < 17))

#Create list without isolated nodes for better visualization
K1_not_isolated=[ n for n,d in K1_naive.degree() if d!=0 ]
print("Isolated nodes in group Administrator ", len(K1_naive.nodes) - len(K1_not_isolated))

K2_not_isolated=[ n for n,d in K2_naive.degree() if d!=0 ]
print("Isolated nodes in group Instructor ", len(K2_naive.nodes) - len(K2_not_isolated))

#Plot both networks 
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 10)

plt.subplot(221)

nx.draw(K1_naive, with_labels = True, node_color = "c", nodelist = solitary1)
plt.title("Group Administrator", fontweight = "bold")

plt.subplot(222)
nx.draw(K2_naive, with_labels = True, nodelist = solitary2, node_color = "m")
plt.title("Group Instructor", fontweight = "bold")

plt.show()
```

The partition results in two graphs of the same size. Initially, we can notice that some nodes were sorted into a group where they don't have any connection which means they should’ve been assigned to the other group as the initial graph is connected. To see if this cut is indeed a "good" option we will need to compare it to other partitions and the real partition. We will do that analysis later in this notebook. 

Let's use some other methods to find cuts.

+++

## Algebraic connectivity and Fiedler vector 

The *algebraic connectivity* of a graph $G$ is the second-smallest eigenvalue (counting multiple eigenvalues separately) of its Laplacian matrix. The magnitude of this value reflects how well-connected the graph is. This connectivity measure considers how many connections there are but also the way in wich vertex are connected.   

The *Fiedler vector* of a connected undirected graph is the eigenvector corresponding to the second smallest eigenvalue of the Laplacian matrix of the graph. In other words, is the eigenvector associated with the eigenvalue that determines the algebraic connectivity. This vector is particularly interesting because it can be used to partition the graph. To partition the graph, we use the signs of the values in the Fiedler vector to assign nodes to one group or another. This method will let us partition the graph into two graphs of similar size by minimizing the number of edges that have to be removed. 

Let's see this in a small example where we will partition a barbell graph. First, we can draw the graph and guess which are the edges that will be eliminated to do the partition. In this case, we could delete the edge (2,3) or (3, 4) that are the red edges in the graph below and get a good partition of the graph. Deleting one edge is enough to get a partition for this particular graph. Any other edge that we delete will not partition the graph. 

```{code-cell} ipython3
G = nx.barbell_graph(3, 1) #Two complete graphs of 3 nodes connected with a path of 1 node

#Set edge colors 
edge_colors = [ "k" for e in G.edges()]
edge_colors[3] = "r" #draw edges (2, 3) and (3, 4) in red 
edge_colors[6] = "r"

plt.title("Barbell Graph", fontweight = "bold")
nx.draw(G,  with_labels = True, node_color = "c", edge_color = edge_colors)
```

Now let's use the fiedler vector to partition this graphs.  

```{code-cell} ipython3
G = nx.barbell_graph(3, 1)

#fiedler vector 
fiedler_vector = nx.fiedler_vector(G, seed = 7)
print("Fiedler vector: ", nx.fiedler_vector(G))

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

edge_color = [ "k" for e in G.edges()]
edge_color[3] = "r"

node_color = []
for n in range(len(fiedler_vector)):
    if fiedler_vector[n] < 0:
        node_color.append("c")
    else: 
        node_color.append("m")

ax1.set_title("Barbell Graph", fontweight = "bold")
nx.draw(G,  with_labels = True, node_color = node_color, edge_color = edge_color, ax = ax1)


G1 = nx.barbell_graph(3, 1)
G1.remove_nodes_from(list(n for n in G1.nodes if fiedler_vector[n] < 0))
nx. draw(G1, ax = ax2, node_color = "m",  with_labels = True)
ax2.set_title("Partition 1", fontweight = "bold")

G2 = nx.barbell_graph(3, 1)
G2.remove_nodes_from(list(n for n in G2.nodes if fiedler_vector[n] >= 0))

nx. draw(G2, ax = ax3, node_color = "c", with_labels = True)
ax3.set_title("Partition 2", fontweight = "bold")

fig.tight_layout(h_pad=0.4)
```

As we expected, the Fiedler vector partitioned the graph by deleting the edge (2, 3). This resulted in a partition of two graphs of similar size. Now let’s get back to the Karate club and analyze the partitions obtained using this method.

```{code-cell} ipython3
fiedler_vec = nx.fiedler_vector(K) #Fiedler vector of the karate club graph

K1 = nx.karate_club_graph()
K1.remove_nodes_from(list(n for n in K1.nodes if fiedler_vec[n] >= 0))

K2 = nx.karate_club_graph()
K2.remove_nodes_from(list(n for n in K2.nodes if fiedler_vec[n] < 0))

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 10)

plt.subplot(221)
nx.draw(K1, with_labels = True, node_color = "c")
plt.title("Group Administrator", fontweight = "bold")

plt.subplot(222)
nx.draw(K2, with_labels = True, node_color = "m")
plt.title("Group Instructor", fontweight = "bold")

plt.show()
```

As we had anticipated, the nodes corresponding to the instructor and the administrator are each in a different graph. The partition resulted in two graphs of similar size. The graph corresponding to the administrator has 2 nodes more than the graph corresponding to the instructor. In contrast to what happened in the naive approach, none of the partitions have isolated nodes. Also, only 10 edges were deleted from the real graph in order to get the partitions. 

```{code-cell} ipython3
print("Graph administrator has :", len(K1.nodes), " nodes")
print("Graph instructor has :",len(K2.nodes), " nodes")

print("Karate club graph has: " , len(K.edges), " edges")
print("After the partition there are " , len(K2.edges) +len(K1.edges), " edges left")
```

### Real Partition
After the conflict, the Karate club member separated into two groups: one around the Instructor and the other around the Administrator. In *karateclub_labels.txt* we have the labels that indicate for each node to which group they are assigned. 
- 0 corresponds to the partition of the Administrator 
- 1 corresponds to the partition of the Instructor

```{code-cell} ipython3
import pandas as pd

# Read labels into a dataframe and create a list with the values
real_cut = list(pd.read_csv("karateclub_labels.txt", names = ["group"])["group"])

K1_real = nx.karate_club_graph()
K2_real = nx.karate_club_graph()

#Remove nodes using group labels 
K1_real.remove_nodes_from(list(n for n in K1_real.nodes if real_cut[n] == 1))
K2_real.remove_nodes_from(list(n for n in K2_real.nodes if real_cut[n] == 0))

#Plot 
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 10)

plt.subplot(221)
nx.draw(K1_real, with_labels = True, node_color = "c")
plt.title("Group Administrator", fontweight = "bold")

plt.subplot(222)
nx.draw(K2_real, with_labels = True, node_color = "m")
plt.title("Group Instructor", fontweight = "bold")

plt.show()
```

```{code-cell} ipython3
print("Graph administrator has :", len(K1_real.nodes), " nodes")
print("Graph instructor has :",len(K2_real.nodes), " nodes")

print("Karate club graph has: " , len(K.edges), " edges")
print("After the partition there are " , len(K2_real.edges) +len(K1_real.edges), " edges left")
```

### Compare the partitions: naive vs fiedler vector vs real
The first question is: are the partitions isomorphic with the real cut? It's reasonable to think that they won't be isomorphic but it is still valuable to check. We already know that the naive partitions won't be isomorphic with the real ones because they have isolated nodes. But let's see if the Fiedler vector partitions are isomorphic with the real ones.
 

```{code-cell} ipython3
print("Are isomorphic the graphs corresponding to the administrator? ", nx.is_isomorphic(K1, K1_real))
print("Are isomorphic the graphs corresponding to the instructor? ", nx.is_isomorphic(K2, K2_real))
```


One way to measure if the partitions are similar is by using the correlation between the label vectors. We can think of the labels are vectors in the $\mathbb{R}^{34}$ and the correlation will tell us how similar are these vectors.The correlation is calculated as:

$$ corr(X, Y) = \frac{\sum_{i = 0}^{|X|}{(x_i - \bar{x})(y_i - \bar{y}) }}{ 
\sqrt{ \sum_{i=0}^{|X|}{(x_i - \bar{x})^2}}  \sqrt{\sum_{i=0}^{|Y|}{(y_i - \bar{y})^2})}}$$

where $\bar{x}$ is the mean of $X$ and $\bar{y}$ is the mean of $Y$. 

```{code-cell} ipython3
#create labels vector for the naive and fiedler vector partitions
partition_naive = np.zeros(34)
partition_fiedler = np.zeros(34)
for n in range(34): 
    partition_naive[n] = n < 17 
    partition_fiedler[n] = fiedler_vec[n] >= 0
    
print("Naive vs fiedler vector correlation: ", abs(np.corrcoef(partition_fiedler, partition_naive)[0, 1]))
print("Real vs naive correlation: ", abs(np.corrcoef(real_cut, partition_naive)[0, 1]))

print("Real vs fiedler vector correlation: ", abs(np.corrcoef(real_cut, partition_fiedler)[0,1]))
```

Finally, we could test that the partition generated with the Fiedler vector is pretty similar to the real one. Even when the partitions are not exactly the same we can observe that they have a pretty good correlation which means they are very close. As expected, the naive approach doesn't seem to be an accurate way to partition the graph. Also, the naive partition is more similar to the real cut than it is to the Fiedler vector partition. 

+++

### Final conclusions
After all the experiments we can conclude that:
1) The degree centrality and eigenvector centrality can be used to identify the most influential nodes in the graph.
2) The Laplacian matrix is a great way to represent a graph that can be used in methods to partition the graph. In this case, we could observe in the matrix some properties that lead to a naive way to partition the graph.  
3) The naive approach is simple but in this case the solution is not accurate enough. But it is a valuable experiment because it let us check that the results regarding the partition obtained using the Fiedler vector are in fact better. 
4) The Fiedler vector can partition the Karate club graph very well compared to the real partition.

#### Further questions
- The Laplacian matrix has many eigenvectors how do they partition the graph? Is there any other eigenvector that partition well this particular graph? 
- There are other methods to generate partitions using flow algorithms. How do that partitions compare to the ones that we generated in this notebook? 
- Is there some other method to compare the partitions? 

+++

## References

- Zachary’s Karate Club graph source: http://vlado.fmf.uni-lj.si/pub/networks/data/Ucinet/UciData.htm#zachary
- Zachary W. (1977). "An information flow model for conflict and fission in small groups" Journal of Anthropological Research, 33, 452-473.
<https://www.jstor.org/stable/3629752>
