# Graph Traversal Algorithms

In this tutorial, we will explore the graph traversal algorithms implemented in networkx under networkx/algorithms/traversal.py.

Specifically, we'll focus on the following:
1. Depth-First Search (DFS)
2. Bread-First Search (BFS)

Many graph applications need to visit the vertices of a graph in some specific order based on the graph’s topology. This is known as a graph traversal. BFS and DFS are really just two different ways of touching all nodes of a graph.

Graph Traversals can be used to find if there exists a path between two nodes and what is the length of such path. For example, many problems in artificial intelligence programming are modeled using graphs. The problem domain might consist of a large collection of states, with connections between various pairs of states. Solving this sort of problem requires getting from a specified start state to a specified goal state by moving between states only through the connections. Typically, the start and goal states are not directly connected. To solve this problem, the vertices of the graph must be searched in some organized manner.

Let's understand with the help of an example.


```python
%matplotlib inline
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
```


```python
G = nx.gnp_random_graph(8, 0.6, 2, False)
nx.draw_kamada_kawai(G, with_labels=True, font_weight='bold')
```


    
![png](output_7_0.png)
    


Let's say you are given the above search space, the intial state is '0' and you have to reach the goal state '1'. Then, based on the edges available between the nodes we move in a certain manner such that a path can be found from 0 to 1.


```python
list(nx.all_simple_paths(G, 0, 1, 4))
```




    [[0, 3, 2, 1],
     [0, 3, 2, 7, 1],
     [0, 3, 4, 5, 1],
     [0, 3, 4, 6, 1],
     [0, 3, 4, 7, 1],
     [0, 3, 5, 1],
     [0, 3, 5, 7, 1],
     [0, 3, 6, 1],
     [0, 3, 6, 7, 1],
     [0, 3, 7, 1],
     [0, 3, 7, 2, 1],
     [0, 3, 7, 5, 1],
     [0, 3, 7, 6, 1],
     [0, 4, 3, 2, 1],
     [0, 4, 3, 5, 1],
     [0, 4, 3, 6, 1],
     [0, 4, 3, 7, 1],
     [0, 4, 5, 1],
     [0, 4, 5, 7, 1],
     [0, 4, 6, 1],
     [0, 4, 6, 7, 1],
     [0, 4, 7, 1],
     [0, 4, 7, 2, 1],
     [0, 4, 7, 5, 1],
     [0, 4, 7, 6, 1]]



The above code generates simple paths (a path in a graph which does not have repeating vertices) from 0 to 1 in graph G. The function all_simple_paths() uses a modified version of the Depth First Search. Let us understand it in detail.

## Depth First Search

DFS algorithm starts at the root node (or any arbitrary node) and explores as far as possible along each branch before backtracking. In other words, DFS explores one path as far as it can go before falling back and exploring another path.

### How does DFS work?

DFS is a recursive algorithm that uses backtracking. To implement it properly, we need to keep track of which vertices have already been visited. It can be done using a set or a boolean array. A stack is used to store the nodes that we mean to visit. Here's the pseudocode:
DFS(G,v)   // v is the vertex where the search starts
    Stack S := {};   // start with an empty stack
    for each vertex u, set visited[u] := false;
        push S, v;
        while (S is not empty) do
            u := pop S;
            if (not visited[u]) then
                visited[u] := true;
                for each unvisited neighbour w of u
                    push S, w;
            end if
        end while
    END DFS()
### DFS Illustration

To help you visualize DFS easily, the graph used earlier has been color coded based on how it would be traversed by the Depth First Search algorithm. Here the root node is taken as '0'. The color changes from dark green to yellow as we traverse from the root node to the nodes further and further away from it.


```python
# helper function to color code the graph
def color_nodes(G, l):
    d = {0:1}
    i = 2
    for t in l:
        d[t[1]] = i
        i += 1
        
    low, *_, high = sorted(d.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.summer)

    nx.draw_kamada_kawai(G, 
            nodelist=d,
            node_size=500,
            node_color=[mapper.to_rgba(i) 
                        for i in d.values()], 
            with_labels=True,
            font_color='black')
    plt.show()
```


```python
# generate a list of edges in the order they are traversed by DFS
dfs_list = list(nx.dfs_edges(G, 0))
```


```python
color_nodes(G, dfs_list)
```


    
![png](output_20_0.png)
    


### NetworkX Implementation of DFS

DFS implementation in NetworkX allows depth-limits i.e. the DFS algorithm runs for a specific depth-limit and this limit increases iteratively till we find our goal or the graph is exhausted.

NetworkX implements several methods using the DFS algorithm. These are:

1. dfs_edges: Iterate over edges in a depth-first-search (DFS)

2. dfs_tree: Returns oriented tree constructed from a depth-first-search from source

3. dfs_predecessors: Returns dictionary of predecessors in depth-first-search from source

4. dfs_successors: Returns dictionary of successors in depth-first-search from source

5. dfs_preorder_nodes: Generate nodes in a depth-first-search pre-ordering starting at source

6. dfs_postorder_nodes: Generate nodes in a depth-first-search post-ordering starting at source.

7. dfs_labeled_edges: Iterate over edges in a depth-first-search (DFS) labeled by type.

## Breadth First Search

BFS algorithm starts at the root node (or any arbitrary node) of the graph and explores all the nodes at the current depth before moving on to the nodes at the next depth. In other words, BFS visits all the nodes at a given level before moving down to the next level. BFS is useful for finding the shortest path between two nodes in an unweighted graph

### How does BFS work?

BFS algorithm starts at the root node of the graph and visits all the nodes at the current level before moving on to the nodes at the next level. To implement BFS, we use a queue data structure to keep track of the nodes to be visited.

Here are the steps to perform BFS on a graph:

1. Create an empty queue and enqueue the root node.
2. Mark the root node as visited.
3. While the queue is not empty, do the following:
- Dequeue a node from the queue.
- Visit the node and process it.
- Enqueue all the adjacent nodes that have not been visited and mark them as visited.

The BFS algorithm continues until all the nodes in the graph have been visited.


```python
bfs_list = list(nx.bfs_edges(G, 0))
```


```python
color_nodes(G, bfs_list)
```


    
![png](output_29_0.png)
    


## References

1. 
