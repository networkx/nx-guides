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
  version: 3.9.2
---

# NetworkX Tutorial

```{code-cell} ipython3
%matplotlib inline
import matplotlib.pyplot as plt
import networkx as nx
```

## Creating a graph

+++

Create an empty graph with no nodes and no edges.

```{code-cell} ipython3
G = nx.Graph()
```

By definition, a `Graph` is a collection of nodes (vertices) along with identified pairs of nodes (called edges, links, etc). In NetworkX, nodes can be any hashable object e.g. a text string, an image, an XML object, another Graph, a customized node object, etc. (Note: Python's None object should not be used as a node as it determines whether optional function arguments have been assigned in many functions.)

+++

## Nodes

+++

The graph G can be grown in several ways. NetworkX includes many graph generator functions and facilities to read and write graphs in many formats. To get started though we'll look at simple manipulations. You can add one node at a time,

```{code-cell} ipython3
G.add_node(1)
```

add a list of nodes,

```{code-cell} ipython3
G.add_nodes_from([2, 3])
```

or add any `nbunch` of nodes. An nbunch is any iterable container of nodes that is not itself a node in the graph. (e.g. a list, set, graph, file, etc..)

```{code-cell} ipython3
H = nx.path_graph(10)
```

```{code-cell} ipython3
G.add_nodes_from(H)
```

Note that G now contains the nodes of H as nodes of G. In contrast, you could use the graph H as a node in G.

```{code-cell} ipython3
G.add_node(H)
```

The graph G now contains H as a node. This flexibility is very powerful as it allows graphs of graphs, graphs of files, graphs of functions and much more. It is worth thinking about how to structure your application so that the nodes are useful entities. Of course you can always use a unique identifier in G and have a separate dictionary keyed by identifier to the node information if you prefer. (Note: You should not change the node object if the hash depends on its contents.)

+++

## Edges

+++

G can also be grown by adding one edge at a time,

```{code-cell} ipython3
G.add_edge(1, 2)
```

```{code-cell} ipython3
e = (2, 3)
```

```{code-cell} ipython3
G.add_edge(*e) # unpack edge tuple*
```

by adding a list of edges,

```{code-cell} ipython3
G.add_edges_from([(1, 2),(1, 3)])
```

or by adding any `ebunch` of edges. An ebunch is any iterable container of edge-tuples. An edge-tuple can be a 2-tuple of nodes or a 3-tuple with 2 nodes followed by an edge attribute dictionary, e.g. (2, 3, {'weight' : 3.1415}). Edge attributes are discussed further below

```{code-cell} ipython3
G.add_edges_from(H.edges())
```

One can demolish the graph in a similar fashion; using `Graph.remove_node`, `Graph.remove_nodes_from`, `Graph.remove_edge` and `Graph.remove_edges_from`, e.g.

```{code-cell} ipython3
G.remove_node(H)
```

There are no complaints when adding existing nodes or edges. For example, after removing all nodes and edges,

```{code-cell} ipython3
G.clear()
```

we add new nodes/edges and NetworkX quietly ignores any that are already present.

```{code-cell} ipython3
G.add_edges_from([(1, 2), (1, 3)])
```

```{code-cell} ipython3
G.add_node(1)
```

```{code-cell} ipython3
G.add_edge(1, 2)
```

```{code-cell} ipython3
G.add_node("spam")       # adds node "spam"
```

```{code-cell} ipython3
G.add_nodes_from("spam") # adds 4 nodes: 's', 'p', 'a', 'm'
```

At this stage the graph G consists of 8 nodes and 2 edges, as can be seen by:

```{code-cell} ipython3
G.number_of_nodes()
```

```{code-cell} ipython3
G.number_of_edges()
```

We can examine them with

```{code-cell} ipython3
list(G.nodes())  # G.nodes() returns an iterator of nodes.
```

```{code-cell} ipython3
list(G.edges())  # G.edges() returns an iterator of edges.
```

```{code-cell} ipython3
list(G.neighbors(1))  # G.neighbors(n) returns an iterator of neigboring nodes of n
```

Removing nodes or edges has similar syntax to adding:

```{code-cell} ipython3
G.remove_nodes_from("spam")
```

```{code-cell} ipython3
list(G.nodes())
```

```{code-cell} ipython3
G.remove_edge(1, 3)
```

When creating a graph structure by instantiating one of the graph classes you can specify data in several formats.

```{code-cell} ipython3
H = nx.DiGraph(G)  # create a DiGraph using the connections from G
```

```{code-cell} ipython3
list(H.edges())
```

```{code-cell} ipython3
edgelist = [(0, 1), (1, 2), (2, 3)]
```

```{code-cell} ipython3
H = nx.Graph(edgelist)
```

## What to use as nodes and edges

+++

You might notice that nodes and edges are not specified as NetworkX objects. This leaves you free to use meaningful items as nodes and edges. The most common choices are numbers or strings, but a node can be any hashable object (except None), and an edge can be associated with any object x using `G.add_edge(n1, n2, object=x)`.

As an example, n1 and n2 could be protein objects from the RCSB Protein Data Bank, and x could refer to an XML record of publications detailing experimental observations of their interaction.

We have found this power quite useful, but its abuse can lead to unexpected surprises unless one is familiar with Python. If in doubt, consider using `convert_node_labels_to_integers` to obtain a more traditional graph with integer labels.

+++

## Accessing edges

+++

In addition to the methods `Graph.nodes`, `Graph.edges`, and `Graph.neighbors`, iterator versions (e.g. `Graph.edges_iter`) can save you from creating large lists when you are just going to iterate through them anyway.

Fast direct access to the graph data structure is also possible using subscript notation.

Warning:

Do not change the returned dict--it is part of the graph data structure and direct manipulation may leave the graph in an inconsistent state.

```{code-cell} ipython3
G[1]  # Warning: do not change the resulting dict
```

```{code-cell} ipython3
G[1][2]
```

You can safely set the attributes of an edge using subscript notation if the edge already exists.

```{code-cell} ipython3
G.add_edge(1, 3)
```

```{code-cell} ipython3
G[1][3]['color']='blue'
```

Fast examination of all edges is achieved using adjacency(iterators). Note that for undirected graphs this actually looks at each edge twice.

```{code-cell} ipython3
FG = nx.Graph()
```

```{code-cell} ipython3
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2 ,4 , 1.2), (3 ,4 , 0.375)])
```

```{code-cell} ipython3
for n,nbrs in FG.adjacency():
    for nbr,eattr in nbrs.items():
        data = eattr['weight']
        if data < 0.5:
            print('(%d, %d, %.3f)' % (n, nbr, data))
```

Convenient access to all edges is achieved with the edges method.

```{code-cell} ipython3
for (u, v, d) in FG.edges(data='weight'):
    if d < 0.5:
        print('(%d, %d, %.3f)'%(n, nbr, d))
```

## Adding attributes to graphs, nodes, and edges

+++

Attributes such as weights, labels, colors, or whatever Python object you like, can be attached to graphs, nodes, or edges.

Each graph, node, and edge can hold key/value attribute pairs in an associated attribute dictionary (the keys must be hashable). By default these are empty, but attributes can be added or changed using add_edge, add_node or direct manipulation of the attribute dictionaries named G.graph, G.node and G.edge for a graph G.


+++

### Graph attributes

+++

Assign graph attributes when creating a new graph

```{code-cell} ipython3
G = nx.Graph(day="Friday")
```

```{code-cell} ipython3
G.graph
```

Or you can modify attributes later

```{code-cell} ipython3
G.graph['day'] = 'Monday'
```

```{code-cell} ipython3
G.graph
```

### Node attributes

+++

Add node attributes using `add_node(), add_nodes_from() or G.nodes`

```{code-cell} ipython3
G.add_node(1, time='5pm')
```

```{code-cell} ipython3
G.add_nodes_from([3], time='2pm')
```

```{code-cell} ipython3
G.nodes[1]
```

```{code-cell} ipython3
G.nodes[1]['room'] = 714
```

```{code-cell} ipython3
list(G.nodes(data=True))
```

Note that adding a node to `G.node` does not add it to the graph, use `G.add_node()` to add new nodes.

+++

### Edge attributes

+++

Add edge attributes using `add_edge()`, `add_edges_from()`, subscript notation, or `G.edges`.

```{code-cell} ipython3
G.add_edge(1, 2, weight=4.7)
```

```{code-cell} ipython3
G.add_edges_from([(3, 4), (4, 5)], color='red')
```

```{code-cell} ipython3
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
```

```{code-cell} ipython3
G[1][2]['weight'] = 4.7
```

```{code-cell} ipython3
G.edges[1, 2]['weight'] = 4
```

```{code-cell} ipython3
list(G.edges(data=True))
```

The special attribute 'weight' should be numeric and holds values used by algorithms requiring weighted edges.

+++

## Directed Graphs

+++

The `DiGraph` class provides additional methods specific to directed edges, e.g. :meth:`DiGraph.out_edges`, `DiGraph.in_degree`, `DiGraph.predecessors`, `DiGraph.successors` etc. To allow algorithms to work with both classes easily, the directed versions of neighbors() and degree() are equivalent to successors() and the sum of in_degree() and out_degree() respectively even though that may feel inconsistent at times.

```{code-cell} ipython3
DG = nx.DiGraph()
```

```{code-cell} ipython3
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])
```

```{code-cell} ipython3
DG.out_degree(1, weight='weight')
```

```{code-cell} ipython3
DG.degree(1,weight='weight')
```

```{code-cell} ipython3
list(DG.successors(1))   # DG.successors(n) returns an iterator
```

```{code-cell} ipython3
list(DG.neighbors(1))   # DG.neighbors(n) returns an iterator
```

Some algorithms work only for directed graphs and others are not well defined for directed graphs. Indeed the tendency to lump directed and undirected graphs together is dangerous. If you want to treat a directed graph as undirected for some measurement you should probably convert it using `Graph.to_undirected` or with

```{code-cell} ipython3
H = nx.Graph(G) # convert G to undirected graph
```

## MultiGraphs

+++

NetworkX provides classes for graphs which allow multiple edges between any pair of nodes. The `MultiGraph` and `MultiDiGraph` classes allow you to add the same edge twice, possibly with different edge data. This can be powerful for some applications, but many algorithms are not well defined on such graphs. Shortest path is one example. Where results are well defined, e.g. `MultiGraph.degree` we provide the function. Otherwise you should convert to a standard graph in a way that makes the measurement well defined.

```{code-cell} ipython3
MG = nx.MultiGraph()
```

```{code-cell} ipython3
MG.add_weighted_edges_from([(1, 2, .5), (1, 2, .75), (2, 3, .5)])
```

```{code-cell} ipython3
list(MG.degree(weight='weight'))  # MG.degree() returns a (node, degree) iterator
```

```{code-cell} ipython3
GG = nx.Graph()
```

```{code-cell} ipython3
for n,nbrs in MG.adjacency():
    for nbr,edict in nbrs.items():
        minvalue = min([d['weight'] for d in edict.values()])
        GG.add_edge(n,nbr, weight = minvalue)
```

```{code-cell} ipython3
nx.shortest_path(GG, 1, 3)
```

## Graph generators and graph operations

+++

In addition to constructing graphs node-by-node or edge-by-edge, they can also be generated by

* Applying classic graph operations, such as:
```
subgraph(G, nbunch)      - induce subgraph of G on nodes in nbunch
union(G1,G2)             - graph union
disjoint_union(G1,G2)    - graph union assuming all nodes are different
cartesian_product(G1,G2) - return Cartesian product graph
compose(G1,G2)           - combine graphs identifying nodes common to both
complement(G)            - graph complement
create_empty_copy(G)     - return an empty copy of the same graph class
convert_to_undirected(G) - return an undirected representation of G
convert_to_directed(G)   - return a directed representation of G
```

* Using a call to one of the classic small graphs, e.g.

```{code-cell} ipython3
petersen = nx.petersen_graph()
```

```{code-cell} ipython3
tutte = nx.tutte_graph()
```

```{code-cell} ipython3
maze = nx.sedgewick_maze_graph()
```

```{code-cell} ipython3
tet = nx.tetrahedral_graph()
```

* Using a (constructive) generator for a classic graph, e.g.

```{code-cell} ipython3
K_5 = nx.complete_graph(5)
```

```{code-cell} ipython3
K_3_5 = nx.complete_bipartite_graph(3, 5)
```

```{code-cell} ipython3
barbell = nx.barbell_graph(10, 10)
```

```{code-cell} ipython3
lollipop = nx.lollipop_graph(10, 20)
```

* Using a stochastic graph generator, e.g.

```{code-cell} ipython3
er = nx.erdos_renyi_graph(100, 0.15)
```

```{code-cell} ipython3
ws = nx.watts_strogatz_graph(30, 3, 0.1)
```

```{code-cell} ipython3
ba = nx.barabasi_albert_graph(100, 5)
```

```{code-cell} ipython3
red = nx.random_lobster(100, 0.9, 0.9)
```

* Reading a graph stored in a file using common graph formats, such as edge lists, adjacency lists, GML, GraphML, pickle, LEDA and others.

```{code-cell} ipython3
nx.write_gml(red, "path.to.file")
```

```{code-cell} ipython3
mygraph = nx.read_gml("path.to.file")
```

Details on graph formats: :doc:`/reference/readwrite`

Details on graph generator functions: :doc:`/reference/generators`

+++

## Analyzing graphs

+++

The structure of G can be analyzed using various graph-theoretic functions such as:


```{code-cell} ipython3
G = nx.Graph()
```

```{code-cell} ipython3
G.add_edges_from([(1, 2), (1, 3)])
```

```{code-cell} ipython3
G.add_node("spam")       # adds node "spam"
```

```{code-cell} ipython3
list(nx.connected_components(G))
```

```{code-cell} ipython3
list(nx.connected_components(G))
```

```{code-cell} ipython3
sorted(d for n, d in nx.degree(G))
```

```{code-cell} ipython3
nx.clustering(G)
```

Functions that return node properties return (node, value) tuple iterators.


```{code-cell} ipython3
nx.degree(G)
```

```{code-cell} ipython3
list(nx.degree(G))
```

For values of specific nodes, you can provide a single node or an nbunch of nodes as argument. If a single node is specified, then a single value is returned. If an nbunch is specified, then the function will return a (node, degree) iterator.

```{code-cell} ipython3
nx.degree(G, 1)
```

```{code-cell} ipython3
G.degree(1)
```

```{code-cell} ipython3
G.degree([1, 2])
```

```{code-cell} ipython3
list(G.degree([1, 2]))
```

Details on graph algorithms supported: :doc:`/reference/algorithms`


+++

## Drawing graphs

+++

NetworkX is not primarily a graph drawing package but basic drawing with Matplotlib as well as an interface to use the open source Graphviz software package are included. These are part of the networkx.drawing package and will be imported if possible.

+++

To test if the import of networkx.drawing was successful draw G using one of

```{code-cell} ipython3
nx.draw(G)
```

```{code-cell} ipython3
nx.draw_random(G)
```

```{code-cell} ipython3
nx.draw_circular(G)
```

```{code-cell} ipython3
nx.draw_spectral(G)
```

when drawing to an interactive display. Note that you may need to issue a Matplotlib

```{code-cell} ipython3
plt.show()
```

command if you are not using matplotlib in interactive mode: (See [Matplotlib FAQ](https://matplotlib.org/stable/faq/index.html) )

To save drawings to a file, use, for example

```{code-cell} ipython3
nx.draw(G)
plt.savefig("graph.png")
```
