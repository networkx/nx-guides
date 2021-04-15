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

# Ego Graph

```{code-cell} ipython3
from operator import itemgetter
import networkx as nx
```

```{code-cell} ipython3
import matplotlib.pyplot as plt
%matplotlib inline
```

```{code-cell} ipython3
G = nx.generators.barabasi_albert_graph(1000, 2)
```

```{code-cell} ipython3
node_and_degree = dict(G.degree())
```

```{code-cell} ipython3
largest_hub, degree = sorted(node_and_degree.items(), key=itemgetter(1))[-1]
```

```{code-cell} ipython3
hub_ego = nx.ego_graph(G, largest_hub)
```

```{code-cell} ipython3
pos = nx.spring_layout(hub_ego)
```

```{code-cell} ipython3
nx.draw(hub_ego,pos,node_color='b', node_size=50, with_labels=False)
nx.draw_networkx_nodes(hub_ego, pos, nodelist=[largest_hub], node_size=300, node_color='r')
plt.show()
```
