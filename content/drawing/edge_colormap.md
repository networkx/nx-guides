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

# Edge Colormap

```{code-cell} ipython3
%matplotlib inline
import networkx as nx
import matplotlib as plt
```

```{code-cell} ipython3
G = nx.star_graph(20)
```

```{code-cell} ipython3
pos = nx.spring_layout(G)
```

```{code-cell} ipython3
nx.draw_networkx(G, pos, node_color='#A0CBE2', edge_color=range(20), width=4, edge_cmap=plt.cm.Blues, with_labels=False)
```
