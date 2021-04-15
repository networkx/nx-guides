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

# Four Grids

```{code-cell} ipython3
%matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
G = nx.grid_2d_graph(4,4)  #4x4 grid
```

```{code-cell} ipython3
pos = nx.spring_layout(G, iterations=100)
```

```{code-cell} ipython3
nx.draw(G, pos, font_size=8)
```

```{code-cell} ipython3
nx.draw(G, pos, node_color='k', node_size=250, with_labels=False)
```

```{code-cell} ipython3
nx.draw(G, pos, node_color='g', node_size=250, with_labels=False, width=6)
```

```{code-cell} ipython3
H = G.to_directed()
nx.draw(H, pos, node_color='b', node_size=250, with_labels=False)
```
