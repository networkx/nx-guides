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
  version: 3.7.4
---

# Degree Histogram

```{code-cell} ipython3
%matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
G = nx.gnp_random_graph(100, 0.02)
```

```{code-cell} ipython3
degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
```

```{code-cell} ipython3
dmax = max(degree_sequence)
```

```{code-cell} ipython3
Gcc = sorted((G.subgraph(c) for c in nx.connected_components(G)), key = len, reverse=True)[0]
```

```{code-cell} ipython3
pos = nx.spring_layout(Gcc)
```

```{code-cell} ipython3
nx.draw_networkx_nodes(Gcc, pos, node_size=20)
nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
plt.show()
```

```{code-cell} ipython3
plt.loglog(degree_sequence,'b-',marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.axes([0.45,0.45,0.45,0.45])
plt.axis('off')
plt.show()
```
