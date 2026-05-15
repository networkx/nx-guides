---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Networks in Epidemiology: Hantavirus

Networkx analysis is an essential part of epidemiology, particularly in the
study of disease transmission, surveillance, and outbreak investigation.
Many data from such studies naturally lend themselves to graphical representations.
For instance, *contact tracing* involves the tracking of potential interactions
between members of a population who may have been exposed to disease.
It is natural to represent such data as a graph where the nodes in the graph
represent individuals and the edges represent interactions (or potential interactions)
between them.
Another common formulation is the *transmission network*, where the edges in
the graph represent likely (or possible) transmissions of an infectious agent from one
individual to another.
Such networks are powerful tools to allow epidemiologists to study and ultimately
predict the dynamics of infectious agents within populations.

## Studying an outbreak of Andes Hantavirus

In this tutorial, we will use NetworkX to investigate and reproduce results from an
epidemiological study of an outbreak in the Andes virus (ANDV) hantavirus that
occurred in 2018-2019 entitled:

  “Super-Spreaders” and Person-to-Person Transmission of Andes Virus in Argentina

by Martínez, V. P. et. al.
The article is publicly available via the New England Journal of Medicine
[DOI: 10.1056/NEJMoa2009040][paper].

[paper]: https://www.nejm.org/doi/full/10.1056/NEJMoa2009040

The paper is packed with a ton of interesting information, but of particular
interest for us is the *transmission network* presented in Figure 1B:

```{figure} https://www.nejm.org/cms/10.1056/NEJMoa2009040/asset/af0da102-84a2-48bf-abec-b1660394b3ee/assets/images/large/nejmoa2009040_f1.jpg
:alt: Four-panel image summarizing study. Upper-right panel contains graphic of transmission network.
:align: center

Figure 1 from [the paper][paper]. Panel 1B presents the transmission network
that we recreate with NetworkX below.
```

Let's start by extracting the information from this figure into a NetworkX
graph!
For consistency, we'll use the same indexing scheme as the paper (i.e. the
initial patient will have index `1`).

```{code-cell}
import networkx as nx

G = nx.DiGraph()

# The initial infection of patients 2 through 6 (i.e. the top of the figure)
G.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)])

# On to the second row, starting with the transmission from patient 2
G.add_edges_from([(2, 9), (2, 12), (2, 13), (2, 11), (2, 7), (2, 8)])
# and the transmissions to patients 14 and 10
G.add_edge(5, 14)
G.add_edge(2, 10)  # In

```
