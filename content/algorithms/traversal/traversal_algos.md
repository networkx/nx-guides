---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Graph Traversal Algorithms

+++

In this tutorial, we will explore the graph traversal algorithms implemented in networkx under [networkx/algorithms/traversal.py](https://networkx.org/documentation/stable/reference/algorithms/traversal.html).

+++

Specifically, we'll focus on the following:
1. Depth-First Search (DFS)
2. Bread-First Search (BFS)

+++

Many graph applications need to visit the vertices of a graph in some specific order based on the graph’s topology. This is known as a graph traversal. BFS and DFS are really just two different ways of touching all nodes of a graph.

+++

Graph Traversals can be used to find if there exists a path between two nodes and what is the length of such path.

For example, many problems in artificial intelligence programming are modeled using graphs. The problem domain might consist of a large collection of states, with connections between various pairs of states. Solving this sort of problem requires getting from a specified start state to a specified goal state by moving between states only through the connections. Typically, the start and goal states are not directly connected. To solve this problem, the vertices of the graph must be searched in some organized manner.

+++

Let's understand with the help of an example.

```{code-cell}
%matplotlib inline
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
```

```{code-cell}
G = nx.gnp_random_graph(8, 0.6, 2, False)
nx.draw_kamada_kawai(G, with_labels=True, font_weight="bold")
```

Let's say you are given the above search space, the intial state is '0' and you have to reach the goal state '1'. Then, based on the edges available between the nodes we move in a certain manner such that a path can be found from 0 to 1.

```{code-cell}
list(nx.all_simple_paths(G, 0, 1, 4))
```

The above code generates simple paths (a path in a graph which does not have repeating vertices) from 0 to 1 in graph G. The function all_simple_paths() uses a modified version of the Depth First Search. Let us understand it in detail.

+++

## Depth First Search

+++

DFS algorithm starts at the root node (or any arbitrary node) and explores as far as possible along each branch before backtracking. In other words, DFS explores one path as far as it can go before falling back and exploring another path.

+++

### How does DFS work?

+++

DFS is a recursive algorithm that uses backtracking. To implement it properly, we need to keep track of which vertices have already been visited. It can be done using a set or a boolean array. A stack is used to store the nodes that we mean to visit. 

Here's the pseudocode for both iterative and recursive implementations of DFS:

```{raw-cell}
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

### DFS Illustration

+++

To help you visualize DFS easily, the graph used earlier has been color coded based on how it would be traversed by the Depth First Search algorithm. Here the root node is taken as '0'. The color changes from dark green to yellow as we traverse from the root node to the nodes further and further away from it.

```{code-cell}
# helper function to color code the graph
def color_nodes(G, l):
    d = {0: 1}
    i = 2
    for t in l:
        d[t[1]] = i
        i += 1

    low, *_, high = sorted(d.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.summer)

    nx.draw_kamada_kawai(
        G,
        nodelist=d,
        node_size=500,
        node_color=[mapper.to_rgba(i) for i in d.values()],
        with_labels=True,
        font_color="black",
    )
    plt.show()
```

```{code-cell}
# generate a list of edges in the order they are traversed by DFS
dfs_list = list(nx.dfs_edges(G, 0))
dfs_list
```

```{code-cell}
color_nodes(G, dfs_list)
```

An interactive tool for understanding how the DFS algorithm will run on different graphs can be found [here](https://www.cs.usfca.edu/~galles/visualization/DFS.html).

+++

### NetworkX Implementation of DFS

+++

DFS implementation in NetworkX allows depth-limits i.e. the DFS algorithm runs for a specific depth-limit and this limit increases iteratively till we find our goal or the graph is exhausted.

+++

NetworkX implements several methods using the DFS algorithm. These are:

1. dfs_edges: Performs a depth-first search over the nodes of graph and returns the edges traversed in order. It may not generate all edges in graph because it stops when all nodes have been visited.


2. dfs_tree: Returns an oriented tree constructed by performing a depth-first-search from source on the graph. (A tree is an undirected graph in which any two nodes are connected by exactly one path.


3. dfs_predecessors: Returns dictionary of predecessors in depth-first-search from source.


4. dfs_successors: Returns dictionary of successors in depth-first-search from source.


5. dfs_preorder_nodes: Generate nodes in a depth-first-search pre-ordering starting at source


6. dfs_postorder_nodes: Generate nodes in a depth-first-search post-ordering starting at source.


7. dfs_labeled_edges: Iterate over edges in a depth-first-search (DFS) labeled by type. It returns a generator of triples of the form (u, v, d) where (u, v) is the edge being explored and d is one of the strings 'forward', 'nontree', 'reverse' and 'reverse-depth_limit'. More information can be found [here](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.traversal.depth_first_search.dfs_labeled_edges.html#networkx.algorithms.traversal.depth_first_search.dfs_labeled_edges).

```{code-cell}
print("dfs_edges : " + str(list(nx.dfs_edges(G))), end="\n\n")
print("dfs_tree : " + str(list(nx.dfs_tree(G))), end="\n\n")
nx.draw_spectral(nx.dfs_tree(G), with_labels=True)
print("dfs_predecessors : " + str(nx.dfs_predecessors(G)), end="\n\n")
print("dfs_successors : " + str(nx.dfs_successors(G)), end="\n\n")
print("dfs_preorder_nodes : " + str(list(nx.dfs_preorder_nodes(G))), end="\n\n")
print("dfs_postorder_nodes : " + str(list(nx.dfs_postorder_nodes(G))), end="\n\n")
print("dfs_labeled_edges : " + str(list(nx.dfs_labeled_edges(G))), end="\n\n")
```

The implementation of all DFS related algorithms in Networkx has been demonstrated above.

+++

## Breadth First Search

+++

BFS algorithm starts at the root node (or any arbitrary node) of the graph and explores all the nodes at the current depth before moving on to the nodes at the next depth. In other words, BFS visits all the nodes at a given level before moving down to the next level. BFS is useful for finding the shortest path between two nodes in an unweighted graph

+++

### How does BFS work?

+++

BFS algorithm starts at the root node of the graph and visits all the nodes at the current level before moving on to the nodes at the next level. Just like DFS, we need to keep track of which vertices have already been visited which can be done using a set or a boolean array. However instead of a stack we use a queue data structure to keep track of the nodes to be visited.

Here's the pseudocode for BFS algorithm:

```{raw-cell}
    bfs (G, src)                   //Where G is the graph and s is the source node
        let Q be queue
        Q.enqueue(src)             //Inserting s in queue until all its neighbour vertices are marked.
        mark src as visited.
        while (Q is not empty)
            //Removing that vertex from queue,whose neighbour will be visited now
            v  =  Q.dequeue( )
            //processing all the neighbours of v  
            for all neighbours w of v in Graph G
                if w is not visited
                    Q.enqueue( w )  //Stores w in Q to further visit its neighbour
                    mark w as visited.
```

### BFS Illustration

+++

Similar to the DFS color-coded visualization, the next one demonstrates how the graph will be traversed by the BFS algorithm. The root node is '0' and the color changes from dark green to yellow as we traverse from the root node to rest of the nodes level-by-level.

```{code-cell}
bfs_list = list(nx.bfs_edges(G, 0))
bfs_list
```

```{code-cell}
color_nodes(G, bfs_list)
```

In the above graph, we can observe that the node that is the furthest from the source node is the lightest yellow color, becuase it is reached at the very end.

An interactive tool for understanding how the BFS algorithm will run on different graphs can be found [here](https://www.cs.usfca.edu/~galles/visualization/BFS.html).

+++

### NetworkX Implementation of BFS

+++

NetworkX implements several methods using the BFS algorithm. These are:

1. bfs_edges : Iterate over edges in a breadth-first-search starting at source such that those edges are reported that are traversed during the BFS over nodes of graph.


2. bfs_layers : Returns an iterator of all the layers in breadth-first search traversal such that there are lists of nodes at same distance from the source.


3. bfs_tree : Returns an oriented tree constructed by performing a breadth-first-search on graph starting at the source.


4. bfs_predecessors : Returns an iterator of predecessors in breadth-first-search from source.


5. bfs_successors : Returns an iterator of successors in breadth-first-search from source.


6. descendants_at_distance : Returns a set of all nodes at a fixed distance from source in G.

```{code-cell}
print("bfs_edges : " + str(list(nx.bfs_edges(G, 0))), end="\n\n")
print("bfs_layers : " + str(dict(enumerate(nx.bfs_layers(G, [0])))), end="\n\n")
print("bfs_tree : " + str(list(nx.bfs_tree(G, 7))), end="\n\n")
nx.draw_planar(nx.bfs_tree(G, 0), with_labels=True)
print("bfs_predecessors : " + str(list(nx.bfs_predecessors(G, 0))), end="\n\n")
print("bfs_successors : " + str(list(nx.bfs_successors(G, 0))), end="\n\n")
print(
    "descendants_at_distance : " + str(nx.descendants_at_distance(G, 0, 2)), end="\n\n"
)
```

## Applications of BFS and DFS

+++

Breadth-first search and Depth-first search form the backbone of many other algorithms in graph theory.

BFS is used to find shortest path and its length in unweighted graphs. It can be used to find if there exists a cycle in the graph. It is used in the Ford-Fulkerson method for computing maximum flow in a flow network and can also be used to test the bipartiteness of the graph.

DFS is often used to find connected components and strongly connected components in a graph. It is also used in the topological sorting algorithm. Both DFS and BFS can be used to find spanning trees of a graph.

+++

## References

+++

1. http://www.cs.toronto.edu/~heap/270F02/node36.html
2. https://wiki.eecs.yorku.ca/course_archive/2012-13/S/2011/_media/22Apps.pdf
3. https://en.wikipedia.org/wiki/Depth-first_search
4. https://en.wikipedia.org/wiki/Breadth-first_search
