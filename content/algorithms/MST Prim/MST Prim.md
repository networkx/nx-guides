---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Minimum Spanning Tree using Prim's Algorithm


We all have travelled by road from one city to another. But, ever wondered how they decided where to create the route and what path to choose? If one will get the job to connect 5 cities via road, then, the naive approach will be to start connecting from one city and continue doing that until one covers all destinations. But, that's not the optimal solution, not only one should cover all nodes but also at the lowest cost possible (minimum length of the road) and for that <b>Minimum Spanning Trees</b> are constructed using Prim's and Kruskal's algorithm.

When each and every node of a graph is connected to each other without forming any cycle, it is known as the <b>Spanning Tree.</b> A graph $G$ having $n$ nodes will have spanning trees with $n$ nodes and $n-1$ edges. Thus, as its name indicates, Minimum Spanning Tree is the tree with the shortest possible distance covered among all other spanning trees.<br> Let's look at the following example to understand this better.


## Minimum Spanning Tree Problem


Suppose there are 5 cities (A, B, C, D and E) that needs to be connected via road. Now, there can be more than one path connecting one city to another but our goal is to find the one having the shortest distance.

<b>ASSUMPTION</b>: Distance taken is imaginary.

The following graph depicts our situation in this case.

```python
# importing libraries
import networkx as nx
import matplotlib.pyplot as plt

roads = nx.Graph()

# adding weighted edges
roads.add_weighted_edges_from(
    [
        ("A", "B", 1),
        ("A", "C", 7),
        ("B", "C", 1),
        ("B", "D", 4),
        ("B", "E", 3),
        ("C", "E", 6),
        ("D", "E", 2),
    ]
)

# layout of the graph
position = {"A": (0.5, 2), "B": (0, 1), "C": (1, 1), "D": (0, 0), "E": (1, 0)}
pos = nx.spring_layout(
    roads, pos=position, weight="weight", fixed=["A", "B", "C", "D", "E"]
)
fig = plt.figure(figsize=(5, 5))

# drawing customised nodes
nx.draw(
    roads,
    pos,
    with_labels=True,
    node_size=900,
    node_color="#DF340B",
    font_color="white",
    font_weight="bold",
    font_size=14,
    node_shape="s",
)

# adding edge labels
nx.draw_networkx_edge_labels(
    roads,
    pos,
    edge_labels=nx.get_edge_attributes(roads, "weight"),
    font_size=12,
);

```

Now, in order to find the minimum spanning tree, this notepad will cover the Prim's algorithm.
Let's understand it in detail.


## Prim's Algorithm
Prim's algorithm uses greedy approach to find the minimum spanning tree.That means, in each iteration it finds an edge which has the minimum weight and add it to the growing spanning tree.

The time complexity of the Prim’s Algorithm is $O((V+E) \text{ log} V)$  because each vertex is inserted in the priority queue only once and insertion in priority queue take logarithmic time.

<b>Algorithm Steps</b>
1. Select any arbitrary node as the root node and add it to the tree. Spanning tree will always cover all nodes so any node can be a root node.
2. Select the node having the minimum edge weight among the outgoing edges of the nodes present in the tree. Ensure the node is not already present in the spanning tree.
3. Add the selected node and edge to the tree.
4. Repeat steps 2 and 3 until all nodes are covered.
5. The final graph will represent the Minimum Spanning Tree


### Example solution
Let's get back to the example and find its minimum spanning tree using Prim's algorithm. Before moving forward, here are a few notations that one should remember:
- Red nodes represent unvisited vertices while green nodes represent visited vertices.
- Edges of minimum spanning tree are represented in purple color.

```python
# converting graph to dictionary
road_list = roads._adj

# infinity is assigned as the maximum edge weight + 1
inf = 1 + max([w['weight'] for u in road_list.keys() for (v,w) in road_list[u].items()])

# initialising dictionaries
(visited, distance, TreeEdges) = ({}, {}, [])
```

### Step 1
Suppose the road construction starts from city A, so A is the source node. The distance of other cities is assumed to be unknown, so all other visited vertices are marked as 'not visited' and the distance as infinite (which equals 8 in this case).

```python
# assigning infinite distance to all nodes and marking all nodes as not visited
for v in road_list.keys():
    (visited[v], distance[v]) = (False, inf)  # false indicates not visited
visited['A'] = True
distance['A']=0

# plotting graph
# Nudge function is created to show node labels outside the node
def nudge(pos, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in pos.items()}

pos_nodes = nudge(pos, 0.025, 0.16)  # shift the layout
fig= plt.figure(figsize=(5, 5))

# assigning green color to visited nodes and red to unvisited.
node_colors = ["#4EAD27" if visited[n] == True  else "#DF340B" for n in visited]
labels = {v:distance[v] for v in distance}

# plotting the base graph
nx.draw(
    roads,
    pos,
    with_labels=True,
    node_size=900,
    node_color=node_colors,
    font_color="white",
    font_weight="bold",
    font_size=14,
    node_shape="s",
)
# adding node labels
nx.draw_networkx_labels(
    roads,
    pos= pos_nodes,
    labels= labels,
    font_size= 14,
    font_color="blue"
)
# adding edge labels
nx.draw_networkx_edge_labels(
    roads,
    pos,
    edge_labels=nx.get_edge_attributes(roads, "weight"),
    font_size=12,
);
```

### Step 2
Now, the next step is to assign distances to A's neighbouring cities and the distance is equal to the edge weight. This needs to be done in order to find the minimum spanning tree. The distance will be updated as `minimum(current weight, new edge weight)`.<br>
Here, the following nodes will get updated:
- B : `min(1, 8) = 1`
- C : `min(7, 8) = 7`

```python
# updating weights of A's neighbour
for (v, w) in road_list["A"].items():
    distance[v] = w["weight"]
# plotting graph
fig = plt.figure(figsize=(5, 5))

node_colors = ["#4EAD27" if visited[n] == True else "#DF340B" for n in visited]
labels = {v: distance[v] for v in distance}

# plotting the base graph
nx.draw(
    roads,
    pos,
    with_labels=True,
    node_size=900,
    node_color=node_colors,
    font_color="white",
    font_weight="bold",
    font_size=14,
    node_shape="s",
)
# adding node labels
nx.draw_networkx_labels(
    roads, pos=pos_nodes, labels=labels, font_size=14, font_color="blue"
)
# adding edge labels
nx.draw_networkx_edge_labels(
    roads,
    pos,
    edge_labels=nx.get_edge_attributes(roads, "weight"),
    font_size=12,
);

```

### Step 3 & Step 4
After updating the distance in the previous step, it's time to find the next node with the minimum distance. To do this, iterate across the neighbours of the visited nodes and find the node with the minimum distance. Then update its distance and mark it as visited.

```python
# initialising the required dictionaries for plotting graphs
visited_list = []
distance_list = []
edge_list = []

# iterating through every node's neighbour
for i in road_list.keys():
    (mindist, nextv) = (inf, None)
    for u in road_list.keys():
        for (v, w) in road_list[u].items():
            d = w["weight"]

            # updating the minimum distance
            if visited[u] and (not visited[v]) and d < mindist:
                (mindist, nextv, nexte) = (d, v, (u, v, d))
    if nextv is None:  # all nodes have been visited
        break
    visited[nextv] = True
    visited_list.append(visited.copy())
    #  adding the next minimum distance edge to the spanning tree
    TreeEdges.append(nexte)
    edge_list.append(TreeEdges.copy())

    # updating the new minimum distance
    for (v, w) in road_list[nextv].items():
        d = w["weight"]
        if not visited[v]:
            distance[v] = min(distance[v], d)
    distance_list.append(distance.copy())

```

Let's understand each iteration and plot the graph!

<b>Figure 1</b><br>
B has the minimum distance of 1 unit from Node A and hence got added in the spanning tree. The next step is to update the distance of B's neighbour, which are as follows:
- A : Already visited
- C : `min(7, 1)` = 1
- D : `min(8, 4)` = 4
- E : `min(8, 3)` = 3

<b>Figure 2</b><br>
The next node with the minimum distance is C with a distance of 1 unit, so now C will get added to the spanning tree, and it's neighbours will get updated:
- A : Already visited
- B : Already visited
- E : `min(3, 6)` = 3

<b>Figure 3</b><br>
Among the last 2 nodes, E has the minimum distance of 3 units. So, E will get added to the spanning tree, and its neighbours will get updated:
- B : Already visited
- C : Already visited
- D : `min(4, 2)` = 2

<b>Figure 4</b><br>
The final node D, with a distance of 2 units, got connected to the minimum spanning tree. This figure illustrates the final Minimum Spanning Tree of the example.

```python
fig, axes = plt.subplots(2, 2, figsize=(15,15))
c=0
for v,d,ax,edges in zip(visited_list,distance_list,axes.ravel(), edge_list):
    c+=1
    ax.set_title("Figure "+str(c), fontsize=16)
    node_colors = ["#4EAD27" if v[n] == True  else "#DF340B" for n in v]
    labels = {k:d[k] for k in d}
    nx.draw(
    roads,
    pos,
    with_labels=True,
    node_size=900,
    node_color=node_colors,
    font_color="white",
    font_weight="bold",
    font_size=14,
    node_shape="s",
    ax= ax
)
    nx.draw_networkx_edges(
    roads,
    pos,
    edgelist=edges,
    width=3,
    edge_color="#823AAF",
    ax=ax,
)

    nx.draw_networkx_labels(
    roads,
    pos= pos_nodes,
    labels= labels,
    font_size= 14.5,
    font_color="blue",
    ax= ax
)
    nx.draw_networkx_edge_labels(
    roads,
    pos,
    edge_labels=nx.get_edge_attributes(roads, "weight"),
    font_size=12,
    ax=ax
);
    
```

### Step 5
The final output of the program is stored as a list of tuples in `TreeEdges` as shown below.

```python
print(TreeEdges)
```

## NetworkX Implementation

The above code is a basic implementation of Prim's algorithm with the time complexity of $ O (mn)$, which further can be improved to $O((V+E) \text{ log} V)$ with the help of priority queues. Here's the good part, with the help of NetworkX functions, one can implement it in $O((V+E) \text{ log} V)$ without even writing the whole code.<br>
NetworkX provides various [Tree](https://networkx.org/documentation/stable/reference/algorithms/tree.html#) functions to perform difficult operations, and [minimum_spanning_tree()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tree.mst.minimum_spanning_tree.html#networkx.algorithms.tree.mst.minimum_spanning_tree) is one of them. Not only this, you can also find the maximum spanning tree with the help of the [maximum_spanning_tree()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tree.mst.maximum_spanning_tree.html#networkx.algorithms.tree.mst.maximum_spanning_tree) function.<br>
The following code uses NetworkX function and gives us the same output as our code.

```python
MST= nx.minimum_spanning_tree(roads, algorithm= "prim")
print(sorted(MST.edges(data=True)))
```

## Applications of Prim's Algorithm
- It is used to solve travelling salesman problem.
- As said earlier, used in network for roads and rail tracks connecting all the cities.
- Path finding algorithms used in artificial intelligence.
- Cluster analysis
- Game development
- Maze generation

There are many other similar applications present in this world. Whenever there's a need to find a cost-effective method to connect nodes (it can be anything), there's a high chance of Prim's algorithm playing its role in the solution.


## Reference
R. C. Prim "Shortest connection networks and some generalizations." The bell system technical journal, Volume: 36, Issue: 6, (Nov. 1957): 1389-1401<br>
https://ia800904.us.archive.org/18/items/bstj36-6-1389/bstj36-6-1389.pdf
