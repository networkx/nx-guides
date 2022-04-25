---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3
  name: python3
---

+++ {"id": "jrizb5yufXBG"}

# **Lowest Common Ancestor**


In this tutorial, we will explore the lowest common ancestor algorithm implemented in networkx under `networkx/algorithms/lowest_common_ancestor.py`. 

## Definitions

Before diving into the algorithm, let's first remember the concepts of an ancestor node and a descendant node.

- **Ancestor:** 
Given a rooted tree, any node $u$ which is on the path from root node to $v$ is an ancestor of $u$. 

- **Descendant:**  A descendant of a node is either a child of the node or a child of some descendant of the node.
- **Lowest Common Ancestor:** For two of nodes $u$ and $v$ in a tree, the lowest common ancestor is the lowest (i.e. deepest) node which is an ancestor of both $u$ and $v$. 

+++ {"id": "Z5VJ4S_mlMiI"}

## Example

It is always a good idea to learn concepts on an example. Consider the following evalutionary tree. We will draw directed version of it and define the ancestor/descendant relationships.

![image:evolutionary tree](images/evolutionary_tree.png)

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
id: FdGHBPT-ublJ
outputId: 49272870-d3b9-4715-8bff-682def5293ec
---
!pip install pydot
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from itertools import chain, count
```

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 258
id: UDDayA6giYRI
outputId: 2f453fe6-2809-4587-d6f5-4a445441e352
---
T = nx.DiGraph()
T.add_edges_from([("Vertabrate","Lamprey"),("Vertabrate","Jawed V."),
                  ("Jawed V.","Sunfish"),("Jawed V.","Tetrapod"),
                  ("Tetrapod","Newt"),("Tetrapod","Amniote"),("Amniote","Lizard"),
                  ("Amniote","Mammal"),("Mammal","Bear"), ("Mammal", "Chimpanzee")])
pos = graphviz_layout(T, prog="dot")
plt.figure(3,figsize=(16,6))
nx.draw(T, pos, with_labels=True, node_size=4000, node_color='brown', font_size = 11, font_color = "White")
plt.show()
```

+++ {"id": "MziCQi2akACo"}

Consider the tree above and observe the following relationships:

- **Ancestors of node $Mammal$**:  
  - For this, we will follow the path from root to node $Mammal$.
  - Nodes $Vertabrate$, $Jawed$ $Vertabrate$, $Tetrapod$ and $Amniote$ -which are on this path- are ancestors of $Mammal$.
- **Descendants of node $Mammal$**:
    - $Bear$ and $Chimpanzee$ are the child of $Mammal$. Thus,they are its descendants.
- **Lowest Common Ancestor of $Mammal$ and $Newt$**:
  - Ancestors of $Mammal$ are $Vertabrate$, $Jawed$ $Vertabrate$, $Tetrapod$ and $Amniote$.
  - Ancestors of $Newt$ are $Vertabrate$, $Jawed$ $Vertabrate$, and $Tetrapod$.
  - Among the common ancestors, the lowest (i.e. farthest away from the root) one is $Tetrapod$.


_Note that every node is both an ancestor and descendant of itself._


+++ {"id": "8CdjSmPZDn7s"}

It is also possible to find lowest common ancestors for all pairs of nodes using `all_pairs_lowest_common_ancestor()` method implemented in NetworkX. You can run the below cell to see it yourself!



```{code-cell}
:id: Q64EdW8EDnb9

dict(nx.all_pairs_lowest_common_ancestor(T))
```

+++ {"id": "mjEM8pgNolIo"}

## Ancestor-List Algorithm

NetworkX uses [Ancestor-List](https://www3.cs.stonybrook.edu/~bender/pub/JALG05-daglca.pdf) algorithm to find lowest common ancestor of all pairs of nodes. We will introduce it here step by step using a simple directed acyclic graph.

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 247
id: KHfCRDdjipmQ
outputId: 70dfaeec-a96c-4796-ecca-a66c3077f56f
---
# Generating and visualizing our DAG
G = nx.DiGraph()
G.add_edges_from([(1, 0), (2, 0), (3, 2), (4, 1), (4, 3),(5,6)])
pos = graphviz_layout(G, prog="dot")
plt.figure(3,figsize=(5,3))
nx.draw(G, pos, with_labels=True, node_size=1500, node_color='darkgreen', font_size = 14, font_color = "White")
plt.show()
```

+++ {"id": "bnLcpToCnyCj"}

###Step 1
Add a node $v$ to the directed acyclic graph $G$, and add directed edges from $v$ to sources with no incoming edges in $G$. The addition of $v$ guarantees that every two nodes have an LCA. If $v$ is reported as a representative $LCA$ for a pair of nodes, then these nodes have no common ancestors in $G$.

```{code-cell}
:id: 6zJtLRXfcWu0

sources = [n for n, deg in G.in_degree if deg == 0]
if len(sources) == 1:
    root = sources[0]
    super_root = None
else:
    G = G.copy()
    # find unused node
    root = -1
    while root in G:
        root -= 1
    # use that as the super_root below all sources
    super_root = root
    for source in sources:
        G.add_edge(root, source)
```

+++ {"id": "uB7T9PNVnqHa"}

Observe that super root $-1$ connected components in our graph. 

```{code-cell}
---
colab:
  base_uri: https://localhost:8080/
  height: 319
id: KTJgQuB-nrQN
outputId: c7eaf69a-ebdf-47e3-df84-f6c3259462a4
---
nx.draw(G, with_labels=True, node_size=1500, node_color='darkgreen', font_size=14, font_color="White")
```

+++ {"id": "Je365ItTG7Ri"}

### Step 2

Preprocess $G$ by partitioning the set of edges into two sets: $S_1$ is the set of edges of a spanning tree $T$ of $G$, and $S_2$ is composed of the remaining edges, which make up the $DAG$ $D = (V, S_2)$.

```{code-cell}
:id: A4ze0sRHnfkT

spanning_tree = nx.dfs_tree(G, root)
dag = nx.DiGraph(
    (u, v)
    for u, v in G.edges
    if u not in spanning_tree or v not in spanning_tree[u]
)

# Ensure that both the dag and the spanning tree contains all nodes in G,
# even nodes that are disconnected in the dag.
spanning_tree.add_nodes_from(G)
dag.add_nodes_from(G)
```

```{code-cell}
:id: tIqgHDjKoxaT

# TO BE CONTINUED
```

+++ {"id": "h1Njv6-9n6JE"}

## References

M. A. Bender, M. Farach-Colton, G. Pemmasani, S. Skiena, P. Sumazin. “Lowest common ancestors in trees and directed acyclic graphs.” Journal of Algorithms, 57(2): 75-94, 2005.
