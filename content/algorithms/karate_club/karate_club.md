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

The network has 34 nodes, one for each member of the karate club, and the edges represent the relationships between the pairs of members who interacted outside the club. During the study, there was a conflict between the administrator "John A"(node 1) and instructor "Mr. Hi" (node 34), which led to the split of the club into two. Half of the members formed a new club around Mr. Hi; members from the other part found a new instructor or gave up karate. We will use different methods to cut this graph and then compare our results with the actual split that happened in the real situation. 

### Let's explore this graph
First, we can draw this graph with different layouts to understand some initial properties. 
TODO: explaind layouts and what can we see

```{code-cell}
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

K = nx.karate_club_graph()

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 10)

plt.subplot(221)

plt.title("Spring layout", fontweight = "bold")
nx.draw_spring(K, with_labels = True, node_color = "c") #Spring layout

plt.subplot(222)
plt.title("Circular layout", fontweight = "bold")
nx.draw_circular(K, with_labels = True, node_color = "m") #Circular layout 
```

Another great way to identify the nodes with more connections is by using the **degree centrality**.
TODO: explaind more

```{code-cell}
#TODO: add colorbar 
import matplotlib.cm as cm
from matplotlib.colors import Normalize, rgb2hex

def color_map_color(value, cmap_name="plasma", vmin=0, vmax=1):
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)
    rgb = cmap(norm(abs(value)))[:3]
    color = rgb2hex(rgb)
    return color

degrees = list(nx.degree_centrality(K).values())

degree_colors = [color_map_color(degrees[i]) for i in range(34)] #Translate the degree value of each node into a value 
                                                           #that can be interpreted as a color

plt.bar(x = list(range(0,  34)), height= degrees, color = degree_colors)
plt.title("Degree centrality of the Karate club", fontweight = "bold")
plt.xlabel("Node labels")
plt.show()
```

In the previous plot we can again identify that the nodes 0 and 34 corresponding to the administrator and the instructor are the ones with higher degree centrality.

```{code-cell}
degrees = list(nx.eigenvector_centrality(K).values())

degree_colors = [color_map_color(degrees[i]) for i in range(34)] #Translate the degree value of each node into a value 
                                                           #that can be interpreted as a color

plt.bar(x = list(range(0,  34)), height= degrees, color = degree_colors)
plt.title("Eigvector centrality of the Karate club", fontweight = "bold")
plt.xlabel("Node labels")
plt.show()
```

Voterank. TODO: Explaind

```{code-cell}
nx.voterank(K, 2)
```

## Matrix representation: Laplacian Matrix 
The laplacian matrix of a graph is a matrix representation of a graph. The matrix is defined as 

$$ L_{i,j} =  
\begin{cases}
deg(i) &  i = j\\
-1 & \text{there's an edge between } v_i \text{ and } v_j \\
0  & else
\end{cases}
$$

Also can be express as $L = D - A$ where $D$ is a diagonal matrix with the degree of each node and $A$ is the adjancency matrix. 

The Laplacian matrix is particularly interesting because it captures information not only about the specific connections between the nodes but also about the amount of them. In other words, this matrix also captures information about the centrality of the nodes in the network. 

TODO: add some applications of this matrix in chemistry. 

Let's see what the laplacian matrix of a small matrix looks like:

```{code-cell}
G = nx.barbell_graph(3, 1) #Two complete graphs of 3 nodes connected with a path of 1 node
nx.draw(G)

print(nx.laplacian_matrix(G).toarray())
```

A great way to visualize all the values from the matrix is by using a heatmap. Let's visualize the Laplacian Matrix of the Karate club graph.

```{code-cell}
#TODO: test other colorgradients 

L = nx.laplacian_matrix(K)

fig, ax = plt.subplots()
im = ax.imshow(L.toarray(), cmap = "plasma")

ax.set_title("Laplacian Matrix of the Karate Club Graph", fontweight = "bold")
plt.colorbar(im)
plt.show()
```

In this heatmap we can see that almost all pair of nodes are connected. TODO: Add about the diagonal

+++

TODO: add some cool math properties of the laplacian matrix

+++

## Algebraic connectivity and Fiedler vector 

The algebraic connectivity of a graph G is the second-smallest eigenvalue (counting multiple eigenvalues separately) of its Laplacian matrix.

The Fiedler vector of a connected undirected graph is the eigenvector corresponding to the second smallest eigenvalue of the Laplacian matrix of the graph.

TODO: Explaind more 

Cut the graph in half:

```{code-cell}
alg_connectivity = nx.algebraic_connectivity(K)
print("Algebraic connectivity: " , alg_connectivity)
```

```{code-cell}
fiedler_vec = nx.fiedler_vector(K)
K1 = nx.karate_club_graph()
K2 = nx.karate_club_graph()

K1.remove_nodes_from(list(n for n in K1.nodes if fiedler_vec[n] >= 0))
K2.remove_nodes_from(list(n for n in K2.nodes if fiedler_vec[n] < 0))
```

```{code-cell}
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 10)

plt.subplot(221)
nx.draw(K1, with_labels = True, node_color = "g")
plt.title("Group Administrator", fontweight = "bold")

plt.subplot(222)
nx.draw(K2, with_labels = True)
plt.title("Group Instructor", fontweight = "bold")

plt.show()
```

### Real Cut

```{code-cell}
import pandas as pd
real_cut = list(pd.read_csv("karateclub_labels.txt", names = ["group"])["group"])

K1_real = nx.karate_club_graph()
K2_real = nx.karate_club_graph()

K1_real.remove_nodes_from(list(n for n in K1_real.nodes if real_cut[n] == 1))
K2_real.remove_nodes_from(list(n for n in K2_real.nodes if real_cut[n] == 0))

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 10)

plt.subplot(221)
nx.draw(K1_real, with_labels = True, node_color = "g")
plt.title("Group Administrator", fontweight = "bold")

plt.subplot(222)
nx.draw(K2_real, with_labels = True)
plt.title("Group Instructor", fontweight = "bold")

plt.show()
```

**Comparison with Real Cut**

```{code-cell}
print(nx.is_isomorphic(K1, K1_real))
print(nx.is_isomorphic(K2, K2_real))
```

```{code-cell}
##Add correlation between labels and fiedler vector 
```

```{code-cell}
# nx.prominent_group(K1)
```

Use flow to cut the network with a different method

+++

## References

- Add dataset sources
