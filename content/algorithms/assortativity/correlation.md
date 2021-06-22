---
jupytext:
  notebook_metadata_filter: all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.2
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
  version: 3.8.5
---

# Tutorial: Node assortativity coefficients and correlation measures

In this tutorial, we will go through the theory of assortativity and its measures. We will also see how to use their implementation at `algorithms/assortativity/correlation.py` in the networkx.

## Assortativity

Assortativity in a network refers to the tendency of nodes to connect with other similar nodes over dissimilar nodes. Here the term 'similar' can refer to many different properties from the degree or other attributes of the nodes. On the other hand, we can also have disassortativity, in which case nodes tend to connect to dissimilar nodes over similar nodes.

We may say two nodes are similar if they have the same/similar property i.e. a node $u$ is similar to $v$ if both of them have the same degree/nominal/numerical value of a property. Based on these properties we can have a different measure of assortativity for the network.

### Assortativity coefficients

Lets say we have a network $N$, $N = (V,E)$ and a poperty $P(v)$ for each node $v$.

#### Mixing matrix

Lets the property $P(v)$ take $P_0,P_1,...P_{k-1}$ distinct values on the network, then Mixing matrix is matrix $M$ such that $M[i][j]=$ number of edges from nodes with property $P_i$ to $P_j$. We can normalize mixing matrix by diving by total number of ordered edges i.e. $ e = \frac{M}{|E|}$.

Now define,

$a[i]=$ proportion of edges $(u,v)$ such that $P(u)=P_i$

$$ a[i] = \sum\limits\_{j}e[i][j] $$

$b[i]=$ proportion of edges $(u,v)$ such that $P(v)=P_i$

$$ b[i] = \sum\limits\_{j}e[j][i]$$

$\sigma_a$ and $\sigma_b$ as standard deviation of $\{\ i\cdot a[i]\ |\ i \in 0...k-1\}$ and $\{ i\cdot b[i]\ |\ i \in 0...k-1\}$ respectively. Note, after this will use subscript notation to denote indexing i.e. $P_i=P[i]$

Then we can define the assortativity coefficient for this property based on the Pearson correlation coefficient.

#### Attribute Assortativity Coefficient

Here the property $P(v)$ is a nominal property assigned to each node. As defined above we calculate the normalized mixing matrix $e$ and from that we define attribute assortativity coefficient as below.

$$ r = \frac{\sum\limits*{i}e*{ii} - \sum\limits*{i}a*{i}b*{i}}{1-\sum\limits*{i}a*{i}b*{i}} = \frac{Trace(e) - ||e^2||}{1-||e^2||}$$

It is implimented as `attribute_assortativity_coefficient`.

#### Numeric Assortativity Coefficient

Here the property $P(v)$ is a _non-negative integer_ property assigned to each node and we assume that $P[i] = i$, and the defination of the normalized mixing matrix $e$, $\sigma_a$, and $\sigma_b$ are same as above. From these we define numeric assortativity coefficient as below.

$$ r = \frac{\sum\limits*{i,j}i j(e*{ij} -a_i b_j)}{\sigma_a\sigma_b} $$

It is implimented as `numeric_assortativity_coefficient`.

#### Degree Assortativity Coefficient

When it comes to measuring degree assortativity for directed networks we have more options compared to assortativity w.r.t a property because we have 2 types of degrees, namely in-degree & out-degree. Based on the 2 types of degrees we can measure $2 \times 2 =4$ different types of assortativity.

    1. r(in,in) : Measures tendency of having a directed edge (u,v) such that, in-degree(u) = in-degree(v).
    2. r(in,out) : Measures tendency of having a directed edge (u,v) such that, in-degree(u) = out-degree(v).
    3. r(out,in) : Measures tendency of having a directed edge (u,v) such that, out-degree(u) = in-degree(v).
    4. r(out,out) : Measures tendency of having a directed edge (u,v) such that, out-degree(u) = out-degree(v).

Note: If the network is undirected all the 4 types of degree assortativity are the same.

To define the degree assortativity coefficient for all 4 types we need slight modification in the defination of $P[i]$ and $e$, and the definations of $\sigma_a$ and $\sigma_b$ remains the same.

Let $x,y \in \{in,out\}$, the property $P(\cdot)$ takes distinct values from union of the values taken by x-degree$(\cdot)$ and y-degree$(\cdot)$, and $e_{i,j}$ is the proportion of directed edges $(u,v)$ with x-degree$(u) = P[i]$ and y-degree$(v) = P[j]$.

$$ r(x,y) = \frac{\sum\limits*{i,j}i j(e*{ij} -a_i b_j)}{\sigma_a\sigma_b} $$

It is implimented as `degree_assortativity_coefficient` and `degree_pearson_correlation_coefficient`, latter one uses `scipy.stats.pearsonr` to calculate the assortativity coefficient which makes it potentally faster.

```{code-cell} ipython3
%matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import copy
import random
```

## Example

Illustrating how value of assortativity changes

```{code-cell} ipython3
gname = "g2"
G = nx.read_graphml(f"data/{gname}.graphml")
with open(f"data/pos_{gname}", 'rb') as fp:
    pos = pickle.load(fp)
```

```{code-cell} ipython3
fig, axes = plt.subplots(4, 2, figsize=(20, 20))
node_colors = [ '#b3d9ff' if G.nodes[u]['cluster'] == 'K5' else '#ffad99' for u in G.nodes ]
node_labels = { u:G.nodes[u]['num_prop'] for u in G.nodes }

for i in range(8):
    g = nx.read_graphml(f"data/{gname}_{i}.graphml")
    cr = nx.attribute_assortativity_coefficient(g, "cluster")
    r_in_out = nx.degree_assortativity_coefficient(g,x='in',y='out')
    nr = nx.numeric_assortativity_coefficient(g, "num_prop")

    nx.draw_networkx_nodes(g, pos=pos, node_size=300,ax=axes[i//2][i%2],node_color = node_colors)
    nx.draw_networkx_labels(g, pos=pos, labels = node_labels,ax=axes[i//2][i%2])
    nx.draw_networkx_edges(g, pos=pos, ax=axes[i//2][i%2],edge_color='0.7')
    axes[i//2][i%2].set_title(f"Attribute assortativity coefficient = {cr:.3}\nNumeric assortativity coefficient = {nr:.3}\nr(in,out) = {r_in_out:.3}", size=15)

fig.tight_layout()
```

Nodes are colored by the `cluster` property and labeled by `num_prop` property. We can observe that the initial network on left side is completely assortative and its compliment on right side is completely disassortative. As we add edges between nodes of different (similar) attributes in the assortative (disassortative) network, the network tends to a non-assortative network and value of both the assortaivity coefficients tends to $0$.

+++

The parameter `nodes` in `attribute_assortativity_coefficient` and `numeric_assortativity_coefficient` specifies the nodes who's edges are to be considered in the mixing matrix calculation. That is to say, if $(u,v)$ is a directed edge then the edge $(u,v)$ will be used in mixing matrix calculation if $u$ is in `nodes` and for undirected case its considered if atleast one of the $u,v$ in in `nodes`.

Whereas the parameter `nodes` in `degree_assortativity_coefficient` and `degree_pearson_correlation_coefficient` specifies the nodes whose subgraph's edges are considered in the mixing matrix calculation.

```{code-cell} ipython3
nodes_list = [None,
              [str(i) for i in range(3)],
              [str(i) for i in range(4)],
              [str(i) for i in range(5)],
              [str(i) for i in range(4,8)],
              [str(i) for i in range(5,10)]]
fig, axes = plt.subplots(3, 2, figsize=(20, 16))

def color_node(u, nodes):
    """Utility function to give the color of a node based on its attribute """
    if u not in nodes:
        return '0.85'
    if G.nodes[u]['cluster'] == 'K5':
        return '#b3d9ff'
    else:
        return '#ffad99'

G.add_edge('4','5')

for nodes, ax in zip(nodes_list, axes.ravel()):
    cr = nx.attribute_assortativity_coefficient(G, 'cluster',nodes=nodes)
    nr = nx.numeric_assortativity_coefficient(G, 'num_prop',nodes=nodes)
    ax.set_title(f"Attribute assortativity coefficient: {cr:.3}\nNumeric assortativity coefficient: {nr:.3}\nNodes = {nodes}",size=15)

    if nodes is None:
        nodes = [u for u in G.nodes()]
    node_colors = [ color_node(u, nodes) for u in G.nodes ]
    nx.draw_networkx_nodes(G,pos=pos, node_size=450,ax=ax,node_color = node_colors)
    nx.draw_networkx_labels(G,pos,labels={u:u for u in G.nodes},font_size=15,ax=ax)
    nx.draw_networkx_edges(G,pos=pos,edgelist=[ (u,v) for u,v in G.edges if u in nodes ],ax=ax,edge_color='0.3')
fig.tight_layout()
```

In the above plots only the nodes which are considred are colored and rest are grayed out and only the edges which are considerd in the assortaivty calculation are drawn.

+++

[^1] M. E. J. Newman, Mixing patterns in networks https://doi.org/10.1103/PhysRevE.67.026126

[^2] Foster, J.G., Foster, D.V., Grassberger, P. & Paczuski, M. Edge direction and the structure of networks https://doi.org/10.1073/pnas.0912671107
