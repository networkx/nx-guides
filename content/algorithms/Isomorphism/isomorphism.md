---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# **Isomorphism**

```{code-cell} ipython3
import networkx as nx
import matplotlib.pyplot as plt
```

## What's isomorphism? Why is it interesting?

+++

As unlabeled graphs can have multiple spatial representations, two graphs are isomorphic if they have the same number of edges, vertices, and same edges connectivity. Let's see an example of two isomorphic graphs, 

```{code-cell} ipython3
plt.subplot(221)
G = nx.Graph([(0, 1), (0, 4), (0,2), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (5, 7), (6, 7), (6, 4)])
nx.draw_spring(G, with_labels = True, node_color = "c")
plt.title("G", fontweight="bold")
H = nx.Graph([(1, 2), (1, 5), (1,3), (2, 4), (2, 6), (3, 4), (3, 7), (4, 8), (5, 6), (6, 8), (7, 8), (7, 5)])
plt.subplot(222)
nx.draw_circular(H, with_labels = True, node_color = "yellow")
plt.title("H", fontweight="bold")

plt.show()
```

These graphs' spatial representations are very different yet they are isomorphic.  

+++

### **Formal definition**

+++

G and H are isomorphic if we can establish a bijection between the vertex sets of G and H. 

$${\displaystyle f\colon V(G)\to V(H)}$$
such as if $$ $$

<center> $v$  and $ w $ are  adjacent  in G $\iff$ $f(v)$ and $f(w)$ are adjacent in H </center>

+++

To formally prove that 2 graphs are isomorphic we need to find the bijection between the vertex set. For the previous example that would be: 

$$f(i) = i+1 \hspace{0.5cm} \forall i \in [0, 7]$$ 

+++

For small examples, isomorphism may seem easy. But it isn't a simple problem. For two graphs G and H of n nodes, there are n! bijections function possible. Checking every combination is not a feasible option for bigger graphs. 
In fact, isomorphism is part of the problems known as NP. This means that we don't know any algorithm that runs in polynomial time.

+++

### Applications (TODO: Should I move this to the end?)

Ideas:
- Test if 2 electronic chips are the same
- Image recognition
- Research: computer and information system, chemistry, social media, images, protein structure

+++

## Isomorphism Algorithms
**Naive Approach**

+++

There are some initial properties that we can check to decide whether it's possible to have an isomorphism
- G and H have the same amount of nodes and edges 
- The degree sequence for G and H are the same

These are necessary conditions but don't guarantee that 2 graphs are isomorphic. Let's see a small example:

```{code-cell} ipython3
plt.subplot(221)
G = nx.cycle_graph(6)
nx.draw_circular(G)
plt.title("G", fontweight="bold")
plt.subplot(222)
H = nx.union(nx.cycle_graph(3), nx.cycle_graph(3), rename = ("s","d"))
nx.draw_circular(H, node_color = "r")
plt.title("H", fontweight="bold")
plt.show()
```

```{code-cell} ipython3
nx.faster_could_be_isomorphic(G, D)
```

These graphs are clearly not isomorphic but they have the same degree secuence. 

+++

Another property we can check for is: 
- Same number of cycles of a particular length, for example, triangles. 

```{code-cell} ipython3
nx.fast_could_be_isomorphic(G, D)
```

Checking this new property we can detect that the previous example graphs were not isomorphic. 

We can go one step further and check the number of cliques. 

```{code-cell} ipython3
nx.could_be_isomorphic(G, D)
```

Again we can detect that G and D are not isomorphic. But these conditions are not enough to say that 2 graphs are isomorphic. Let's look at the following example: 

```{code-cell} ipython3
plt.subplot(221)
G = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1), (2,4)])
nx.draw_circular(G, with_labels = True, node_color="g")
plt.title("G", fontweight="bold")

plt.subplot(222)
H = nx.Graph([(1, 2), (2, 3), (3, 4), (2,4), (3, 1)])
nx.draw_circular(H, with_labels = True, node_color = "c")
plt.title("H", fontweight="bold")
plt.show()
```

```{code-cell} ipython3
nx.could_be_isomorphic(G1, G2)
```

These graphs meet all the necessary conditions but they're not isomorphic.

+++

### TODO: add classes of graphs with solution in polynomial time

+++

**Advanced Algorithms**

+++

**vf2**

```{code-cell} ipython3

```

## Todo: State of the art 

+++

# Sources (TODO: check formatting)
- Graph Theory and Its applications
- https://www.ijcaonline.org/archives/volume162/number7/somkunwar-2017-ijca-913414.pdf
