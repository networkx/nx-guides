---
jupytext:
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# To be or not to be (isomorphic)

```{code-cell}
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
```

The graph isomorphism problem is a very interesting topic with many applications
spanning graph theory and network science --- check out {doc}`isomorphism` for
a deeper introduction!

Determining whether two graphs `G` and `H` are isomorphic essentially boils
down to finding a valid isomorphic mapping between the nodes in `G` and `H`,
respectively.
The process of finding such a mapping can be quite expensive:

```{code-cell}
G = nx.complete_graph(100)
H = nx.relabel_nodes(G, {n: 10 * n for n in G})
```

We know `G` and `H` are isomorphic a priori, since `H` is just a copy of `G` with
relabeled nodes.
Of course, we can verify this:

```{code-cell}
nx.is_isomorphic(G, H)
```

and do some basic timing to get a sense of how long it takes to make this
determination:

```{code-cell}
%timeit nx.is_isomorphic(G, H)
```

Not too bad, at least for these relatively small simple graphs - but absolute
timing values aren't particularly enlightening.
How does this compare with a very similar example where the graphs are *not*
isomorphic?

```{code-cell}
H_ni = G.copy()
H_ni.remove_edge(27, 72)  # Remove a single arbitrary edge
```

Again, we know a priori that `G` and `H_ni` are not isomorphic:

```{code-cell}
nx.is_isomorphic(G, H_ni)
```

but even though all we've done is remove a single arbitrary edge from `H`, the
isomorphism determination is several orders of magnitude faster!

```{code-cell}
%timeit nx.is_isomorphic(G, H_ni)
```

Quantitatively:

```{code-cell}
import timeit

iso_timing, non_iso_timing = (
    timeit.timeit(f"nx.is_isomorphic(G, {G2})", number=20, globals=globals())
    for G2 in ("H", "H_ni")
)
print(f"Relative compute time, iso/non_iso example: {iso_timing/non_iso_timing:.2f}")
```
