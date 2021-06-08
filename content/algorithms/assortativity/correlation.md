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

In this tutorial, we will go through the theory of assortativity and its measures. We will also see how to use their implementation at `algorithms/assortativity/correlation.py` in the network.

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

Here the property $P(v)$ is a numerical property assigned to each node. And just as above we use the same defination of the normalized mixing matrix $e$ and $\sigma_a$ and $\sigma_b$ defined above to define the numeric assortativity coefficient as below.

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

## Attribute and Numeric Assortativity Coefficient

```{code-cell} ipython3
G = nx.read_graphml("data/base.graphml")
with open("data/pos", 'rb') as fp:
    pos = pickle.load(fp)
```

```{code-cell} ipython3
g = copy.deepcopy(G)
edge_list = list(nx.complement(g).edges())
random.shuffle(edge_list)

def add_new_edges(edge_incriment):
    """Utility function to add edges randomly which are not there in G"""
    while edge_incriment > 0 and len(edge_list) > 0:
        e = edge_list.pop()
        g.add_edge(e[0],e[1])
        edge_incriment-=1

edge_incriments = [50,150,250,350,450,550]
fig, axes = plt.subplots(3, 2, figsize=(20, 20))
edge_count = []
cr_list, nr_list = [], []
for ei, ax in zip(edge_incriments,axes.ravel()):
    nx.draw(g, pos=pos, ax=ax, node_size=10, width=0.5)

    cr = nx.attribute_assortativity_coefficient(g, "cluster")
    nr = nx.numeric_assortativity_coefficient(g, "num_prop")

    ax.set_title(f"Attribute assortativity coefficient = {cr:.3}\nNumeric assortativity coefficient = {nr:.3}", size=15)
    edge_count.append(g.number_of_edges())
    cr_list.append(cr)
    nr_list.append(nr)
    add_new_edges(ei)
fig.tight_layout()
```

We can observe that the value of assortativity coefficients decreases as we add edges between different clusters.

```{code-cell} ipython3
plt.figure(figsize=(16,8))
plt.plot(edge_count,cr_list,'go--',label="Attribute assortativity coefficient",markersize=10)
plt.plot(edge_count,nr_list,'ro--',label="Numeric assortativity coefficient",markersize=10)
plt.xlabel("Number of edges",fontsize=14)
plt.ylabel("Assortativity measure",fontsize=14)
plt.legend(fontsize=12)
plt.show()
```

The parameter `nodes` in `attribute_assortativity_coefficient`, `numeric_assortativity_coefficient`, `degree_assortativity_coefficient`, and `degree_pearson_correlation_coefficient` specifies the nodes whos edges are to be considered in the mixing matrix calculation.

Note: If $u$ is in `nodes` and $(u,v)$ is a directed edge and even if $v$ is not in `nodes` the edge $(u,v)$ will be used in mixing matrix calculation.

```{code-cell} ipython3
nodes_list = [None,
              [str(i) for i in range(3)],
              [str(i) for i in range(4)],
              [str(i) for i in range(5)],
              [str(i) for i in range(4,12)],
              [str(i) for i in range(5,12)]]
fig, axes = plt.subplots(3, 2, figsize=(20, 20))

for nodes, ax in zip(nodes_list, axes.ravel()):
    nx.draw_networkx(G,pos=pos,node_size=350, width=0.5,ax=ax,font_size=15,node_color='w')
    ax.set_title(f"""Attribute assortativity coefficient: {nx.attribute_assortativity_coefficient(G, 'cluster',nodes=nodes):.3}\nNumeric assortativity coefficient: {nx.numeric_assortativity_coefficient(G, 'num_prop',nodes=nodes):.3}\nNodes = {nodes}""",size=15)
    G.add_edge('3','4')
fig.tight_layout()
```

## Degree Assortativity Coefficients

```{code-cell} ipython3
G = nx.read_graphml("data/base_degree.graphml")
with open("data/pos_degree", 'rb') as fp:
    pos = pickle.load(fp)
```

```{code-cell} ipython3
g = copy.deepcopy(G)
edge_list = list(nx.complement(g).edges())
random.shuffle(edge_list)

edge_incriments = [0,27,47,87,167,248]
fig, axes = plt.subplots(3, 2, figsize=(20, 20))
edge_count = []
r_in_in_list, r_in_out_list,r_out_in_list,r_out_out_list = [], [], [], []
for ei, ax in zip(edge_incriments,axes.ravel()):
    add_new_edges(ei)
    nx.draw(g, pos=pos, ax=ax, node_size=10, width=0.5)

    r_in_in = nx.degree_assortativity_coefficient(g,x='in',y='in')
    r_in_out = nx.degree_assortativity_coefficient(g,x='in',y='out')
    r_out_in = nx.degree_assortativity_coefficient(g,x='out',y='in')
    r_out_out = nx.degree_assortativity_coefficient(g,x='out',y='out')

    ax.set_title(f"r(in,in) = {r_in_in:.3}    r(in,out) = {r_in_out:.3}\nr(out,in) = {r_out_in:.3}    r(out,out) = {r_out_out:.3}", size=15)
    edge_count.append(g.number_of_edges())
    r_in_in_list.append(r_in_in)
    r_in_out_list.append(r_in_out)
    r_out_in_list.append(r_out_in)
    r_out_out_list.append(r_out_out)
fig.tight_layout()
```

```{code-cell} ipython3
plt.figure(figsize=(16,8))
plt.plot(edge_count,r_in_in_list,'bo--',label="r(in,in) degree assortativity coefficient",markersize=10)
plt.plot(edge_count,r_in_out_list,'go--',label="r(in,out) degree assortativity coefficient",markersize=10)
plt.plot(edge_count,r_out_in_list,'yo--',label="r(out,in) degree assortativity coefficient",markersize=10)
plt.plot(edge_count,r_out_out_list,'ro--',label="r(out,out) degree assortativity coefficient",markersize=10)
plt.xlabel("Number of edges",fontsize=14)
plt.ylabel("Degree assortativity measure",fontsize=14)
plt.legend(fontsize=12)
plt.show()
```

```{code-cell} ipython3
g = copy.deepcopy(G)
edge_list = list(nx.complement(g).edges())
random.shuffle(edge_list)
add_new_edges(5)


weight_list = [None,'weight']
labels_list = [{str(i):str(i) for i in range(G.number_of_nodes())},nx.get_node_attributes(G,'weight')]
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

for w, l, ax in zip(weight_list, labels_list, axes.ravel()):
    nx.draw(g, pos=pos, ax=ax, node_size=350, width=0.5,with_labels = True, labels=l,font_size=15,node_color='w')

    r_in_in = nx.degree_assortativity_coefficient(g,x='in',y='in',weight=w)
    r_in_out = nx.degree_assortativity_coefficient(g,x='in',y='out',weight=w)
    r_out_in = nx.degree_assortativity_coefficient(g,x='out',y='in',weight=w)
    r_out_out = nx.degree_assortativity_coefficient(g,x='out',y='out',weight=w)

    ax.set_title(f"r(in,in) = {r_in_in:.3}    r(in,out) = {r_in_out:.3}\nr(out,in) = {r_out_in:.3}    r(out,out) = {r_out_out:.3}", size=15)

fig.tight_layout()
```

[^1] M. E. J. Newman, Mixing patterns in networks https://doi.org/10.1103/PhysRevE.67.026126

[^2] Foster, J.G., Foster, D.V., Grassberger, P. & Paczuski, M. Edge direction and the structure of networks https://doi.org/10.1073/pnas.0912671107
