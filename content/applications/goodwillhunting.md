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
[Definitions][tree_wiki_defn].

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
    G, "pos", {0: (0, 2), 1: (1, 1), 2: (0, 0), 3: (2, 1), 4: (3, 2), 5: (3, 0)}
)

H = nx.Graph([(6, 5), (5, 4), (5, 3), (3, 2), (3, 1)])
nx.set_node_attributes(
    H, "pos", {6: (2, 0), 5: (1, 0), 4: (0, 0), 3: (1, 1), 2: (1, 2), 1: (1, 0)}
)
```

```{code-cell}
fig, (left, right) = plt.subplots(1, 2)
nx.display(G, ax=left)
nx.display(H, ax=right)
```
