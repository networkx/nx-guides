# CHECK PLANARITY

## Planarity Algorithm in NetworkX

## Introduction
A graph is said to be **planar** if it can be drawn on a plane without any of its edges crossing. The `check_planarity` function in NetworkX helps determine whether a given graph is planar and provides either an embedding or a counterexample.

### Mathematical Background
A graph is **planar** if and only if it does not contain a subgraph homeomorphic to **K₅ (complete graph on 5 vertices)** or **K₃,₃ (complete bipartite graph with partition sizes 3 and 3)**. This is known as **Kuratowski’s theorem**.

The planarity check in NetworkX is based on the **Left-Right Planarity Test**, an efficient combinatorial method to determine planarity.

---



***What is  Left-Right Planarity Test***

The Left-Right Planarity Test is a linear-time algorithm used to check whether a graph is planar—that is, drawable in the plane without edge crossings. This test forms the core of the networkx.check_planarity() function.

***How It Works (Conceptually):***



1. *Depth-First Search (DFS):*  
The algorithm starts by building a DFS tree of the input graph, which helps classify edges into tree edges and back edges.
2. *Lowpoints and Embedding Constraints:*  
For each vertex, the algorithm computes "lowpoints"—the smallest reachable ancestor in DFS. It uses this to decide how back edges can be placed to the left or right of tree edges without crossings.
3. *Conflict Detection:*  
The algorithm tracks embedding constraints between edges. If it detects a conflict (e.g., an edge that can't be placed without violating planarity), it concludes the graph is non-planar.
4. *Constructs a Planar Embedding or Finds Obstruction:*  
If the graph is planar, it returns a combinatorial embedding (rotation system). If not, it can identify a Kuratowski subgraph (e.g., K₅ or K₃,₃).






```python
from functools import singledispatch
```


```python
from collections import defaultdict
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
```


```python
__all__ = ["check_planarity", "is_planar", "PlanarEmbedding"]
```

## Parameters

G: NetworkX graph
counterexample : bool
A Kuratowski subgraph (to prove non planarity) is only returned if set to true.


What is ***Kuratowski subgraph*** ?

A Kuratowski subgraph is a specific subgraph that serves as evidence that a graph is not planar. According to Kuratowski’s Theorem, a graph is non-planar if and only if it contains a subgraph that is a subdivision (i.e., homeomorphic copy) of either **K₅ (the complete graph on 5 vertices)** or **K₃,₃ (the complete bipartite graph with partitions of size 3)**. These subgraphs are called Kuratowski subgraphs.

They may not appear in their exact form but can be present in a stretched-out version where edges are replaced by paths. NetworkX uses this principle internally: *if check_planarity() returns False, it indicates the existence of a Kuratowski subgraph obstructing planar embedding.*

---



## Returns

The function returns a tuple of the form:


*   is_planar (bool):
  *   True if the graph is planar.
  *   False if the graph is non-planar.

*   certificate (NetworkX graph):
  *   If is_planar is True, certificate will be a PlanarEmbedding object representing a valid planar embedding of the graph.
  *   If is_planar is False, certificate will be a Kuratowski subgraph, which is a subgraph of the original graph that proves the graph is non-planar by being a homeomorphic copy of K₅ or K₃,₃.

---




```python
from networkx.algorithms.planarity import LRPlanarity
```


```python
def is_planar(G):
    return check_planarity(G, counterexample=False)[0]
```


```python
def check_planarity(G, counterexample=False):
    planarity_state = LRPlanarity(G)
    embedding = planarity_state.lr_planarity()
    if embedding is None:
        # graph is not planar
        if counterexample:
            return False, get_counterexample(G)
        else:
            return False, None
    else:
        # graph is planar
        return True, embedding
```


```python
#Example 1
# Load GraphML file
G = nx.read_graphml("./data/planar_graph.graphml")

# Draw the graph
pos = nx.planar_layout(G)  # Planar layout for better visualization
plt.figure(figsize=(6, 6))
nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='black', node_size=500, font_size=12)
plt.title("Planar Graph from GraphML")
plt.show()
```


    
![png](planarity_files/planarity_11_0.png)
    



```python
#Example 2
# Load GraphML file
G = nx.read_graphml("./data/non_planar_k3_3.graphml")

# Draw the graph
pos = nx.spring_layout(G)  # Spring layout for visualization
plt.figure(figsize=(6, 6))
nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='black', node_size=500, font_size=12)
plt.title("Non-Planar Graph (K3,3) from GraphML")
plt.show()
```


    
![png](planarity_files/planarity_12_0.png)
    


## Check Planarity Recusrivly
The function check_planarity_recursive recursively checks whether a graph G is planar. It uses a method lr_planarity_recursive from the LRPlanarity class to determine planarity. If the graph is planar, it returns True along with a PlanarEmbedding. If the graph is non-planar, it either returns False and a counterexample (if the counterexample=True flag is set) or just False with no counterexample. The recursive nature of the function allows it to break down the problem in smaller steps, examining the graph’s structure in a depth-first manner to assess its planarity.

---




```python
def check_planarity_recursive(G, counterexample=False):
    """Recursive version of :meth:`check_planarity`."""
    planarity_state = LRPlanarity(G)
    embedding = planarity_state.lr_planarity_recursive()
    if embedding is None:
        # graph is not planar
        if counterexample:
            return False, get_counterexample_recursive(G)
        else:
            return False, None
    else:
        # graph is planar
        return True, embedding
```


```python
# Example 1: Planar Graph
# Load GraphML file
G = nx.read_graphml("./data/planar_graph.graphml")

# Draw the graph
pos = nx.planar_layout(G)  # Planar layout for better visualization
plt.figure(figsize=(6, 6))
nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='black', node_size=500, font_size=12)
plt.title("Planar Graph from GraphML")
plt.show()
```


    
![png](planarity_files/planarity_15_0.png)
    


## Notes

**Embedding** - A (combinatorial) embedding consists of cyclic orderings of the incident edges at each vertex. Given such an embedding there are multiple approaches discussed in literature to drawing the graph (subject to various constraints, e.g. integer coordinates), see e.g. [2].



The planarity check algorithm and extraction of the combinatorial embedding is based on the Left-Right Planarity Test [1].



A counterexample is only generated if the corresponding parameter is set, because the complexity of the counterexample generation is higher.

## IS_PLANAR

## Planarity:
A graph is planar if it can be drawn on a plane without edges crossing.

## Kuratawoski's Theorem:
A graph is not planar if it contains a subgraph that is homeomorphic to K5 or K3,3.

## NetworkX's is_planar(G) function
determines whether a given graph is planar.

---



## Parameters:

*   G: NetworkX graph  
The graph to be checked for planarity.

---




## Returns

*   bool:
  *   True if the graph is planar.
  *   False if the graph is non-planar.


---




```python
# Example 3: A simple planar graph
# Load GraphML file
G = nx.read_graphml("./data/simple_planar_graph.graphml")

# Draw the graph
pos = nx.spring_layout(G)  # Spring layout for visualization
plt.figure(figsize=(4, 4))
nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='black', node_size=500, font_size=12)
plt.title("Simple Planar Graph from GraphML")
plt.show()
```


    
![png](planarity_files/planarity_20_0.png)
    



```python
#Example 4
# Load GraphML file
G = nx.read_graphml("./data/K5_nonplanar.graphml")

# Draw the graph
pos = nx.spring_layout(G)  # Spring layout for visualization
plt.figure(figsize=(4, 4))
nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='black', node_size=500, font_size=12)
plt.title("Complete Graph K5 (Non-Planar)")
plt.show()
```


    
![png](planarity_files/planarity_21_0.png)
    


## Planar Embedding

## Planar Embedding in NetworkX

*Class PlanarEmbedding:* This class represents a planar graph along with its planar embedding.


A planar embedding is a way to represent a graph in the plane such that no edges cross, and it is given by a combinatorial embedding. This embedding stores the cyclic order of edges around each vertex, which is essential for visualizing the graph in a planar form.

---



## Combinatorial embedding

**Main article: Rotation system**

An embedded graph uniquely defines cyclic orders of edges incident to the same vertex. The set of all these cyclic orders is called a rotation system. Embeddings with the same rotation system are considered to be equivalent and the corresponding equivalence class of embeddings is called combinatorial embedding (as opposed to the term topological embedding, which refers to the previous definition in terms of points and curves). Sometimes, the rotation system itself is called a "combinatorial embedding".[3][4][5]

An embedded graph also defines natural cyclic orders of edges which constitutes the boundaries of the faces of the embedding. However handling these face-based orders is less straightforward, since in some cases some edges may be traversed twice along a face boundary. For example this is always the case for embeddings of trees, which have a single face. To overcome this combinatorial nuisance, one may consider that every edge is "split" lengthwise in two "half-edges", or "sides". Under this convention in all face boundary traversals each half-edge is traversed only once and the two half-edges of the same edge are always traversed in opposite directions.

Other equivalent representations for cellular embeddings include the ribbon graph, a topological space formed by gluing together topological disks for the vertices and edges of an embedded graph, and the graph-encoded map, an edge-colored cubic graph with four vertices for each edge of the embedded graph.

## Neighbor ordering:
In comparison to a usual graph structure, the embedding also stores the order of all neighbors for every vertex. The order of the neighbors can be given in clockwise (cw) direction or counterclockwise (ccw) direction. This order is stored as edge attributes in the underlying directed graph. For the edge (u, v) the edge attribute ‘cw’ is set to the neighbor of u that follows immediately after v in clockwise direction.

In order for a PlanarEmbedding to be valid it must fulfill multiple conditions. It is possible to check if these conditions are fulfilled with the method check_structure(). The conditions are:
1. Edges must go in both directions (because the edge attributes differ)
2. Every edge must have a ‘cw’ and ‘ccw’ attribute which corresponds to a correct planar embedding.

As long as a PlanarEmbedding is invalid only the following methods should be called:

1. add_half_edge()
2. connect_components()

Even though the graph is a subclass of nx.DiGraph, it can still be used for algorithms that require undirected graphs, because the method is_directed() is overridden. This is possible, because a valid PlanarGraph must have edges in both directions.

## Half edges:
In methods like add_half_edge the term “half-edge” is used, which is a term that is used in doubly connected edge lists. It is used to emphasize that the edge is only in one direction and there exists another half-edge in the opposite direction. While conventional edges always have two faces (including outer face) next to them, it is possible to assign each half-edge exactly one face. For a half-edge (u, v) that is oriented such that u is below v then the face that belongs to (u, v) is to the right of this half-edge.

---



## Parameters:


*   *incoming_graph_data :*  
graph (optional, default: None)
Data used to initialize the graph. If None (default), an empty graph is created. It can be an edge list or any NetworkX graph object. If the relevant Python packages are installed, it can also be a 2D NumPy array, a SciPy sparse matrix, or a PyGraphviz graph.
*   *attr :*  
keyword arguments, optional (default: no attributes)
Attributes to add to the graph, provided as key-value pairs.

---




```python
class PlanarEmbedding(nx.DiGraph):
    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data=incoming_graph_data, **attr)
        self.add_edge = self.__forbidden
        self.add_edges_from = self.__forbidden
        self.add_weighted_edges_from = self.__forbidden



    def __forbidden(self, *args, **kwargs):
        """Forbidden operation

        Any edge additions to a PlanarEmbedding should be done using
        method `add_half_edge`.
        """
        raise NotImplementedError(
            "Use `add_half_edge` method to add edges to a PlanarEmbedding."
        )

    def get_data(self):
        """Converts the adjacency structure into a better readable structure.

        Returns
        -------
        embedding : dict
            A dict mapping all nodes to a list of neighbors sorted in
            clockwise order.

        See Also
        --------
        set_data

        """
        embedding = {}
        for v in self:
            embedding[v] = list(self.neighbors_cw_order(v))
        return embedding


    def set_data(self, data):
        """Inserts edges according to given sorted neighbor list.

        The input format is the same as the output format of get_data().

        Parameters
        ----------
        data : dict
            A dict mapping all nodes to a list of neighbors sorted in
            clockwise order.

        See Also
        --------
        get_data

        """
        for v in data:
            ref = None
            for w in reversed(data[v]):
                self.add_half_edge(v, w, cw=ref)
                ref = w

    def remove_node(self, n):
        """Remove node n.

        Removes the node n and all adjacent edges, updating the
        PlanarEmbedding to account for any resulting edge removal.
        Attempting to remove a non-existent node will raise an exception.

        Parameters
        ----------
        n : node
           A node in the graph

        Raises
        ------
        NetworkXError
           If n is not in the graph.

        See Also
        --------
        remove_nodes_from

        """
        try:
            for u in self._pred[n]:
                succs_u = self._succ[u]
                un_cw = succs_u[n]["cw"]
                un_ccw = succs_u[n]["ccw"]
                del succs_u[n]
                del self._pred[u][n]
                if n != un_cw:
                    succs_u[un_cw]["ccw"] = un_ccw
                    succs_u[un_ccw]["cw"] = un_cw
            del self._node[n]
            del self._succ[n]
            del self._pred[n]
        except KeyError as err:  # NetworkXError if n not in self
            raise nx.NetworkXError(
                f"The node {n} is not in the planar embedding."
            ) from err
        nx._clear_cache(self)


    def remove_nodes_from(self, nodes):
        """Remove multiple nodes.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes (list, dict, set, etc.).  If a node
            in the container is not in the graph it is silently ignored.

        See Also
        --------
        remove_node

        Notes
        -----
        When removing nodes from an iterator over the graph you are changing,
        a `RuntimeError` will be raised with message:
        `RuntimeError: dictionary changed size during iteration`. This
        happens when the graph's underlying dictionary is modified during
        iteration. To avoid this error, evaluate the iterator into a separate
        object, e.g. by using `list(iterator_of_nodes)`, and pass this
        object to `G.remove_nodes_from`.

        """
        for n in nodes:
            if n in self._node:
                self.remove_node(n)


            # silently skip non-existing nodes

    def neighbors_cw_order(self, v):
        """Generator for the neighbors of v in clockwise order.

        Parameters
        ----------
        v : node

        Yields
        ------
        node

        """
        succs = self._succ[v]
        if not succs:
            # v has no neighbors
            return
        start_node = next(reversed(succs))
        yield start_node
        current_node = succs[start_node]["cw"]
        while start_node != current_node:
            yield current_node
            current_node = succs[current_node]["cw"]

    def add_half_edge(self, start_node, end_node, *, cw=None, ccw=None):
        """Adds a half-edge from `start_node` to `end_node`.

        If the half-edge is not the first one out of `start_node`, a reference
        node must be provided either in the clockwise (parameter `cw`) or in
        the counterclockwise (parameter `ccw`) direction. Only one of `cw`/`ccw`
        can be specified (or neither in the case of the first edge).
        Note that specifying a reference in the clockwise (`cw`) direction means
        inserting the new edge in the first counterclockwise position with
        respect to the reference (and vice-versa).

        Parameters
        ----------
        start_node : node
            Start node of inserted edge.
        end_node : node
            End node of inserted edge.
        cw, ccw: node
            End node of reference edge.
            Omit or pass `None` if adding the first out-half-edge of `start_node`.


        Raises
        ------
        NetworkXException
            If the `cw` or `ccw` node is not a successor of `start_node`.
            If `start_node` has successors, but neither `cw` or `ccw` is provided.
            If both `cw` and `ccw` are specified.

        See Also
        --------
        connect_components
        """

        succs = self._succ.get(start_node)
        if succs:
            # there is already some edge out of start_node
            leftmost_nbr = next(reversed(self._succ[start_node]))
            if cw is not None:
                if cw not in succs:
                    raise nx.NetworkXError("Invalid clockwise reference node.")
                if ccw is not None:
                    raise nx.NetworkXError("Only one of cw/ccw can be specified.")
                ref_ccw = succs[cw]["ccw"]
                super().add_edge(start_node, end_node, cw=cw, ccw=ref_ccw)
                succs[ref_ccw]["cw"] = end_node
                succs[cw]["ccw"] = end_node
                # when (cw == leftmost_nbr), the newly added neighbor is
                # already at the end of dict self._succ[start_node] and
                # takes the place of the former leftmost_nbr
                move_leftmost_nbr_to_end = cw != leftmost_nbr
            elif ccw is not None:
                if ccw not in succs:
                    raise nx.NetworkXError("Invalid counterclockwise reference node.")
                ref_cw = succs[ccw]["cw"]
                super().add_edge(start_node, end_node, cw=ref_cw, ccw=ccw)
                succs[ref_cw]["ccw"] = end_node
                succs[ccw]["cw"] = end_node
                move_leftmost_nbr_to_end = True
            else:
                raise nx.NetworkXError(
                    "Node already has out-half-edge(s), either cw or ccw reference node required."
                )
            if move_leftmost_nbr_to_end:
                # LRPlanarity (via self.add_half_edge_first()) requires that
                # we keep track of the leftmost neighbor, which we accomplish
                # by keeping it as the last key in dict self._succ[start_node]
                succs[leftmost_nbr] = succs.pop(leftmost_nbr)

        else:
            if cw is not None or ccw is not None:
                raise nx.NetworkXError("Invalid reference node.")
            # adding the first edge out of start_node
            super().add_edge(start_node, end_node, ccw=end_node, cw=end_node)


    def check_structure(self):
        """Runs without exceptions if this object is valid.

        Checks that the following properties are fulfilled:

        * Edges go in both directions (because the edge attributes differ).
        * Every edge has a 'cw' and 'ccw' attribute which corresponds to a
          correct planar embedding.

        Running this method verifies that the underlying Graph must be planar.

        Raises
        ------
        NetworkXException
            This exception is raised with a short explanation if the
            PlanarEmbedding is invalid.
        """
        # Check fundamental structure
        for v in self:
            try:
                sorted_nbrs = set(self.neighbors_cw_order(v))
            except KeyError as err:
                msg = f"Bad embedding. Missing orientation for a neighbor of {v}"
                raise nx.NetworkXException(msg) from err

            unsorted_nbrs = set(self[v])
            if sorted_nbrs != unsorted_nbrs:
                msg = "Bad embedding. Edge orientations not set correctly."
                raise nx.NetworkXException(msg)
            for w in self[v]:
                # Check if opposite half-edge exists
                if not self.has_edge(w, v):
                    msg = "Bad embedding. Opposite half-edge is missing."
                    raise nx.NetworkXException(msg)

        # Check planarity
        counted_half_edges = set()
        for component in nx.connected_components(self):
            if len(component) == 1:
                # Don't need to check single node component
                continue
            num_nodes = len(component)
            num_half_edges = 0
            num_faces = 0
            for v in component:
                for w in self.neighbors_cw_order(v):
                    num_half_edges += 1
                    if (v, w) not in counted_half_edges:
                        # We encountered a new face
                        num_faces += 1
                        # Mark all half-edges belonging to this face
                        self.traverse_face(v, w, counted_half_edges)
            num_edges = num_half_edges // 2  # num_half_edges is even
            if num_nodes - num_edges + num_faces != 2:
                # The result does not match Euler's formula
                msg = "Bad embedding. The graph does not match Euler's formula"
                raise nx.NetworkXException(msg)


    def add_half_edge_ccw(self, start_node, end_node, reference_neighbor):
        """Adds a half-edge from start_node to end_node.

        The half-edge is added counter clockwise next to the existing half-edge
        (start_node, reference_neighbor).

        Parameters
        ----------
        start_node : node
            Start node of inserted edge.
        end_node : node
            End node of inserted edge.
        reference_neighbor: node
            End node of reference edge.

        Raises
        ------
        NetworkXException
            If the reference_neighbor does not exist.

        See Also
        --------
        add_half_edge
        add_half_edge_cw
        connect_components

        """
        self.add_half_edge(start_node, end_node, cw=reference_neighbor)


    def add_half_edge_cw(self, start_node, end_node, reference_neighbor):
        """Adds a half-edge from start_node to end_node.

        The half-edge is added clockwise next to the existing half-edge
        (start_node, reference_neighbor).

        Parameters
        ----------
        start_node : node
            Start node of inserted edge.
        end_node : node
            End node of inserted edge.
        reference_neighbor: node
            End node of reference edge.

        Raises
        ------
        NetworkXException
            If the reference_neighbor does not exist.

        See Also
        --------
        add_half_edge
        add_half_edge_ccw
        connect_components
        """
        self.add_half_edge(start_node, end_node, ccw=reference_neighbor)



    def remove_edge(self, u, v):
        """Remove the edge between u and v.

        Parameters
        ----------
        u, v : nodes
        Remove the half-edges (u, v) and (v, u) and update the
        edge ordering around the removed edge.

        Raises
        ------
        NetworkXError
        If there is not an edge between u and v.

        See Also
        --------
        remove_edges_from : remove a collection of edges
        """
        try:
            succs_u = self._succ[u]
            succs_v = self._succ[v]
            uv_cw = succs_u[v]["cw"]
            uv_ccw = succs_u[v]["ccw"]
            vu_cw = succs_v[u]["cw"]
            vu_ccw = succs_v[u]["ccw"]
            del succs_u[v]
            del self._pred[v][u]
            del succs_v[u]
            del self._pred[u][v]
            if v != uv_cw:
                succs_u[uv_cw]["ccw"] = uv_ccw
                succs_u[uv_ccw]["cw"] = uv_cw
            if u != vu_cw:
                succs_v[vu_cw]["ccw"] = vu_ccw
                succs_v[vu_ccw]["cw"] = vu_cw
        except KeyError as err:
            raise nx.NetworkXError(
                f"The edge {u}-{v} is not in the planar embedding."
            ) from err
        nx._clear_cache(self)

    def remove_edges_from(self, ebunch):
        """Remove all edges specified in ebunch.

        Parameters
        ----------
        ebunch: list or container of edge tuples
            Each pair of half-edges between the nodes given in the tuples
            will be removed from the graph. The nodes can be passed as:

                - 2-tuples (u, v) half-edges (u, v) and (v, u).
                - 3-tuples (u, v, k) where k is ignored.

        See Also
        --------
        remove_edge : remove a single edge

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the graph.

        Examples
        --------
        >>> G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> ebunch = [(1, 2), (2, 3)]
        >>> G.remove_edges_from(ebunch)
        """
        for e in ebunch:
            u, v = e[:2]  # ignore edge data
            # assuming that the PlanarEmbedding is valid, if the half_edge
            # (u, v) is in the graph, then so is half_edge (v, u)
            if u in self._succ and v in self._succ[u]:
                self.remove_edge(u, v)


    def connect_components(self, v, w):
        """Adds half-edges for (v, w) and (w, v) at some position.

        This method should only be called if v and w are in different
        components, or it might break the embedding.
        This especially means that if `connect_components(v, w)`
        is called it is not allowed to call `connect_components(w, v)`
        afterwards. The neighbor orientations in both directions are
        all set correctly after the first call.

        Parameters
        ----------
        v : node
        w : node

        See Also
        --------
        add_half_edge
        """
        if v in self._succ and self._succ[v]:
            ref = next(reversed(self._succ[v]))
        else:
            ref = None
        self.add_half_edge(v, w, cw=ref)
        if w in self._succ and self._succ[w]:
            ref = next(reversed(self._succ[w]))
        else:
            ref = None
        self.add_half_edge(w, v, cw=ref)

    def add_half_edge_first(self, start_node, end_node):
        """Add a half-edge and set end_node as start_node's leftmost neighbor.

        The new edge is inserted counterclockwise with respect to the current
        leftmost neighbor, if there is one.

        Parameters
        ----------
        start_node : node
        end_node : node

        See Also
        --------
        add_half_edge
        connect_components
        """
        succs = self._succ.get(start_node)
        # the leftmost neighbor is the last entry in the
        # self._succ[start_node] dict
        leftmost_nbr = next(reversed(succs)) if succs else None
        self.add_half_edge(start_node, end_node, cw=leftmost_nbr)

    def next_face_half_edge(self, v, w):
        """Returns the following half-edge left of a face.

        Parameters
        ----------
        v : node
        w : node

        Returns
        -------
        half-edge : tuple
        """
        new_node = self[w][v]["ccw"]
        return w, new_node


    def traverse_face(self, v, w, mark_half_edges=None):
        """Returns nodes on the face that belong to the half-edge (v, w).

        The face that is traversed lies to the right of the half-edge (in an
        orientation where v is below w).

        Optionally it is possible to pass a set to which all encountered half
        edges are added. Before calling this method, this set must not include
        any half-edges that belong to the face.

        Parameters
        ----------
        v : node
            Start node of half-edge.
        w : node
            End node of half-edge.
        mark_half_edges: set, optional
            Set to which all encountered half-edges are added.

        Returns
        -------
        face : list
            A list of nodes that lie on this face.
        """
        if mark_half_edges is None:
            mark_half_edges = set()

        face_nodes = [v]
        mark_half_edges.add((v, w))
        prev_node = v
        cur_node = w
        # Last half-edge is (incoming_node, v)
        incoming_node = self[v][w]["cw"]

        while cur_node != v or prev_node != incoming_node:
            face_nodes.append(cur_node)
            prev_node, cur_node = self.next_face_half_edge(prev_node, cur_node)
            if (prev_node, cur_node) in mark_half_edges:
                raise nx.NetworkXException("Bad planar embedding. Impossible face.")
            mark_half_edges.add((prev_node, cur_node))

        return face_nodes

    def is_directed(self):
        """A valid PlanarEmbedding is undirected.

        All reverse edges are contained, i.e. for every existing
        half-edge (v, w) the half-edge in the opposite direction (w, v) is also
        contained.
        """
        return False

    def copy(self, as_view=False):
        if as_view is True:
            return nx.graphviews.generic_graph_view(self)
        G = self.__class__()
        G.graph.update(self.graph)
        G.add_nodes_from((n, d.copy()) for n, d in self._node.items())
        super(self.__class__, G).add_edges_from(
            (u, v, datadict.copy())
            for u, nbrs in self._adj.items()
            for v, datadict in nbrs.items()
        )
        return G
```


```python
# Load GraphML file
G = nx.read_graphml("./data/planar_embedding.graphml")

# Check if the graph is planar
is_planar, embedding = nx.check_planarity(G, counterexample=False)

if is_planar:
    print("The graph is planar.")

    # Generate a planar embedding layout
    pos = nx.planar_layout(G)

    # Draw the graph
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='black', node_size=500, font_size=12)
    plt.title("Planar Graph with Visualization")
    plt.show()
else:
    print("The graph is not planar.")
```

    The graph is planar.
    


    
![png](planarity_files/planarity_28_1.png)
    


## Summary
**Planarity in NetworkX**

A planar graph can be embedded in the plane without any edge crossings. NetworkX provides functions to check whether a graph is planar using the Left-Right Planarity Test. This test determines if a graph is planar based on combinatorial embeddings.

*   *check_planarity():* Returns a tuple (is_planar, certificate), where is_planar is a boolean indicating if the graph is planar, and certificate is either a PlanarEmbedding (for planar graphs) or a Kuratowski subgraph (for non-planar graphs).
*   *PlanarEmbedding class:* Represents a planar graph and its embedding, which is described by a combinatorial embedding that stores the cyclic order of edges around each vertex.
*   *Recursive Planarity Check:* The function check_planarity_recursive() checks planarity using recursion, returning a counterexample for non-planar graphs when requested.

**Key Concepts:**

*   *Kuratowski’s Theorem:*  A graph is non-planar if it contains a subgraph homeomorphic to K₅ or K₃,₃.
*   *PlanarEmbedding:*  Encodes a valid planar graph embedding, ensuring no edge crossings in the planar layout.

---








## References
[1]
Ulrik Brandes: The Left-Right Planarity Test 2009 http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.217.9208



[2]
Takao Nishizeki, Md Saidur Rahman: Planar graph drawing Lecture Notes Series on Computing: Volume 12 2004

[3] J. Edmonds, A Combinatorial Representation for Polyhedral Surfaces, 1960.

[4] J.L. Gross and T.W. Tucker, Topological Graph Theory, 1987.

[5] R. Cori and A. Machì, Maps, Hypermaps and Their Automorphisms, Expositiones Mathematicae, 1982.

---


