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

# Node Colormap

```{code-cell} ipython3
%matplotlib inline
import networkx as nx
import matplotlib as plt
```

```{code-cell} ipython3
G = nx.cycle_graph(24)
```

```{code-cell} ipython3
pos = nx.spring_layout(G,iterations=200)
```

```{code-cell} ipython3
nx.draw_networkx(G, pos, node_color=range(24), node_size=800, cmap=plt.cm.Blues)
```
