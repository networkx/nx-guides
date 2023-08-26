---
jupytext:
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Graph Traversal Algorithms

+++

In this guide, we will explore graph traversal algorithms implemented under [networkx/algorithms/traversal.py](https://networkx.org/documentation/stable/reference/algorithms/traversal.html), mainly breadth-first search (BFS) and depth-first search (DFS).

+++

## Import packages

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from IPython.display import clear_output, display
import time
```

## Introduction

A graph traversal is also known as a graph search. 

There are many scenarios in which searching a graph is of interest. Consider, for example, you are at one node and want to search for another. You could also be interested in starting from one node and travelling to all other nodes to check some property or to do some operation. 


A concrete example is below. In the below graph, starting from the green vertex is there some way to get to the red? This is can example of a search problem.

```{code-cell} ipython3
G = nx.Graph()
G.add_edges_from(
    [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (3, 6), (3, 7), (4, 8), (7, 8), (8, 9)]
)
pos = nx.spectral_layout(G)
node_colors = [
    "green" if node == 2 else "red" if node == 9 else "blue" for node in G.nodes
]
nx.draw(
    G,
    pos,
    with_labels=True,
    font_color="white",
    node_color=node_colors,
    node_size=500,
    font_size=10,
    font_weight="bold",
)
plt.show()
```

Given this, what procedure should we use to search/traverse a graph? There are 2 major ways to do this: BFS and DFS. 

## BFS

+++

Consider the problem from above. Starting from node 2 in green, how do we search for node 9 in red?

+++

One way to go about it is as follows: from a start node, check all neighbors of that node. Repeat for each neighbor (i.e. checking all of its neighbors), and on and on. In the process, ensure you only visit nodes that have not already been visited. Intuitively, you are searching in a 'breadth-first' fashion: checking all the neighbors of vertices (surveying all your options) without committing to a single 'branch' and deep diving into it. See the pseudocode below:

+++

```python
def BFS(G, start, goal):
    """Return whether a path from start to goal exists, 
    Q = [start]  # create a queue
    seen = {start}  # store the nodes as we visit them
    while Q:
        v = Q.pop(0)  # FIFO queue
        if v in seen:
            continue
        if v == goal:
            return True
        for w in G[v]:
            if w not in explored:
                seen.add(w)
                Q.append(w)
    return False
```

+++

Note the use of a queue...its first-in first-out (FIFO) nature enables remembering the next vertex to start a search at. We also mark vertices as explored to ensure we do not visit them again.

Here is an example animation for BFS: each explored 'layer' is marked with a different color. Notice how we check all neighbors for each vertex, with committing to a single path. 

Do not worry about the code here, we will explore networkx's implementations further later

```{code-cell} ipython3
def animate_bfs(G, start_node):
    pos = nx.spring_layout(G)

    fig, ax = plt.subplots(figsize=(12, 9))

    node_colors = {node: "skyblue" for node in G.nodes}

    visited = set()
    queue = [start_node]
    layers = list(nx.bfs_layers(G, start_node))

    for layer_idx, layer in enumerate(layers):
        next_layer = []

        for node in layer:
            if node not in visited:
                visited.add(node)
                node_colors[node] = mcolors.hsv_to_rgb(
                    (layer_idx / len(layers), 0.7, 0.9)
                )
                next_layer.extend(G.neighbors(node))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=[node_colors[node] for node in G.nodes],
            node_size=1000,
            font_size=10,
            font_weight="bold",
            ax=ax,
        )

        clear_output(wait=True)
        display(fig)
        time.sleep(1)

        queue = next_layer

    clear_output(wait=True)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=[node_colors[node] for node in G.nodes],
        node_size=1000,
        font_size=10,
        font_weight="bold",
    )
    plt.show()


# Example usage with a larger graph
G = nx.Graph()
G.add_edges_from(
    [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (1, 5),
        (3, 6),
        (3, 7),
        (4, 8),
        (7, 8),
        (8, 9),
        (2, 10),
        (2, 11),
        (10, 12),
        (10, 13),
        (12, 14),
        (12, 15),
        (5, 16),
        (5, 17),
        (16, 18),
        (16, 19),
        (18, 20),
        (18, 21),
        (7, 22),
        (7, 23),
        (22, 24),
        (22, 25),
    ]
)

# Start the BFS animation from the root node (node 0)
animate_bfs(G, start_node=0)
```

## Using NetworkX for BFS

Now that we understand BFS, what functionality does NetworkX provide for BFS?

We have six use cases. 
- bfs_layers
- bfs_edges
- bfs_tree
- bfs_predecessors
- bfs_successors
- descendants_at_distance


bfs_layers returns an iterator of all the 'layers' of a BFS: that is all the vertices that are on the same level (i.e. distance) from the root. BFS operates layer by layer. We use bfs_layers in the above to color the nodes at each layer

We can use bfs_edges to explicitly show all the edges that are traversed in the above graph during a BFS. Check it out below. It matches our animation!

```{code-cell} ipython3
bfs_edges_result = list(nx.bfs_edges(G, 0))
print("Edges traversed during BFS traversal:")
for edge in bfs_edges_result:
    print(edge)
```

bfs_tree creates a "traversal" tree that shows what vertices were traversed in what order. It is a representation of the BFS, and must always be a tree because BFS visits no vertex twice (we ensure that doesn't happen by keeping track of what vertices are explored in the traversal)

```{code-cell} ipython3
start_node = 0
bfs_tree = nx.bfs_tree(G, start_node)

# Draw the BFS tree
pos = nx.spring_layout(G)  # Layout the original graph nodes using spring layout
plt.figure(figsize=(12, 9))
nx.draw(
    bfs_tree,
    pos,
    with_labels=True,
    node_size=1000,
    font_size=10,
    font_weight="bold",
    alpha=0.6,
    node_color="skyblue",
    width=2,
)

# Draw the BFS tree edges with a different color and width to distinguish it from the original graph

plt.title("BFS Tree")
plt.show()
```

bfs_successor and bfs_predecessor both generate node-neighbor_list pairs where neighbors are the successors and predecessors, respectively. Below, we use these functions to reconstruct the graph. As you can see, in the graph on the left all edges are from nodes to their predecessors (and thus we have the BFS tree but all edges reversed). In the graph on the right all edges are from nodes to their successors (and thus we have the BFS tree)


Finally, we have descendants_at_distance, which is a useful way of identifying all nodes at a fixed distance from a source in G. It uses BFS (remember, layer number is the same as distance from the root) to do so. In our example graph, supposed I am at node 9 and want to find all nodes 2 edges away, because I can only travel two edges. I do so as below!

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt

import networkx as nx
import matplotlib.pyplot as plt

# Create the graph G
G = nx.Graph()
G.add_edges_from(
    [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (1, 5),
        (3, 6),
        (3, 7),
        (4, 8),
        (7, 8),
        (8, 9),
        (2, 10),
        (2, 11),
        (10, 12),
        (10, 13),
        (12, 14),
        (12, 15),
        (5, 16),
        (5, 17),
        (16, 18),
        (16, 19),
        (18, 20),
        (18, 21),
        (7, 22),
        (7, 23),
        (22, 24),
        (22, 25),
    ]
)

# Find vertices at distance 2 from vertex 0
vertices_at_distance_2 = nx.descendants_at_distance(G, source=0, distance=2)

# Draw the graph G
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)

# Draw all vertices in blue
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="blue", alpha=0.6)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.6)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

# Highlight vertices at distance 2 in red
nx.draw_networkx_nodes(
    G, pos, nodelist=vertices_at_distance_2, node_size=500, node_color="red", alpha=0.8
)

plt.title("Graph G with Vertices at Distance 2 from Vertex 0 Highlighted in Red")
plt.axis("off")
plt.show()
```

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt

# Create the graph G
G = nx.Graph()
G.add_edges_from(
    [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (1, 5),
        (3, 6),
        (3, 7),
        (4, 8),
        (7, 8),
        (8, 9),
        (2, 10),
        (2, 11),
        (10, 12),
        (10, 13),
        (12, 14),
        (12, 15),
        (5, 16),
        (5, 17),
        (16, 18),
        (16, 19),
        (18, 20),
        (18, 21),
        (7, 22),
        (7, 23),
        (22, 24),
        (22, 25),
    ]
)

# Perform BFS starting from node 0
start_node = 0
predecessors = dict(nx.bfs_predecessors(G, start_node))
successors = dict(nx.bfs_successors(G, start_node))

# Create a new graph for the BFS tree with predecessor edges
BFS_predecessor_tree = nx.DiGraph()

# Add the nodes from G to BFS_predecessor_tree
BFS_predecessor_tree.add_nodes_from(G.nodes)

# Add predecessor edges
for node, pred in predecessors.items():
    if pred is not None:
        BFS_predecessor_tree.add_edge(node, pred, directed=True)

# Create a new graph for the BFS tree with successor edges
BFS_successor_tree = nx.DiGraph()

# Add the nodes from G to BFS_successor_tree
BFS_successor_tree.add_nodes_from(G.nodes)

# Add successor edges
for node, succ in successors.items():
    for s in succ:
        BFS_successor_tree.add_edge(node, s, directed=True)

# Draw G with predecessor edges
plt.figure(figsize=(15, 4))
plt.subplot(1, 2, 1)
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx(
    BFS_predecessor_tree,
    pos,
    with_labels=True,
    node_size=150,
    arrows=True,
    node_color="skyblue",
    edge_color="blue",
    width=2,
    arrowstyle="->",
    arrowsize=9,
)
plt.title("Graph G with Predecessor Edges")
plt.axis("off")

# Draw G with successor edges
plt.subplot(1, 2, 2)
nx.draw_networkx(
    BFS_successor_tree,
    pos,
    with_labels=True,
    node_size=150,
    arrows=True,
    node_color="skyblue",
    edge_color="red",
    width=2,
    arrowstyle="->",
    arrowsize=9,
)
plt.title("Graph G with Successor Edges")
plt.axis("off")

plt.tight_layout()
plt.show()
```

## DFS

One way to approach it is as follows: from a start node, explore one of its neighbors and continue exploring further down that branch as deep as possible before backtracking. Repeat this process for each unvisited neighbor, going deeper into each branch before returning to explore other unvisited options. In this manner, you are searching in a 'depth-first' fashion, delving deeply into one branch at a time. See the pseudocode below:

+++

```
// ITERATIVE APPROACH    
    dfs-iterative (G, src):    //Where G is graph and src is source vertex
        let st be stack
        st.push(src)             //Inserting src in stack 
        mark s as visited
        while (st is not empty):
            //Pop a vertex from stack to visit next
            v  =  st.top( )
            st.pop( )
            //Push all the neighbours of v in stack that are not visited   
            for all neighbours w of v in Graph G:
                if w is not visited :
                    st.push(w)         
                    mark w as visited


// RECURSIVE APPROACH
    dfs-recursive(G, src):
        mark src as visited
        for all neighbours w of src in Graph G:
            if w is not visited:
                DFS-recursive(G, w)
```

+++

The iterative approach uses an explicit stack to keep track of vertices. It starts by pushing the source vertex onto the stack and marking it as visited. While the stack is not empty, the algorithm pops a vertex from the top of the stack, processes it, and then pushes its unvisited neighbors onto the stack. This process continues until the stack is empty, ensuring deep exploration along each branch.

On the other hand, in the recursive approach the algorithm starts with a source vertex. It marks the vertex as visited and then recursively calls itself for each unvisited neighbor. This recursive process allows the algorithm to explore each branch deeply before backtracking to explore other neighbors.

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from IPython.display import clear_output, display
import time


def animate_dfs(G, start_node):
    pos = nx.spring_layout(G)

    fig, ax = plt.subplots(figsize=(12, 9))

    node_colors = {node: "skyblue" for node in G.nodes}

    visited = set()

    def dfs(node):
        visited.add(node)
        node_colors[node] = "yellow"
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=[node_colors[node] for node in G.nodes],
            node_size=1000,
            font_size=10,
            font_weight="bold",
            ax=ax,
        )

        clear_output(wait=True)
        display(fig)
        time.sleep(1)

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start_node)

    clear_output(wait=True)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=[node_colors[node] for node in G.nodes],
        node_size=1000,
        font_size=10,
        font_weight="bold",
    )
    plt.show()


# Example usage with the same larger graph
G = nx.Graph()
G.add_edges_from(
    [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (1, 5),
        (3, 6),
        (3, 7),
        (4, 8),
        (7, 8),
        (8, 9),
        (2, 10),
        (2, 11),
        (10, 12),
        (10, 13),
        (12, 14),
        (12, 15),
        (5, 16),
        (5, 17),
        (16, 18),
        (16, 19),
        (18, 20),
        (18, 21),
        (7, 22),
        (7, 23),
        (22, 24),
        (22, 25),
    ]
)

# Start the DFS animation from the root node (node 0)
animate_dfs(G, start_node=0)
```

Note how we dive deeply into a branch before moving on to another branch, instead of moving out in levels like BFS

+++

## Using NetworkX for DFS

Now that we understand DFS, what functionality does NetworkX provide for DFS?

We have six use cases. 
- dfs_edges
- dfs_tree
- dfs_predecessors
- dfs_successors
- dfs_labelled_edges
- dfs_preorder_nodes
- dfs_postorder_nodes
- descendants_at_distance

dfs_predecessors and dfs_successors do essentially the same as their BFS counterparts but with BFS, so we'll ignore those for now. Likewise, dfs_tree simply builds a tree corresponding to the DFS traversal and descendants_at_distance does the same as its BFS counterpart, just using DFS as a base to traverse.

As such, we will focus on the remaining: dfs_edges, dfs_labelled_edges, and the preorder and postorder node functions.

We can dfs_edges to explicitly show all the edges that are traversed in the above graph during a DFS. Check it out below. It matches our animation as well!

```{code-cell} ipython3
dfs_edges_result = list(nx.dfs_edges(G, 0))
print("Edges traversed during BFS traversal:")
for edge in dfs_edges_result:
    print(edge)
```

```{code-cell} ipython3
G = nx.DiGraph([(0, 1), (1, 2), (2, 1)])
# Label the edges using dfs_labeled_edges

edge_labels = {(u, v): d for u, v, d in nx.dfs_labeled_edges(G, source=0)}

print(list(nx.dfs_labeled_edges(G, source=0)))

# Draw the graph with labeled edges
pos = nx.random_layout(G, seed=42)

plt.figure(figsize=(8, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1000,
    node_color="skyblue",
    arrowsize=10,
    font_size=10,
    font_weight="bold",
)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_size=8, font_weight="bold"
)
plt.title("Example Graph with Labeled Edges using DFS")
plt.axis("off")
plt.show()
```

As per the documentation, a ‘forward’ edge is one in which u has been visited but v has not. A ‘nontree’ edge is one in which both u and v have been visited but the edge is not in the DFS tree. A ‘reverse’ edge is one in which both u and v have been visited and the edge is in the DFS tree. 

Note the reverse and nontree edges in the above illustrative example. 


Finally, can take a look at dfs_postorder and dfs_preorder.

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt

# Create a simple graph
G = nx.DiGraph()
G.add_edges_from(
    [(1, 2), (1, 3), (2, 4), (2, 5), (1, 6)]
)  # Adding vertex 6 and connecting to vertex 1

# Draw the graph on the left with DFS postorder node labels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

postorder_nodes = list(nx.dfs_postorder_nodes(G, source=1))
pos1 = nx.spectral_layout(G)
nx.draw(
    G,
    pos1,
    with_labels=True,
    node_color="skyblue",
    node_size=1000,
    font_size=0,
    font_weight="bold",
    ax=ax1,
    arrows=True,
)
ax1.set_title("Graph with DFS Postorder Node Labels")

# Draw the graph on the right with DFS preorder node labels
preorder_nodes = list(nx.dfs_preorder_nodes(G, source=1))
pos2 = nx.spectral_layout(G)
nx.draw(
    G,
    pos2,
    with_labels=True,
    node_color="skyblue",
    node_size=1000,
    font_size=0,
    font_weight="bold",
    ax=ax2,
    arrows=True,
)
ax2.set_title("Graph with DFS Preorder Node Labels")

# Label nodes with DFS postorder and preorder numbers
node_labels_postorder = {node: f"{i}" for i, node in enumerate(postorder_nodes, 1)}
node_labels_preorder = {node: f"{i}" for i, node in enumerate(preorder_nodes, 1)}

nx.draw_networkx_labels(
    G,
    pos1,
    labels=node_labels_postorder,
    font_size=10,
    font_color="red",
    font_weight="bold",
    ax=ax1,
)
nx.draw_networkx_labels(
    G,
    pos2,
    labels=node_labels_preorder,
    font_size=10,
    font_color="red",
    font_weight="bold",
    ax=ax2,
)

plt.tight_layout()
plt.show()
```

DFS postorder is an ordering in which we visit a node's children first before processing the node itself. Starting from the source node, we traverse deeper into the graph, visiting all the child nodes before processing the current node. Once all the child nodes are visited, we backtrack and process the current node. This order is often used to compute the size of subtrees and perform tasks that depend on information from the children.

On the other hand, DFS preorder is an ordering in which we process the current node before visiting its children. We start from the source node, process it, then move to its first child, process it, and so on, until all children are processed. Only then do we backtrack and continue processing other children of the parent node. This order is useful for tasks that require processing nodes before their children, such as copying the entire tree structure.

+++

## Applications of BFS and DFS

+++

Breadth-First Search (BFS) and Depth-First Search (DFS) are fundamental graph traversal algorithms that find numerous applications in computer science and various real-world scenarios.

BFS is commonly used for finding the shortest path between two nodes in an unweighted graph. It systematically explores the graph layer by layer, guaranteeing that the first path discovered is the shortest one. Beyond path finding, BFS also helps analyze the connectivity of a graph. By starting from a source node and visiting all reachable nodes, BFS can determine whether the graph is connected or contains isolated components.

In networking, BFS plays a crucial role in routing protocols. By finding the shortest path between devices on a network, BFS ensures efficient data transmission with minimal delays and hops. Web crawling is another application of BFS, where it facilitates systematic exploration of web pages, beginning from a specific webpage and gradually discovering linked pages layer by layer.

Conversely, DFS is highly efficient for exploring all nodes in a graph. It excels in various graph traversal tasks, enabling the identification of connected components, cycles, and other structural properties. DFS is particularly valuable in topological sorting of directed acyclic graphs (DAGs). The algorithm orders the nodes in a manner that preserves dependencies, making it widely used in tasks like scheduling and project planning.

DFS finds its place in solving mazes and puzzles as well. By exploring different possible paths systematically, DFS can find solutions to puzzles where the goal is to reach a specific destination. Additionally, DFS is utilized in detecting cycles in a graph, aiding in various applications such as deadlock detection in operating systems and identifying circular dependencies in software design.


## References

[^1]:  Depth-First Search (DFS). (n.d.). University of Toronto - Computer Science. Retrieved from [http://www.cs.toronto.edu/~heap/270F02/node36.html](http://www.cs.toronto.edu/~heap/270F02/node36.html)

[^2]:  Applications of Depth-First and Breadth-First Search. (n.d.). York University - Department of Electrical Engineering and Computer Science. Retrieved from [https://wiki.eecs.yorku.ca/course_archive/2012-13/S/2011/_media/22Apps.pdf](https://wiki.eecs.yorku.ca/course_archive/2012-13/S/2011/_media/22Apps.pdf)

[^3]:  Depth-first search. (2021, September 16). In Wikipedia, The Free Encyclopedia. Retrieved July 30, 2023, from [https://en.wikipedia.org/wiki/Depth-first_search](https://en.wikipedia.org/wiki/Depth-first_search)

[^4]:  Breadth-first search. (2021, September 17). In Wikipedia, The Free Encyclopedia. Retrieved July 30, 2023, from [https://en.wikipedia.org/wiki/Breadth-first_search](https://en.wikipedia.org/wiki/Breadth-first_search)

[^5]:  NetworkX. (2021, August 29). Traversal — NetworkX documentation. Retrieved July 30, 2023, from [https://networkx.org/documentation/stable/reference/traversal.html](https://networkx.org/documentation/stable/reference/traversal.html)

[^6]:  Wikipedia. Lowest common ancestor. [https://en.wikipedia.org/wiki/Lowest_common_ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor)
