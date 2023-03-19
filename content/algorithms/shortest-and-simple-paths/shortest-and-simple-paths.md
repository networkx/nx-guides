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

# Shortest Paths and Simple Paths in Networkx

+++

Networkx provides a large collection of methods to calculate the [shortest paths](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html) and [simple paths](https://networkx.org/documentation/stable/reference/algorithms/simple_paths.html) in a graph. In this tutorial we will explore these methods and draw comparisons amongst them.

+++

## Shortest paths

+++

The shortest path methods in Networkx can be used for computing shortest paths and shortest path lengths between the nodes in a graph. We will understand the methods used for undirected graphs within the scope of this notebook.

First, we'll generate a random graph G and then apply the various methods on this graph to understand how they work.

```{code-cell} ipython3
%matplotlib inline
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
```

```{code-cell} ipython3
G = nx.gnp_random_graph(10, 0.2, seed = 25354)
nx.draw_kamada_kawai(G, with_labels = True, node_color = 'yellow', node_size = 1000)
```

We'll start with the methods that are applicable for both undirected and directed graphs:

+++

1. **shortest_path(G, source=None, target=None, weight=None, method='dijkstra'):** It computes the shortest path(s) between nodes.

    There may be more than one shortest path between a source and target, but this method returns only one of them. Both the starting and ending nodes are included in the path.
    
    The output format depends on whether the source and target have been specified or not - 
    
    - Neither specified : Return a dictionary of dictionaries with paths[source][target]=[list of nodes in path]
    - Source specified : Return a dictionary keyed by targets with a list of nodes in a shortest path from the source to one of the targets 
    - Target specified : Return a dictionary keyed by sources with a list of nodes in a shortest path from one of the sources to the target
    - Both specified : Return a single list of nodes in a shortest path from the source to the target

    By default, the method is implemented using Dijkstra's algorithm.

```{code-cell} ipython3
# Returns a dictionary of dictionaries when neither source nor target is specified
paths = dict(nx.shortest_path(G))

print("Path between nodes 4 and 5: " + str(paths[4][5]))
print("Paths between node 3 as source and all the nodes as target: " + str(paths[3]))
```

```{code-cell} ipython3
# Returns a dictionary of lists when either source or target is specified
print("Paths between all the nodes as source and node 3 as target: " + str(dict(nx.shortest_path(G, target = 3))))
```

```{code-cell} ipython3
# Returns a list when both source and target are specified
print("Path between nodes 3 and 6: " + str(list(nx.shortest_path(G, source = 3, target = 6))))
```

2. **shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra'):** This method is similar to shortest_path in terms of the input parameters and output format, except that we return the path length instead of a list containing the path nodes.

    The similarity in the two methods can be seen by running shortest_path_length on the same examples as shortest_path.

```{code-cell} ipython3
# Returns a dictionary of dictionaries when neither source nor target is specified
path_lens = dict(nx.shortest_path_length(G))

print("Path lengths between nodes 4 and 5: " + str(path_lens[4][5]))
print("Path lengths between node 3 as source and all the nodes as target: " + str(path_lens[3]))
```

```{code-cell} ipython3
# Returns a dictionary of ints when either source or target is specified
print("Path lengths between all the nodes as source and node 3 as target: " + str(dict(nx.shortest_path_length(G, target = 3))))
```

```{code-cell} ipython3
# Returns an int when both source and target are specified
print("Path length of shortest path between nodes 3 and 6: " + str(nx.shortest_path_length(G, source = 3, target = 6)))
```

3. **all_shortest_paths(G, source, target, weight=None, method='dijkstra'):** It computes all the shortest simple paths between the source and target and return a list of paths.

    A simple path is a path with no repeated nodes. We will cover this in more detail later in the notebook.
    
    Unlike shortest_path method, this method requires us to specifiy both source and target and will output all possible shortest paths between the two.

```{code-cell} ipython3
print("All possible shortest paths between 3 and 6: " + str(list(nx.all_shortest_paths(G, source = 3, target = 6))))
```

4. **average_shortest_path_length(G, weight=None, method=None):** It returns the average shortest path length of the graph.

    The average shortest path length is equal to - 
    \begin{split}a =\sum_{\substack{s,t \in V \\ s\neq t}} \frac{d(s, t)}{n(n-1)}\end{split} 
    where V is the set of nodes in G, d(s, t) is the shortest path from s to t, and n is the number of nodes in G.
    
    Since our example graph G has disconnected components, this method will throw an error. However, we can find the average shortest path length of the various components of G.

```{code-cell} ipython3
i = 1
for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
    print("Average shortest path length of component " + str(i) + " : " + str(nx.average_shortest_path_length(C)))
    i+=1
```

5. **has_path(G, source, target):** This method returns True if G has a path from source to target, false otherwise.

```{code-cell} ipython3
print("Path exists between nodes 3 and 5: " + str(nx.has_path(G, 3, 5)))
print("Path exists between nodes 2 and 6: " + str(nx.has_path(G, 2, 6)))
```

// comments for weight and method parameters.

+++

Now, we'll go through some advanced interface methods available exclusively for undirected graphs.

+++

1. **single_source_shortest_path(G, source, cutoff=None):** Compute shortest path between source and all other nodes reachable from source.

2. **single_source_shortest_path_length(G, source):** Compute the shortest path lengths from source to all reachable nodes.

+++

3. **single_target_shortest_path(G, target, cutoff=None):** Compute shortest path to target from all nodes that reach target.

4. **single_target_shortest_path_length(G, target):** Compute the shortest path lengths to target from all reachable nodes.

+++

5. **all_pairs_shortest_path(G, cutoff=None):** Compute shortest paths between all nodes.

6. **all_pairs_shortest_path_length(G, cutoff=None):** Computes the shortest path lengths between all nodes in G.

+++

7. **bidirectional_shortest_path(G, source, target):** Returns a list of nodes in a shortest path between source and target.

+++

8. **predecessor(G, source, target=None, cutoff=None, return_seen=None]):** Returns dict of predecessors for the path from source to all nodes in G.

+++

// comments about cutoff

+++

## Simple Paths

+++

// discuss simple paths

+++

1. **all_simple_paths(G, source, target, cutoff=None):** Generate all simple paths in the graph G from source to target.

+++

2. **all_simple_edge_paths(G, source, target, cutoff=None):** Generate lists of edges for all simple paths in G from source to target.

+++

3. **is_simple_path(G, nodes):** Returns True if and only if nodes form a simple path in G.

+++

4. **shortest_simple_paths(G, source, target, weight=None):** Generate all simple paths in the graph G from source to target,

+++

// conclusion notes
