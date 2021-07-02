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
  version: 3.9.2
---

# Directed Acyclic Graphs

In this tutorial, we'll explore the algorithms related to directed acyclic graph
(or a "dag" as it is sometimes called) implemented in networkx under `networkx/algorithms/dag.py`.

#### Example

**TODO: Create Professor Bumstead clothing graph**

#### Definition

Directed acyclic graph ("DAG" or "dag") is a directed graph with no directed cycles.
That is, it consists of vertices and edges (also called arcs), with each edge directed from one vertex to another,
such that following those directions will never form a closed loop.
A directed graph is a DAG if and only if it can be topologically ordered,
by arranging the vertices as a linear ordering that is consistent with all edge directions.

## Topological sort

### Applications

The canonical application of topological sorting is in scheduling a sequence of jobs
or tasks based on their dependencies.
The jobs are represented by vertices, and there is an edge from $u$ to $v$
if job $u$ must be completed before job $v$ can be started
(for example, when washing clothes, the washing machine must finish before we put the clothes in the dryer).
Then, a topological sort gives an order in which to perform the jobs.

A closely related application of topological sorting algorithms
was first studied in the early 1960s in the context of the PERT technique for scheduling in project management.
In this application, the vertices of a graph represent the milestones of a project,
and the edges represent tasks that must be performed between one milestone and another.
Topological sorting forms the basis of linear-time algorithms for finding
the critical path of the project, a sequence of milestones and tasks that controls
the length of the overall project schedule.

In computer science, applications of this type arise in instruction scheduling,
ordering of formula cell evaluation when recomputing formula values in spreadsheets,
logic synthesis, determining the order of compilation tasks to perform in makefiles,
data serialization, and resolving symbol dependencies in linkers.
It is also used to decide in which order to load tables with foreign keys in databases.

#### Definition

A topological sort of a directed acyclic graph $G = (V, E)$ is a linear ordering of all its vertices
such that if $G$ contains an edge $(u, v)$, then $u$ appears before $v$ in the ordering.

It is worth noting that if the graph contains a cycle, then no linear ordering is possible.

It is useful to view a topological sort of a graph as an ordering of its vertices
along a horizontal line so that all directed edges go from left to right.

#### Asymptotics

The usual algorithms for topological sorting have running time linear
in the number of nodes plus the number of edges, asymptotically,
$\mathcal{O}(|V| + |E|)$.

### Kahn's algorithm

#### Example

**TODO: add example of usage `topological_sort(G)` function**

#### Definition

First, find a list of "start nodes" which have no incoming edges and insert them into a set S;
at least one such node must exist in a non-empty acyclic graph. Then:

```
L <- Empty list that will contain the sorted elements
S <- Set of all nodes with no incoming edge

while S is not empty do
    remove a node n from S
    add n to L
    for each node m with an edge e from n to m do
        remove edge e from the graph
        if m has no other incoming edges then
            insert m into S

if graph has edges then
    return error   (graph has at least one cycle)
else 
    return L   (a topologically sorted order)
```

### Depth-first search based algorithm

#### Example

**TODO: create topological sort function using depth-first search**\
**TODO: add an example of using this function**

#### Definition

The algorithm loops through each node of the graph, in an arbitrary order,
initiating a depth-first search that terminates when it hits any node that has already been visited
since the beginning of the topological sort or the node has no outgoing edges (i.e. a leaf node):

```
L <- Empty list that will contain the sorted nodes

while exists nodes without a permanent mark do
    select an unmarked node n
    visit(n)

function visit(node n)
    if n has a permanent mark then
        return
    if n has a temporary mark then
        stop   (not a DAG)

    mark n with a temporary mark

    for each node m with an edge from n to m do
        visit(m)

    remove temporary mark from n
    mark n with a permanent mark
    add n to head of L
```