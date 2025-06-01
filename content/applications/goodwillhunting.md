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

# The Good Will Hunting Problem

If you've seen the film [Good Will Hunting][gwh_wiki], you may recall a scene
in the beginning of the film where Fields medal-winning MIT professor Gerald Lambeau
(played by Stellan Skarsgård) presents a mathematics challenge to a classrom
full of students.
It turns out that the problem involves some basic graph theory... let's see if
we can't attack it ourselves with NetworkX!

## The problem statement

The excellent [Numberphile YouTube channel](https://www.youtube.com/@numberphile)
did a very nice video on this topic.

```{warning}
Make sure to pause at **3:05** if you don't want to give away the answer!
```

<iframe 
  width="560" 
  height="315"
  src="https://www.youtube.com/embed/iW_LkYiuTKE?si=zgyO8Pnn6eqid30P"
  title="YouTube video player"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen>
</iframe>

[gwh_wiki]: https://en.wikipedia.org/wiki/Good_Will_Hunting

Here is the problem statement, quoting James in the Numberphile video linked
above (starting at around `1:23`):

> Draw all homeomorphically irreducible trees of size n=10

As in the video, let's examine these terms more closely to make sure we can
understand the problem.

The first term to focus on ["tree"][tree_wiki], a fundamental concept in
graph theory.
A tree refers to an undirected graph which is fully connected and contains no
cycles.
We are also given the "size" of the tree in the problem statement, i.e. the
number of nodes that the tree contains.

[tree_wiki]: https://en.wikipedia.org/wiki/Tree_(graph_theory)

Given these simple definitions, we can already start coming up with example
graphs that might fit the bill.
For example, a path graph with 10 nodes is connected and contains no cycles,
and is therefore a tree!

```{code-cell}
G = nx.path_graph(10)
nx.is_tree(G)
```

Wow, that was easy... did we really find our first example that quickly?
Not so fast... there's still that whole business of "homeomorphic irreducibility".
Fortunately, at least in the context of this problem, this complicated terminology
describes a relatively simple concept:

    A tree is homeomorphically irreducible if it contains no nodes with degree
    2.

This simple interpretation can be found explicitly near the end of the
[Definitions section of the wiki article on trees][tree_wiki_defn].

[tree_wiki_defn]: https://en.wikipedia.org/wiki/Tree_(graph_theory)#Definitions

This added condition means that our path graph isn't a valid solution after all,
as it contains at least one node (8, in fact) with degree 2:

```{code-cell}
dict(G.degree)
```

So, let's restate the problem in these less-specialized terms:

We're looking for all undirected graphs that:
 - Contain 10 nodes
 - Are fully connected
 - Contain no cycles
 - Contain no nodes with degree 2

There's one final consideration which isn't explicitly mentioned in the problem
statement.
How do we determine whether or not a graph is "unique"?

This is briefly touched on in the Numberphile video. Consider two graphs:

```{code-cell}
# The reason for explicit positioning will become clear in a moment

G = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)])
nx.set_node_attributes(
    G, {0: (0, 2), 1: (1, 1), 2: (0, 0), 3: (2, 1), 4: (3, 2), 5: (3, 0)}, "pos"
)

H = nx.Graph([(6, 5), (5, 4), (5, 3), (3, 2), (3, 1)])
nx.set_node_attributes(
    H, {6: (0, 2), 5: (0, 1), 4: (0, 0), 3: (1, 1), 2: (1, 2), 1: (1, 0)}, "pos"
)
nx.set_node_attributes(H, values="tab:red", name="color")
```

```{code-cell}
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

for graph, axis in zip((G, H), ax):
    nx.display(graph, canvas=axis)
    axis.set_axis_off()
```

At face value, it's clear these graphs are not identical.
For starters, the numbers representing the nodes are different.
Then there's the properties of the nodes in the two graphs, e.g. the node
color or their position in the 2D visualization. 
Let's think about these differences in the context of our problem.
If we consider the node properties significant, then our question could have
infinite answers: all we'd need to do is find one such tree, then change the
coloring, positioning, or any other unbounded property of the nodes to get a
"new" answer.
For our purposes then, we want to ignore node properties.

Similarly, there are the node labels - i.e. the values assigned 
If we allow these labels to do be anything (i.e. integers, letters, etc.)
then we have the same situation as the node properties: there is an infinite
number of ways to label the nodes.
We reject this as uninteresting for our question.
Even if we were to limit the set of possible labels (say the integers from `[0, 9]`
for our `n=10` case), then we'd still have a scenario where graphs with the same
adjacency can be represented multiple ways depending on the permutations of node
labels.
For our purposes then, we'll also be ignoring the node labels.
In the parlance of graph theory, this means we're dealing with *unlabelled trees*.

What's left then is a comparison of the adjacencies between the two graphs.
In the context of our problem, when we say "unique" graphs what we mean are
graphs that are *nonisomorphic*.

```{code-cell}
nx.is_isomorphic(G, H)
```

You can learn more about isomorphism in the {ref}`other NX guides <isomorphism>`.

### Problem statement summary

With that final clarification, we've fully specified the problem.
We're looking for all undirected graphs that:
 - Contain 10 nodes
 - Are fully connected
 - Contain no cycles
 - Contain no nodes with degree 2
 - Are nonisomorphic with each other

## Attacking the problem

How many of these trees exist for `n=10`?
As noted in the video, there are 10 homeomorphically irreducible unlabeled trees
with 10 nodes.
We can confirm this by checking the corresponding sequence in the [OEIS](oeis.org):
[The number of series-reduced trees with n nodes][a000014].

[a000014]: https://oeis.org/A000014

### Qualitative approach

We began our investigation with a `path_graph`, which is a tree but doesn't meet
the criterion for irreducibility.
Are there any simple modifications we can think of from this starting point to
arrive at an irreducible tree?
The main issue is all of those interconnected degree-2 nodes: how could we replace
that pattern?

One common way to think about trees is as a *hierarchical* structure, with
"root" nodes and "leaf" nodes.
Perhaps this line of thinking could help here.
What if we organized our 10 nodes so that we had one "root" with the remaining
nodes as leaves?

```{code-cell}
G = nx.Graph()
G.add_node(0)  # our "root" node

# Then, let's add each of the remaining 9 nodes as leaves connected only to
# the root
G.add_edges_from((0, n) for n in range(1, 10))

fig, ax = plt.subplots()
# Position nodes hierarchically, with "root" on one end and "leaves" on the other
pos = nx.bfs_layout(G, 0)

nx.draw(G, pos=pos, ax=ax)
```

This looks promising... our graph `G` is a tree:

```{code-cell}
nx.is_tree(G)
```

with 10 nodes:

```{code-cell}
len(G)
```

and, unlike the `path_graph`, doesn't contain any nodes with degree 2:

```{code-cell}
not any(d == 2 for _, d in G.degree())
```

It looks like we've found our first example!

### Another perspective

We arrived at this example by thinking in terms of "roots" and "leaves", but if
we change our perspective a bit, we might recognize this as an instance of a
common class of graphs.

Let's try a different layout; perhaps one that tries to evenly spread nodes
spatial rather than capture hierarchical relationships:

```{code-cell}
# A force-directed layout
pos = nx.spring_layout(G)

fig, ax = plt.subplots()
nx.draw(G, pos=pos, ax=ax)
```

That looks an awful lot like the {func}`~networkx.generators.classic.star_graph`.
And indeed it is!

```{code-cell}
nx.is_isomorphic(G, nx.star_graph(9))
```
