---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3.8.10 64-bit
    language: python
    name: python3
---

# Distance Measures in Networkx

Distance measures are used in physical cosmology to give a natural notion of the distance between two objects or eventsin the universe. They are often used to tie some observable quantity to another quantity that is not directly observable, but is more convenient for calculation.

In a graph we look at distance when it comes to connected graph. In case of a disconnected graph (G) and vertex A and B are in different components we say that the distance between A and B is infinity.
We will be looking at different aspect of distance when it comes to graph. 



```python
import networkx as nx
import matplotlib.pyplot as plt
```

## Eccentricity
It is defined as the maximum distance of one vertex from other vertex.The maximum distance between a vertex to all other vertices is considered as the eccentricity of the vertex. It is denoted by e(V). 

<br><br>
The eccentricity is very important factor, from the eccentricity of different vertices we can get the radius, diameter, center and periphery.

```python
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (6, 8), (6,9), (8,9)])
nx.draw(G, with_labels = "True")
```

```python
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (6, 8), (6,9), (8,9)])
dict(nx.eccentricity(G))
```

<!-- #region -->
The eccentricity Of G which was returned shows the maximum distance of one node to another.
Let's examine the case of node 1.


Eccentricity of node 1, it's maximum distance will be leaving from (1-2,3-6,6-9) or (1-2, 5-6, 6-8) which gives a maximum distance of 4.
so, <br> <br>
e(1) = 4 
<!-- #endregion -->

nx.eccentricity(G) returns all the nodes in our Graph along as it's eccentricity. Nevertheless, we can always precise the nodes with want.

```python
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (6, 8), (6,9), (8,9)])
dict(nx.eccentricity(G, v=[1, 6])) # This returns the eccentrity of node 1 and 6 only
```

## Diameter
The diameter of a graph is the maximum eccentricity of any vertex in the graph. That is, it is the greatest distance between any pair of vertices. To find the diameter of a graph, first find the shortest path between each pair of vertices. The greatest length of any of these paths is the diameter of the graph.


Diameter is the maximum eccentricity, if we look at the eccentricity of the graph below, the overall maximum eccentricity is 3 and hence the diameter.

```python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.eccentricity(G)

```

```python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])

color_map = []
for node in G:
    if node == (nx.diameter(G)):
        color_map.append('yellow')
    else:
        color_map.append('purple')
nx.draw(G, node_color=color_map, with_labels="True")

```

## Periphery
The Periphery has nodes, with eccentricity equal to the diameter. It denotes a sparsely connected, usally non-central set of nodes, which are linked to the core.
<br> <br> 
Therfore, 
<br>
e(V) = diameter(G) gives the periphery

```python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.periphery(G)
```

## Radius
The radius of a graph is the minumum graph eccentricity of any graph vertex in a graph. This holds for a connected graph. For a disconnected graph there is an infinite radius. The radius is also called the smallest eccentricity in a graph.

```python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.radius(G)
```

```python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
color_map = []
for node in G:
    if node == (nx.radius(G)):
        color_map.append('yellow')
    else:
        color_map.append('purple')
nx.draw(G, node_color=color_map, with_labels="True")

```

## Center
The center of a graph is the set of all vertices of minimum eccentricity,that is, the set of all vertices u where the greatest distance d(u,v) to other vertices v is minimal. Equivalently, it is the set of vertices with eccentricity equal to the graph's radius.


e(v) = radius(G) then v is the central node and the set of all such nodes makes the center of G

```python
import networkx as nx
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (7, 8), (6, 9)])
list(nx.center(G))
```

```python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.center(G)
```

## Barycenter
 The barycenter is the center of mass of two or more bodies that orbit one another and is the point about which the bodies orbit. Did you know the barycenter is sometimes called the median.

```python
G = nx.Graph([(0, 1), (1, 2), (1, 5), (5, 4), (2, 4), (2, 3), (4, 3), (3, 6)])
nx.barycenter(G)
```

## Resistance Distance
In graph theory, the resistance distance between two vertices of a simple connected graph, G, is equal to the resistance between two equivalent points on an electrical network, constructed so as to correspond to G, with each edge being replaced by a 1 ohm resistance. It is a metric on graphs.

On a graph G, the resistance distance Ωi,j between two vertices vi and vj is[1]

{\displaystyle \Omega _{i,j}:=\Gamma _{i,i}+\Gamma _{j,j}-\Gamma _{i,j}-\Gamma _{j,i}}{\displaystyle \Omega _{i,j}:=\Gamma _{i,i}+\Gamma _{j,j}-\Gamma _{i,j}-\Gamma _{j,i}}
where {\displaystyle \Gamma =\left(L+{\frac {1}{|V|}}\Phi \right)^{+}}{\displaystyle \Gamma =\left(L+{\frac {1}{|V|}}\Phi \right)^{+}}, with {\displaystyle ^{+}}{\displaystyle ^{+}} denoting the Moore–Penrose inverse, {\displaystyle L}L the Laplacian matrix of G, {\displaystyle |V|}|V| is the number of vertices in G, and {\displaystyle \Phi }\Phi  is the {\displaystyle |V|\times |V|}{\displaystyle |V|\times |V|} matrix containing all 1s.



```python
G = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4), (5, 4), (5, 3), (4, 1), (3, 6)])
nx.resistance_distance(G, 3, 5)

```

## Extrema Bounding
We can use the extrema bounding to calculate the diameter, radius, center, eccentricity , barycenter and periperal

```python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="diameter")
```

```python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="radius")

```

```python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="center")
```

```python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="periphery")
```
