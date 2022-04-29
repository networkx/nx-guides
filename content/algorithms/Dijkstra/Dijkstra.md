---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Shortest path using Dijkstra's algorithm

+++

When it comes to finding the shortest path in a weighted graph, the Dijkstra algorithm has always been preferred by all. In this notebook, we will learn how it works and is carried out.<b> Shortest path problem</b> is a graph problem where the objective is to find a path between 2 nodes having the minimum distance covered.

+++

## Shortest Path Problem

+++

Let's say you want to travel from Delhi (DEL), India, to London (LCY), UK via flights that have various routes with different stops, namely, Frankfurt (FRA), Zurich (ZRH), Amsterdam (AMS), Geneva (GVA) and Dublin (DUB). Now, you want to find the shortest path as you are in a hurry and want to get to London as soon as possible.<br> 
An important thing to know is that any subpath from C $\rightarrow$ E of the shortest path A $\rightarrow$ E is also the shortest path from node C to node E. That means not only one will get the shortest path from Delhi to London but also to other stops from Delhi.

<b>ASSUMPTIONS</b>
- Distance taken is imaginary.
- No waiting time at airports.
- The shortest distance in this problem means shortest time costing. 
- Speed is considered to be uniform
- Scale : 1 unit = 1000kms

So, the following directed graph describes all paths available with the distance between them.

```{code-cell} ipython3
# importing libraries
import networkx as nx
import matplotlib.pyplot as plt

flight_path = nx.DiGraph()
path_edge=  [
        ("DEL", "ZRH", 5),
        ("DEL", "FRA", 6),
        ("DEL", "DUB", 7),
        ("ZRH", "LCY", 6),
        ("ZRH", "GVA", 3),
        ("FRA", "LCY", 3),
        ("FRA", "AMS", 2),
        ("DUB", "LCY", 4),
        ("DUB", "AMS", 2),
        ("GVA", "LCY", 1),
        ("AMS", "LCY", 5),
    ]
# adding weighted edges
flight_path.add_weighted_edges_from( path_edge
)

# layout of the graph
position = {
    "DEL": (0, 1),
    "DUB": (1, 2),
    "AMS": (1, 1.25),
    "FRA": (1, 0.5),
    "ZRH": (1, 0),
    "LCY": (2, 1),
    "GVA": (2, 0),
}
pos = nx.spring_layout(
    flight_path,
    pos=position,
    weight="weight",
    fixed=["DEL", "AMS", "DUB", "ZRH", "FRA", "LCY", "GVA"],
)
fig = plt.figure(figsize=(6.5, 4.5))

# drawing customised nodes
nx.draw(
    flight_path,
    pos,
    with_labels=True,
    node_size=1100,
    node_color="#546A8E",
    font_color="white",
    font_weight="bold",
    font_size=13,
    node_shape="s",
    width=1.5,
    edge_color="#545B5D",
)
# adding edge labels
nx.draw_networkx_edge_labels(
    flight_path,
    pos,
    edge_labels=nx.get_edge_attributes(flight_path, "weight"),
    font_size=13,
);
```

## Dijkstra's Algorithm

Dijkstra's algorithm is used to find the shortest path between nodes or commonly from one source node to every other node in the graph, where edge weight represents the cost/ distance between 2 nodes in the case of a weighted graph. It can work with both directed and undirected graphs, but <b>it is not suitable for graphs with NEGATIVE edges.</b><br>
Time complexity of Dijkstra's algorithm is $O(\ V^{2})$, but with minimum priority queue, it comes down to $O(\ V + E\text{ log } V\ )$

### Algorithm

1. Convert your problem into a graph equivalent.
2. Create a list of unvisited vertices. 
3. Assign the starting point as source node with <b>distance(cost)= 0</b> and other node's distance as infinity.
4. For every unvisited neighbour, calculate the minimum distance from the current node.
5. The new distance is calculated as `minimum(current distance, distance of previous node + edge weight)`
6. When all the neighbours have been visited, remove the node from the unvisited list and select the next node with the minimum distance.
7. Repeat from step 4.
8. The final graph will represent all the nodes with minimum distance and the algorithm will end.

+++

Let's look at the example of the directed graph mentioned above. But, before moving forward, here are some things one should keep in mind.<br>
In the following graphs:
- Edge weight defines the distance between 2 nodes
- Black edge represents unvisited edges
- Red represents edges that are being traversed
- Green represents visited edges

LET'S BEGIN!!

```{code-cell} ipython3
# converting graph to dictionary
flight_succ = flight_path._succ

# infinity is assigned as the maximum edge weight + 1
inf = 1 + len(flight_succ.keys())* max([d['weight'] for u in flight_succ.keys() for (v,d) in flight_succ[u].items()])

# initialising dictionaries
(visited, distance) = ({}, {})
```

### Step 1

Assign all stops(nodes) infinite values except the source node (DEL in this case as the path starts from Delhi), which is assigned a value of 0. This is because the distance one needs to cover to reach other nodes is assumed to be unknown and, hence maximum value possible is being assigned.

```{code-cell} ipython3
# assigning infinite distance to all nodes and marking all nodes as not visited
for v in flight_succ.keys():
    (visited[v], distance[v]) = (False, inf)  # false indicates not visited

distance['DEL'] = 0

# plotting graph
# Nudge function is created to show node labels outside the node
def nudge(pos, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in pos.items()}

pos_nodes = nudge(pos, 0.06, 0.18)  # shift the layout
fig,ax= plt.subplots(figsize=(9, 7))

labels = {v:distance[v] for v in distance}

# drawing customised nodes
nx.draw(
    flight_path,
    pos,
    with_labels=True,
    node_size=1100,
    node_color="#546A8E",
    font_color="white",
    font_weight="bold",
    font_size=13,
    node_shape="s",
    width=1.5,
    edge_color="#545B5D",
)
# adding node labels
nx.draw_networkx_labels(
    flight_path,
    pos= pos_nodes,
    labels= labels,
    font_size= 15,
    font_color='red'
)
# adding edge labels
nx.draw_networkx_edge_labels(
    flight_path,
    pos,
    edge_labels=nx.get_edge_attributes(flight_path, "weight"),
    font_size=13,
)

# expand plot to fit labels
ax.set_ylim(tuple(i * 1.02 for i in ax.get_ylim()));
```

### Step 2
Dijkstra is based on the greedy approach, which means one needs to select the node with the minimum distance and this approach is being followed in the whole process. After selecting, it's time to start traversing the neighbours of the selected node and update the distance of all neighbouring nodes. While updating the distance, always keep in mind that the updated distance should be `minimum(current distance, distance of previous node + edge weight)`.

```{code-cell} ipython3
# initialising the required dictionaries for plotting graphs
edgelist = [[]]
current_edges = []
current_distance = []

# stores the paths of each node
path = {}
path["DEL"] = ["DEL"]

for _ in flight_succ.keys():

    # minimum distance among unvisited nodes
    nextd = min([distance[v] for v in flight_succ.keys() if not visited[v]])
    # list of nodes having the minimum distance
    nextvlist = [
        v for v in flight_succ.keys() if (not visited[v]) and distance[v] == nextd
    ]

    if nextvlist == []:  # all nodes have been visited
        break
    nextv = min(nextvlist)
    visited[nextv] = True
    edge = []  # stores the traversing edges

    for (v, d) in flight_succ[nextv].items():
        if not visited[v]:
            # if new minimum distance exists
            if (distance[nextv] + d["weight"]) < distance[v]:
                distance[v] = distance[nextv] + d["weight"]
                path[v] = path[nextv] + [v]
            edge.append((nextv, v))
    # updating lists for plotting purpose
    edgelist.append(edgelist[-1] + edge)
    current_edges.append(edge.copy())
    current_distance.append(distance.copy())
```

LET'S UNDERSTAND EACH ITERATION

<b>Figure 1</b><br>
DEL has the minimum distance of 0 units, so, it's time to start traversing its neighbours and updating their distances.
- DUB : `min(infinity, 7) = 7`
- FRA : `min(infinity, 6) = 6`
- ZRH : `min(infinity, 5) = 5`

<b>Figure 2</b><br>
Now, pick the next unvisited node with the minimum distance value. ZRH has the minimum distance (5 units), so it's time to update its neighbour's (LCY, GVA) distance.
- LCY : `min(infinity, 5+6) = 11`
- GVA : `min(infinity, 5+3) = 8`

<b>Figure 3</b><br>
Similar to the previous step, the next unvisited node with minimum distance is FRA (6 units).Hence, update its neighbours. 
- AMS : `min(infinity, 6+2) = 8`
- LCY : `min(11, 6+3) = 9`
   
<b>Figure 4</b><br>  
DUB is the next node with minimum distance of 7 units. The distance of its neighbours will change as follows:
   - AMS : `min(7, 7+2) = 7`
   - LCY : `min(9, 7+4) = 9`

<b>Figure 5</b><br>
Both AMS and GVA have the same distance of 8 units. The node which was added first will be traveresed first according to the code. So, AMS's neighbour LCY will get updated.
   - LCY : `min(9, 7+5) = 9`

<b>Figure 6</b><br>
It's time to update the final node GVA's neighbour.
   - LCY : `min(9, 8+1) = 9`
   
<b>Figure 7</b><br>
This figure shows the final graph with shortest distance to each node from DEL(source node) and it comes out that the shortest distance to LCY from DEL is 9 units which have 2 paths:<br>
- (DEL $\rightarrow$ FRA $\rightarrow$ LCY) <br>
- (DEL $\rightarrow$ ZRH $\rightarrow$ GVA $\rightarrow$ LCY)

So, one can take any of these paths to reach as soon as possible. But, in case there are more than one path, like in this situation, <b>dijkstra's algorithm returns the first shortest path traveresed in the graph as shown below. </b>

```{code-cell} ipython3
# Distance and path from DEL to LCY
print(distance['LCY'],path['LCY'])
```

```{code-cell} ipython3
# plotting the graphs

# layout of the graphs
fig, axes = plt.subplots(4, 2, figsize=(20, 30), dpi=700)
axes[3][1].remove()
c = 0

for d, ax, edges, current in zip(
    current_distance, axes.ravel(), edgelist, current_edges
):
    c += 1
    ax.set_title("Figure " + str(c), fontsize=18)
    edge_color = [
        "red" if (v, u) in current else "green" if (v, u) in edges else "#545B5D"
        for (v, u, w) in path_edge
    ]
    labels = {k: d[k] for k in d}

    # plotting the base graph
    nx.draw(
        flight_path,
        pos,
        with_labels=True,
        node_size=1100,
        node_color="#546A8E",
        font_color="white",
        font_weight="bold",
        font_size=13,
        node_shape="s",
        width=1.5,
        edge_color=edge_color,
        ax=ax,
    )
    # adding node labels
    nx.draw_networkx_labels(
        flight_path, pos=pos_nodes, labels=labels, font_size=15, font_color="red", ax=ax
    )

    # adding edge labels
    nx.draw_networkx_edge_labels(
        flight_path,
        pos,
        edge_labels=nx.get_edge_attributes(flight_path, "weight"),
        font_size=13,
        ax=ax,
    )
    # expand plot to fit labels
    ax.set_ylim(tuple(i * 1.02 for i in ax.get_ylim()));
```

## NetworkX Implementation

+++

The time complexity of the above program was $O(n^{2})$, which is fine for the above example as the number of nodes was less. But, in real-life problems, there can be a lot of nodes with complex solutions, and thus, it is needed to implement the algorithm in $O(\ V + E\text{ log } V\ )$ time using a priority queue. Don't worry; you don't need to write the whole code. Networkx got you covered!!

So, NetworkX provides provides functions with the help of which one can actually find the [shortest path](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html) based on their needs.<br>
All functions using dijkstra's algorithm are similar, but for this example the most suitable one is [single_source_dijkstra()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.single_source_dijkstra.html#networkx.algorithms.shortest_paths.weighted.single_source_dijkstra). This function gives the same output as the above program but in a better time. One only needs to call the function as shown below.

```{code-cell} ipython3
nx.single_source_dijkstra(G= flight_path, source = 'DEL', target='LCY')
```

## Applications of Dijkstra's Algorithm

It is used as a part of applications to find the shortest path if required. There are other factors as well which are considered in every application while implementing Dijkstra's algorithm. Like,
- In special drones or robots for delivery service, it is used as a part to identify the shortest path possible.
- One of the most common use case is Google Maps. It helps to find the best route possible in shortest time.
- In social media applications, for smaller graphs it can be used effectively to suggest the "people you may know" section.
- As the above example, it can be used in a software which calculates and informs the estimate arrival time, best route etc. of a flight to a user.
- It is used in IP routing to find Open shortest Path First.
- It is used in the telephone network.

+++

## Advantages and Disadvantages of Dijkstra's Algorithm

<b>ADVANTAGES</b>
 - Once it is carried out, we can find the shortest path to all permanently labelled node.
 - Only one diagram is enough to reflect all distances/paths.
 - It is efficient enough to use for relatively large problems.
 
<b>DISADVANTAGES</b>
- It cannot handle negative weights which leads to acyclic graphs and most often cannot obtain the right shortest path.
- It is a greedy algorithm that means it is possible for the algorithm to select the current best option which can make the algorithm get sidetracked following a potential path that doesn’t exist, simply because the edges along it form a short path.

+++

## Reference

Dijkstra, Edsger W. "A note on two problems in connexion with graphs." Numerische mathematik 1, no. 1 (1959): 269-271.<br>
https://ir.cwi.nl/pub/9256/9256D.pdf
