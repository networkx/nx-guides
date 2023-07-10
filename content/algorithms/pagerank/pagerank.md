---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
# this function to be added to networkx

def my_draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=10,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    rotate=True,
    clip_on=True,
    rad=0
):
    """Draw edge labels.

    Parameters
    ----------
    G : graph
        A networkx graph

    pos : dictionary
        A dictionary with nodes as keys and positions as values.
        Positions should be sequences of length 2.

    edge_labels : dictionary (default={})
        Edge labels in a dictionary of labels keyed by edge two-tuple.
        Only labels for the keys in the dictionary are drawn.

    label_pos : float (default=0.5)
        Position of edge label along edge (0=head, 0.5=center, 1=tail)

    font_size : int (default=10)
        Font size for text labels

    font_color : string (default='k' black)
        Font color string

    font_weight : string (default='normal')
        Font weight

    font_family : string (default='sans-serif')
        Font family

    alpha : float or None (default=None)
        The text transparency

    bbox : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for edge labels.
        Default is {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}.

    horizontalalignment : string (default='center')
        Horizontal alignment {'center', 'right', 'left'}

    verticalalignment : string (default='center')
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

    ax : Matplotlib Axes object, optional
        Draw the graph in the specified Matplotlib axes.

    rotate : bool (deafult=True)
        Rotate edge labels to lie parallel to edges

    clip_on : bool (default=True)
        Turn on clipping of edge labels at axis boundaries

    Returns
    -------
    dict
        `dict` of labels keyed by edge

    Examples
    --------
    >>> G = nx.dodecahedral_graph()
    >>> edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw
    draw_networkx
    draw_networkx_nodes
    draw_networkx_edges
    draw_networkx_labels
    """
    import matplotlib.pyplot as plt
    import numpy as np

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5*pos_1 + 0.5*pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0,1), (-1,0)])
        ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
        ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
        ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
        bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items
```

## PageRank: Quantifying Node Importance in Networks

+++

In this tutorial, we will explore the PageRank algorithm implemented in NetworkX under [algorithms/link_analysis/pagerank_alg.py](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html). We will focus on the mathematical model behind the PageRank algorithm.

+++

### Introduction to PageRank

PageRank is a link-analysis algorithm that assigns a numerical weight to each node in a network with the purpose of measuring its relative importance within the node set.

While the approach behind the PageRank algorithm has been exploited since the late 1800s, its creation is attributed to Larry Page and Sergey Brin in 1998. PageRank went on to become the foundation of the Google Search engine and revolutionized web search.

Consider the World Wide Web as a network of webpages where the hyperlinks act as edges. PageRank works by determining the number and quality of links to a webpage to compute a rough estimate of how important it is. The underlying assumption is that more important pages are likely to receive more links from other pages.

```{code-cell} ipython3
# imports
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
# run pagerank algorithm on a small graph
G = nx.karate_club_graph()
pagerank_dict = nx.pagerank(G)
```

```{code-cell} ipython3
# plot the graph such that node size is proportional to the pagerank value of node
nsize = [x*25000 for x in pagerank_dict.values()]
plt.figure(figsize=(10,10))
pos=nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, node_size=nsize, node_color='yellow')
plt.show()
```

From the plot above, we observe that the node size (which is proportional to the pagerank of the node) is proportional to the number of edges connected to the node. 

+++

### Markov Chains

+++

Markov chains are mathematical models that represent systems that evolve over time in a probabilistic manner. These systems consist of a set of states, and transitions between these states occur randomly based on specific probabilities. There are a finite number of states and time moves forward in steps (discrete time).

The key characteristic of Markov chains is that the probability of transitioning from one state to another depends solely on the current state and is independent of the past states. This is also called the <i>memoryless</i> property of Markov chains. 

Markov chains can be used to model the web network, particularly in the context of the PageRank algorithm. The algorithm models web traffic as a random walk with equal chance of moving across each outgoing link of each webpage. The concept of <i>random walks</i> will be discussed further in the tutorial.

In this context, individual web pages are represented as states, and going from one state to another involves transition probabilities. This transition probability is determined by the number and quality of incoming links to that page. Pages with more incoming links are considered to have a higher probability of being visited.


It is important to highlight at this point that we deal with two types of probabilities while modelling Markov chains - one is the transition probability between states and the other is the probability distribution over states. Transition probability is the probability of moving from one state to another and remains constant over time. Whereas, the probability distribution over states signifies probability of being in each state at every time step. It changes as time progresses and eventually stabilises (called stationary distribution, which will be further discussed in detail).

```{code-cell} ipython3
# generate a random Markov Chain with transition probabilities
H = nx.fast_gnp_random_graph(4, 0.8, seed=237, directed=True)
pos=nx.kamada_kawai_layout(H)
nx.draw_kamada_kawai(H, with_labels=True, connectionstyle='arc3, rad = 0.15', node_size=1500, node_color="yellow")
outdeg_dict = dict(H.out_degree)
transition_probabilities = {}
for (x, y) in H.edges:
    transition_probabilities[(x, y)] = round(1/outdeg_dict[x], 2)
edge_labels = my_draw_networkx_edge_labels(H, pos, edge_labels=transition_probabilities, rotate=False, rad = 0.15)
```

In the above plot, we model a simple Markov chain with 4 states. The transition probability is simply based on the incoming links to a state. It is assumed that the user is equally likely to transition to any of the states linked to a state i.e. if a state has 3 outgoing links, the transition probability of each of those will be 0.33.

Transition probability of going from state 1 to state 2 can be represented as $ P(1, 2) = 0.5 $.

```{code-cell} ipython3
P = np.zeros((4, 4))
P = np.array([[transition_probabilities.get((i, j), 0) for j in range(4)] for i in range(4)])
df = pd.DataFrame(P, columns=[i for i in range (4)], index=[i for i in range (4)])
df
```

To represent the transition probabilities, a transition matrix is constructed as shown above. It is a square matrix with its rows and columns corresponding to the states (web pages). Entry $ P_{i j} $ in matrix represents the transition probability of going from state $i$ to state $j$.

The fundamental components of a Markov chain are the set of states, transition probabilities, and an initial state distribution. 

We have already discussed states and transition probabilities. We will discuss initial distribution after Random Walk model for better understanding.

+++

A <b><i>random walk model</b></i> is employed on this Markov Chain to simulate the behavior of a web surfer navigating through the web network. This random walk represents the movement of the surfer as they visit different web pages by following the hyperlinks present on each page. It is assumed that at each step, the surfer randomly selects an outgoing link from the current web page and moves to the next page. The choice of the next page is governed by the transition probabilities.

+++

In the context of Markov chains, the initial distribution represents the probability distribution of the surfer's starting location or web page when the random walk begins. It signifies the initial conditions of the system before any transitions occur and influences the subsequent transitions in the random walk model simulated on the Markov chain.

The initial distribution is typically represented as a probability vector $\pi_{0}$, where each element $\pi_{0}(v)$ corresponds to the probability of being in state $v$ in the Markov chain.

At any step $n$, the probability distribution can be represented as - 

$\pi_{n} = [~ \pi_{n}(0) ~~~~ \pi_{n}(1) ~~~~ \pi_{n}(2) ~~~~ \pi_{n}(3) ~~ ... ]$

Where $\pi_{0}(v)$ represents the probability of being in state $v$ at step n.

The sum of all elements in $\pi_{n}$ always equals 1, as it represents a probability distribution.

This probability distribution across states changes at each step according to the following formula - 

$\pi_{n+1} = \pi_{n}.P$

Here, $P$ is the state transition matrix.

+++

Now that we know how to mathematically model a Markov chain and its transitions, an important question arises.

+++

<b> How do we measure the relative importance of states in a Markov Chain? </b> <i> Answer is Stationary Distributions.</i>

+++

### Stationary Distributions

+++

In a Markov chain, a stationary distribution represents the long-term behavior of the system. It is a probability distribution that remains unchanged after transitions within the Markov chain. The stationary distribution is reached when the Markov chain reaches a steady state, where the probabilities of transitioning between different web pages no longer change significantly. 

In the context of the PageRank algorithm, the stationary distribution corresponds to the importance or rank assigned to each web page. This distribution provides a measure of the relative importance of each web page, as it represents the probability of a random surfer visiting each page in the long run.

Considering the Markov chain we plotted above, let's compute the probability distribution across states over time. The initial probability distribution across states is taken as uniform. At each step we perform the operation $\pi_{n+1} = \pi_{n}.P$

```{code-cell} ipython3
probability_distribution = np.full(4, 0.25)
for i in range(25):
    print("Step", i, ": ", probability_distribution)
    probability_distribution = np.dot(probability_distribution, P)
```

It is observed that towards the end of iterations, the probability distribution is reaching a steady state i.e. the stationary distribution.

This brute-force method of computing stationary distributions by performing the operation $\pi_{n+1} = \pi_{n}.P$ at every step is called the Power Iteration method. We continue the iterations till the difference between $\pi_{n+1}$ and $\pi_{n}$ becomes less than the tolerance threshold value.

There exist algebraic methods that can compute stationary distributions in a more direct manner. But practical experiments on large web networks have found that the brute-force method has the best performance  because most web networks have relatively fast convergence times (~50 iterations to reach a reasonable tolerance threshold).

+++

### Existence of Stationary Distributions

+++

<i>Do all Markov chains converge to a Stationary distribution?</i>

To answer this question, let us look at two examples.

```{code-cell} ipython3
I = nx.MultiDiGraph()
I.add_edges_from([(1, 1), (0, 0)])

plt.figure(figsize=(4,2))

pos={0:(1, 1), 1:(2, 1)}
nx.draw(I, pos, with_labels=True, node_size=1000, node_color="yellow", connectionstyle='arc3, rad = 0.1')
el = nx.draw_networkx_edge_labels(I, pos, edge_labels={(1, 1):1.0, (0, 0):1.0})
plt.title("G1", y=-0.2)
plt.show()
```

Both states in above Markov chain have only one incoming link that too from itself. Thus, it contains isolated subsets of states that cannot be reached from the rest of the chain. This is called a <b><i>reducible</i></b> Markov chain 

Here the transition probability matrix is an identity matrix because of which every initial distribution becomes a stationary distribution.

```{code-cell} ipython3
J = nx.DiGraph()
J.add_edges_from([(0, 1), (1, 0)])

plt.figure(figsize=(4,2))

pos={0:(1, 1), 1:(2, 1)}
nx.draw(J, pos, with_labels=True, node_size=1000, node_color="yellow", connectionstyle='arc3, rad = 0.2')
edge_labels = my_draw_networkx_edge_labels(J, pos, edge_labels={(0, 1):1.0, (1, 0):1.0}, rotate=False, rad = 0.2)

plt.title("G2", y=-0.1)
plt.show()
```

In the above Markov chain, when we apply transitions, the distribution never converges and only oscillates. This is called a <b><i>periodic</i></b> Markov chain.

Periodic Markov chains are characterized by having subsets of states that form closed loops or cycle, where transitions within the cycle are more probable than transitions between cycles. These loops introduce a regularity in the chain's behavior, causing the system to exhibit repetitive patterns as it evolves over time.

A periodic Markoc chain does not converge to a stationary distribution.

+++

Thus, we can conclude that for a Markov chain to have a unique stationary distribution, it must satisfy two conditions:

<b>Reducibility (Uniqueness problem):</b> For a unique stationary distribution $\pi$ to exist, the Markov chain must not be reducible. The Markov chain must be irreducible i.e it is possible to reach any state from any other state, either in a single step or over multiple steps.

<b>Periodicity (Convergence problem):</b> For all initial distributions $\pi_{0}$ to converge to $\pi$, the Markov chain must not be periodic. The Markov chain must be aperiodic i.e. when we apply transitions, the distribution across states should not oscillate but converge after sufficient time.

When a Markov chain is both irreducible and aperiodic, it is guaranteed to have a unique stationary distribution. This distribution represents the long-term behavior of the system, where the probabilities of being in each state stabilize and remain constant over time.

+++

### PageRank Algorithm

The Pagerank algorithm is fundamentally based on the principle of computing Stationary Distributions of Markov chains. Our methods for computing stationary distributions rely on the assumption that the web network is a reducible and aperiodic Markov chain. However it may not always be true in reality.

There maybe webpages that have no outgoing links, so all users will be absorbed into this state after some transitions (these are called sink states). There maybe two or more webpages linked to each other such that once a user enters, they get stuck in a never ending cycle and all users eventually end up cycling between these two states.

<i> So, how do we handle Markov chains that don't satisfy the required conditions?</i>

At every step, we transition to a random state with the probability $\frac{1-\alpha}{N}$ where $N = $ Number of states and we can pick any value for $\alpha$.

But it is not sufficient to just add these random transition probabilities because it breaks the assumption of a probability distribution of across states since the distribution no longer sums to one. To solve this problem, we use the damping factor $\alpha$. We first reduce the original transition probability by $\alpha$ and then add the random state transition probability of $\frac{1-\alpha}{N}$.

```{code-cell} ipython3
H2 = nx.complete_graph(4, create_using=nx.MultiDiGraph())
H2.add_edges_from([(0, 0), (1, 1), (2, 2), (3, 3)])
pos=nx.kamada_kawai_layout(H2)
nx.draw_kamada_kawai(H2, with_labels=True, connectionstyle='arc3, rad = 0.15', node_size=1500, node_color="yellow")
outdeg_dict = dict(H.out_degree)
transition_probabilities = {}
for x in range(4):
    for y in range(4):
        temp = 0
        if((x, y) in H.edges):
            temp += 1/outdeg_dict[x]
        transition_probabilities[(x, y)] = round(temp+0.1, 2)
edge_labels = my_draw_networkx_edge_labels(H2, pos, edge_labels=transition_probabilities, rotate=False, rad = 0.15)
```

```{code-cell} ipython3
H2 = nx.complete_graph(4, create_using=nx.MultiDiGraph())
H2.add_edges_from([(0, 0), (1, 1), (2, 2), (3, 3)])
pos=nx.kamada_kawai_layout(H2)
nx.draw_kamada_kawai(H2, with_labels=True, connectionstyle='arc3, rad = 0.15', node_size=1500, node_color="yellow")
outdeg_dict = dict(H.out_degree)
alpha = 0.6
transition_probabilities = {}
for x in range(4):
    for y in range(4):
        temp = 0
        if((x, y) in H.edges):
            temp += 1/outdeg_dict[x]
            temp *= alpha
        transition_probabilities[(x, y)] = round(temp+((1-alpha)/4), 2)
edge_labels = my_draw_networkx_edge_labels(H2, pos, edge_labels=transition_probabilities, rotate=False, rad = 0.15)
```

This prevents any state from permanently becoming an absorbing state amd also prevents users from being stuck in a cycle.

Thus, PageRank computes a modified probability distribution that satisfies the Ergodic theorem from the initial distribution as follows - 
<br></br>
<center>$\hat{P} = (\alpha*P) + (\frac{1-\alpha}{N}*\mathbf{1}_{N\times N})$</center>

Where, 
- $\hat{P}$ is the modified probability distribution (also called the Google matrix)
- $\alpha$ is the damping factor
- $\mathbf{1}_{N\times N}$ is an NxN matrix of all ones
- The term $(\frac{1-\alpha}{N}*\mathbf{1}_{N\times N})$ simulates the idea of picking any random state as the next state during transition.

```{code-cell} ipython3
nx.google_matrix(H, alpha=0.6)
```

### Personalization in PageRank

Personalized PageRank is an extension of the traditional PageRank algorithm that incorporates personalization preferences to influence the ranking of nodes in a network. In the standard PageRank algorithm, the ranking of nodes is primarily determined by the network structure, where nodes with many incoming links tend to receive higher rankings. However, personalized PageRank enables us to introduce a bias or preference towards specific nodes, regardless of their link structure.

Personalized PageRank is particularly important in web networks due to its ability to provide personalized and context-aware recommendations, improve search relevance, and enhance user experience.

In NetworkX, the pagerank function provides an option to specify the personalization vector. The personalization vector is a dictionary where each node in the network is assigned a personalized score. By default, the personalization vector assigns equal importance to all nodes, resulting in a standard PageRank calculation. However, by assigning different scores to specific nodes, we can influence the ranking outcomes.

+++

## References

1. https://www.cse.iitb.ac.in/~soumen/readings/papers/PageBMW1998pagerank.pdf (Original PageRank paper)
2. https://brilliant.org/wiki/markov-chains/#markov-chain
3. https://brilliant.org/wiki/stationary-distributions/
4. https://www.youtube.com/watch?v=JGQe4kiPnrU 
5. https://www2.math.upenn.edu/~kazdan/312F12/JJ/MarkovChains/markov_google.pdf 
6. https://www.youtube.com/watch?v=URaS1u-Murc
