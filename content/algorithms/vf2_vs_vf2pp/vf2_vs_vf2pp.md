---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# VF2 vs VF2++: Comparative analysis of performance

+++

Currently, in NetworkX we have two isomorphism algorithms implemented: VF2 and VF2++.

VF2 and VF2++ are recursive algorithms that explore all the possible matching functions between the nodes of the graphs in order to find one that satisfies the isomorphism. As exploring all the matching functions has an exponential cost some cutting rules are used to avoid unfruitful branches.

**What's new on VF2++?**
- Node ordering: Previously the order in which the nodes were explored was determined by the labels. In this new algorithm, a particular node order is defined for every graph in order to explore the "rarest" nodes first. The "rarest" nodes are defined based on the graph structure.   
- Simple-to-check cutting rules. These new rules are cheaper than the old ones but are just as effective to determine if a branch is unfruitful.
- A non-recursive implementation that saves both time and space.

Let's see an example of how to use VF2 and VF2++ to test for isomorphism with NetworkX.

```{code-cell}
import networkx as nx

G = nx.bull_graph() #Create a bull graph

print("VF2:  ", nx.is_isomorphic(G, G))  # VF2

print("VF2++: ", nx.vf2pp_is_isomorphic(G, G))  # VF2++
```

## Analysis: General approach
To compare the performance of both algorithms we will run the algorithms over many different types of graphs and digraphs. The analysis will be divided as follows:

- Complete Graphs: Graphs and DiGraphs
- Regular Graphs
- Random Erdos Renyi Graphs and DiGraphs
- Random Graphs and DiGraphs with the same degree sequence
- Proteins Dataset

+++

To measure execution time we can use the function *timeit(setup, stmt, number )*. Where *stmt* is the code that we want to time, *setup* is the code needed to run stmt but that we don't want to time and *number* is how many times stmt is run.

Let's see an example:

```{code-cell}
import timeit

sleep_time = timeit.timeit(
    setup="import time",  # Setup code
    stmt="time.sleep(2)",  # Code to be timed
    number=1,
)  # Number of times my code is going to be executed

print("I was asleep for " + str(sleep_time) + " seconds")
```

Given that the state of the CPU can change the execution time of our code it's important to repeat our measurements many times and the consider some way to summarize our data. We can use the median. To achive this we will use *repeat(setup, stmt, timer, number, repeat)*.
Let's measure how much time it takes to create a balanced tree with networkX. We will repeat it 100 times and then take the median of all measumerements.

```{code-cell}
import numpy as np
import time

np.median(
    timeit.repeat(
        setup="import networkx as nx",  # Setup not included into
        stmt="G = nx.balanced_tree(10, 2)",  # Code to be measured
        timer=time.process_time,  # Only measure time used by the process running this code
        number=1,
        repeat=100,
    )
)  # repetitions
```

For more information about timeit: <https://docs.python.org/3/library/timeit.html>

+++

**Disclaimer:** The graphs used in the following examples are going to be small because the execution time grows exponentially as we increase the size of the graphs otherwise the examples are going to take too much time to run. In order to do a more exhaustive benchmarking we need to repeat all the measurements many times and use bigger graphs. This notebook does not intend to be a proper benchmarking but rather a general analysis of the performance of both algorithms.

```{code-cell}
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
```

## Complete Graphs and DiGraphs without labels
We can compare both algorithms on complete graphs as a way to see how these algorithms behave on dense graphs.
Let's measure how much it takes for both algorithms to run in complete graphs as we increase the number of nodes in the graphs. For these graphs we are interested in identifying positive instances, in other words, we want to test graphs that are isomorphic.

```{code-cell}
vf2_all_times_graphs = []  # VF2 time measurements on graphs
vf2pp_all_times_graphs = []  # VF2++ time measurements on graphs

vf2_all_times_digraphs = []  # VF2 time measurements on digraphs
vf2pp_all_times_digraphs = []  # VF2++ time measurements on digraphs

for i in range(10, 120, 10):
    # time vf2 on graphs
    vf2_time_g = np.median(
        timeit.repeat(
            setup="import networkx as nx;G = nx.complete_graph(" + str(i) + ")",
            stmt="nx.is_isomorphic(G,G)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2_all_times_graphs.append(vf2_time_g)

    # time vf2++ on graphs
    vf2pp_time_g = np.median(
        timeit.repeat(
            setup="import networkx as nx;G = nx.complete_graph(" + str(i) + ")",
            stmt="nx.vf2pp_is_isomorphic(G,G)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2pp_all_times_graphs.append(vf2pp_time_g)

    # time vf2 on digraphs
    vf2_time_d = np.median(
        timeit.repeat(
            setup="import networkx as nx;G = nx.complete_graph("
            + str(i)
            + ", nx.DiGraph())",
            stmt="nx.is_isomorphic(G,G)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2_all_times_digraphs.append(vf2_time_d)

    # time vf2++ on digraphs
    vf2pp_time_d = np.median(
        timeit.repeat(
            setup="import networkx as nx;G = nx.complete_graph("
            + str(i)
            + ", nx.DiGraph())",
            stmt="nx.vf2pp_is_isomorphic(G,G)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2pp_all_times_digraphs.append(vf2pp_time_d)

# Plot results
fig, ax = plt.subplots(1, 2)

fig.set_size_inches(10, 5)

plt.suptitle("VF2 vs. VF2++ in complete graphs and digraphs", fontweight="bold")

x = list(range(10, 120, 10))  # x labels

# Plot vf2 and vf2++ in graphs
(vf2_line_g,) = ax[0].plot(
    x, vf2_all_times_graphs, label="vf2", linestyle="--", marker="o"
)
(vf2pp_line_g,) = ax[0].plot(
    x, vf2pp_all_times_graphs, label="vf2++", linestyle="--", marker="o"
)
ax[0].set_title("Graphs")
ax[0].set_ylabel("Execution Time (seconds)")
ax[0].set_xlabel("Number of nodes")

(vf2_line_d,) = ax[1].plot(
    x, vf2_all_times_digraphs, label="vf2", linestyle="--", marker="o"
)
(vf2pp_line_d,) = ax[1].plot(
    x, vf2pp_all_times_digraphs, label="vf2++", linestyle="--", marker="o"
)
ax[1].set_title("DiGraphs")
ax[1].set_ylabel("Execution Time (seconds)")
ax[1].set_xlabel("Number of nodes")

ax[0].legend(handles=[vf2_line_g, vf2pp_line_g])
ax[1].legend(handles=[vf2_line_d, vf2pp_line_d])

fig.tight_layout(pad=2.0)

plt.show()
```

As expected VF2++ performs better than VF2 as we increase the number of nodes. We can see that the curve of VF2 grows significantly faster compared to the curve of VF2++.  From this experiment, we can't affirm that VF2++ has a linear behavior on complete graphs of all sizes but under the particular circumstances of this experiment, it does look like VF2++ has a linear behavior. It's important to note that this may not be true on bigger graphs. Also, we can notice that for graphs and digraphs, the behavior of both algorithms is similar but in digraphs, the execution time is approximately twice that in graphs. This makes sense because in digraphs there are two types of edges to be considered in the matching function.

+++

## Random Regular Graphs

+++

A random $d$-regular graph is a graph randomly selected from all $d$-regular graphs of $n$ vertices, where $3\leq d < n$ and $nr$ is even. A $d$-regular graph is a graph where each node has exactly $d$ neighbors. That means that all nodes have the same degree. These graphs are interesting for our experiments because as we increase $d$ we will have graphs that get denser. This way we can easily test how the algorithms perform as we make graphs denser. In our example, we take a graph of 15 nodes and we will increase $d$. Again We will focus on positive instances.

```{code-cell}
vf2_all_times = [] #VF2 time measurements
vf2pp_all_times = [] #VF2++ time measurements


for i in range(0, 10, 2):
    # vf2
    vf2_time = np.median(
        timeit.repeat(
            setup="import networkx as nx;G = nx.random_regular_graph("
            + str(i)
            + ",15 , seed= 104)",
            stmt="nx.is_isomorphic(G,G)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2_all_times.append(vf2_time)

    # vf2++
    vf2pp_time = np.median(
        timeit.repeat(
            setup="import networkx as nx;G = nx.random_regular_graph("
            + str(i)
            + ",15 , seed= 104)",
            stmt="nx.vf2pp_is_isomorphic(G,G)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2pp_all_times.append(vf2pp_time)

# Plot results
fig, ax = plt.subplots()

x = list(range(0, 10, 2))

(vf2_line,) = ax.plot(x, vf2_all_times, label="vf2", linestyle="--", marker="o")
(vf2pp_line,) = ax.plot(x, vf2pp_all_times, label="vf2++", linestyle="--", marker="o")

plt.title("VF2 vs. VF2++ in random regular graphs of 15 nodes", fontweight="bold")
plt.ylabel("Execution Time (seconds)")
plt.xlabel("Number of neighbours")
ax.legend(handles=[vf2_line, vf2pp_line])

plt.show()
```

Once again, VF2++ is significantly faster than VF2. It's interesting to note that the execution time of VF2++ doesn't always increase as graphs become denser. This can be due to the fact that node ordering is more effective on some graphs than others. In some cases, unproductive matching functions may be explored first, causing VF2++ to be slower on smaller graphs.

+++

## Erdos-Renyi Random graphs and digraphs
A random erdos-renyi graph $G_{n, p}$ is a graph of $n$ nodes where all possible edges are added with probability $p$. With these graphs we can easily create graphs with similar density for multiple values of $n$. We will use them to see how the algorithms behave on graphs with the same density as we increase the number of nodes in positive instances.
Let's do this experiment for different values of $p$:

```{code-cell}
p = [0.1, 0.3, 0.5, 0.6] #Define probabilities

vf2_all_times = [] #vf2 time measurements
vf2pp_all_times = [] #vf2++ time measurements

for j in range(0, len(p)):
    vf2 = []
    vf2pp = []
    for i in range(0, 101, 10):
        # vf2
        vf2_time = np.median(
            timeit.repeat(
                setup="import networkx as nx;G = nx.erdos_renyi_graph("
                + str(i)
                + ","
                + str(p[j])
                + ", seed= 200)",
                stmt="nx.is_isomorphic(G,G)",
                timer=time.process_time,
                number=1,
                repeat=100,
            )
        )
        vf2.append(vf2_time)

        # vf2++
        vf2pp_time = np.median(
            timeit.repeat(
                setup="import networkx as nx;G = nx.erdos_renyi_graph("
                + str(i)
                + ", "
                + str(p[j])
                + " , seed= 200)",
                stmt="nx.vf2pp_is_isomorphic(G,G)",
                timer=time.process_time,
                number=1,
                repeat=100,
            )
        )
        vf2pp.append(vf2pp_time)
    vf2_all_times.append(vf2)
    vf2pp_all_times.append(vf2pp)

# Plot results
fig, axs = plt.subplots(2, 2)

fig.set_size_inches(10, 5)

x = list(range(0, 101, 10))

plt.suptitle("VF2 vs. VF2++ in random erdos-renyi Graphs", fontweight="bold")

(vf2_line1,) = axs[0][0].plot(
    x, vf2_all_times[0], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line1,) = axs[0][0].plot(
    x, vf2pp_all_times[0], label="vf2++", linestyle="--", marker="o"
)
axs[0][0].set_title("p = 0.1")
axs[0][0].set_ylabel("Execution Time (seconds)")
axs[0][0].set_xlabel("Number of nodes")

(vf2_line2,) = axs[0][1].plot(
    x, vf2_all_times[1], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line2,) = axs[0][1].plot(
    x, vf2pp_all_times[1], label="vf2++", linestyle="--", marker="o"
)
axs[0][1].set_title("p = 0.3")
axs[0][1].set_ylabel("Execution Time (seconds)")
axs[0][1].set_xlabel("Number of nodes")

(vf2_line2,) = axs[1][0].plot(
    x, vf2_all_times[2], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line2,) = axs[1][0].plot(
    x, vf2pp_all_times[2], label="vf2++", linestyle="--", marker="o"
)
axs[1][0].set_title("p = 0.5")
axs[1][0].set_ylabel("Execution Time (seconds)")
axs[1][0].set_xlabel("Number of nodes")

(vf2_line2,) = axs[1][1].plot(
    x, vf2_all_times[3], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line2,) = axs[1][1].plot(
    x, vf2pp_all_times[3], label="vf2++", linestyle="--", marker="o"
)
axs[1][1].set_title("p = 0.6")
axs[1][1].set_ylabel("Execution Time (seconds)")
axs[1][1].set_xlabel("Number of nodes")

axs[0][0].legend(handles=[vf2_line1, vf2pp_line1])
axs[0][1].legend(handles=[vf2_line2, vf2pp_line2])
axs[1][0].legend(handles=[vf2_line1, vf2pp_line1])
axs[1][1].legend(handles=[vf2_line2, vf2pp_line2])

fig.tight_layout(pad=2.0)
plt.show()
```

Now we can do the same analysis in DiGraphs.

```{code-cell}
p = [0.1, 0.3, 0.5, 0.6] #Define probabilities

vf2_all_times = [] #VF2 time measurements
vf2pp_all_times = [] #VF2++ time measurements

for j in range(0, len(p)):
    vf2 = []
    vf2pp = []
    for i in range(0, 101, 10):
        # vf2
        vf2_time = np.median(
            timeit.repeat(
                setup="import networkx as nx;G = nx.erdos_renyi_graph("
                + str(i)
                + ","
                + str(p[j])
                + ", seed= 200, directed=True)",
                stmt="nx.is_isomorphic(G,G)",
                timer=time.process_time,
                number=1,
                repeat=100,
            )
        )
        vf2.append(vf2_time)

        # vf2++
        vf2pp_time = np.median(
            timeit.repeat(
                setup="import networkx as nx;G = nx.erdos_renyi_graph("
                + str(i)
                + ", "
                + str(p[j])
                + " , seed= 200, directed=True)",
                stmt="nx.vf2pp_is_isomorphic(G,G)",
                timer=time.process_time,
                number=1,
                repeat=100,
            )
        )
        vf2pp.append(vf2pp_time)
    vf2_all_times.append(vf2)
    vf2pp_all_times.append(vf2pp)

# Plot results
fig, axs = plt.subplots(2, 2)

fig.set_size_inches(10, 5)

x = list(range(0, 101, 10))

plt.suptitle("VF2 vs. VF2++ in random erdos-renyi DiGraphs", fontweight="bold")

(vf2_line1,) = axs[0][0].plot(
    x, vf2_all_times[0], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line1,) = axs[0][0].plot(
    x, vf2pp_all_times[0], label="vf2++", linestyle="--", marker="o"
)
axs[0][0].set_title("p = 0.1")
axs[0][0].set_ylabel("Execution Time (seconds)")
axs[0][0].set_xlabel("Number of nodes")

(vf2_line2,) = axs[0][1].plot(
    x, vf2_all_times[1], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line2,) = axs[0][1].plot(
    x, vf2pp_all_times[1], label="vf2++", linestyle="--", marker="o"
)
axs[0][1].set_title("p = 0.3")
axs[0][1].set_ylabel("Execution Time (seconds)")
axs[0][1].set_xlabel("Number of nodes")

(vf2_line2,) = axs[1][0].plot(
    x, vf2_all_times[2], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line2,) = axs[1][0].plot(
    x, vf2pp_all_times[2], label="vf2++", linestyle="--", marker="o"
)
axs[1][0].set_title("p = 0.5")
axs[1][0].set_ylabel("Execution Time (seconds)")
axs[1][0].set_xlabel("Number of nodes")

(vf2_line2,) = axs[1][1].plot(
    x, vf2_all_times[3], label="vf2", linestyle="--", marker="o"
)
(vf2pp_line2,) = axs[1][1].plot(
    x, vf2pp_all_times[3], label="vf2++", linestyle="--", marker="o"
)
axs[1][1].set_title("p = 0.6")
axs[1][1].set_ylabel("Execution Time (seconds)")
axs[1][1].set_xlabel("Number of nodes")

axs[0][0].legend(handles=[vf2_line1, vf2pp_line1])
axs[0][1].legend(handles=[vf2_line2, vf2pp_line2])
axs[1][0].legend(handles=[vf2_line1, vf2pp_line1])
axs[1][1].legend(handles=[vf2_line2, vf2pp_line2])

fig.tight_layout(pad=2.0)
plt.show()
```

In both graphs and directed graphs, the experimental results are quite similar. VF2++ continues to outperform VF2. The growth of VF2's execution time increases exponentially as the number of nodes increases, while VF2++ has a linear behavior. Additionally, it's noteworthy that for all values of $p$, the curves of VF2 and VF2++ are very similar, with the only difference being the increase in execution time as the graphs become denser.

+++

## Create graphs from a degree secuence

To test on negative instances, in other words, graphs that are not isomorphic we need to create graphs with the same degree sequence. For that, we can use *nx.configuration_model(degree_sequence)* that creates a random MultiGraph with the given degree sequence. The degree sequence must have an even sum. Then we can just convert the resulting MultiGraph into a Graph. Let's see in an example how can we experiment with this:

```{code-cell}
# Example
import random

random.seed(11)  # Set a random seed
d = random.choices(
    list(range(0, 5)), k=11
)  # Create a list with 11 random numbers in [0, 5]

print("Is the sequence sum even?", np.sum(d) % 2 == 0)

# Create 2 different random graphs with the same degree secuence
g1 = nx.Graph(nx.configuration_model(d, seed=10))
g1.remove_edges_from(nx.selfloop_edges(g1))

g2 = nx.Graph(nx.configuration_model(d, seed=11))
g2.remove_edges_from(nx.selfloop_edges(g2))

print(g1)
print("Are isomorphic? ", nx.is_isomorphic(g1, g2))
```

To do this same experiment on DiGraphs, we need to define an in-degree sequence and an out-degree sequence.  
We will use the function *nx.directed_configuration_model(in_degree_sequence, out_degree_sequence, create_using, seed)*. Both degree sequences must have the same sum. Again this function returns a MultiDiGraph so we will have to convert it into a DiGraph. Let's do this in an example:

```{code-cell}
# Example
import random

random.seed(11)  # Set a random seed
d = random.choices(
    list(range(0, 5)), k=11
)  # Create a list with 11 random numbers in [0, 5]

print("Is the sequence sum even? ", np.sum(d) % 2 == 0)

# Create 2 different random digraphs with the same degree secuence
g1 = nx.directed_configuration_model(d, d, create_using=nx.DiGraph, seed=10)
g1.remove_edges_from(nx.selfloop_edges(g1))

g2 = nx.directed_configuration_model(d, d, create_using=nx.DiGraph, seed=11)
g2.remove_edges_from(nx.selfloop_edges(g2))
print(g1)
print("Are isomorphic? ", nx.is_isomorphic(g1, g2))
```

Then we can create two random graphs with the same degree sequence and check that they are not isomorphic. The values of $k$ where chosen because they return a sequence with an even sum using these seeds.

```{code-cell}
k = [10, 11, 15, 18, 24, 32]  # Network sizes

vf2_all_times_graphs = []  # VF2 time measurements on graphs
vf2pp_all_times_graphs = []  # VF2++ time measurements on graphs

vf2_all_times_digraphs = []  # VF2 time measurements on digraphs
vf2pp_all_times_digraphs = []  # VF2++ time measurements on digraphs

for i in range(0, len(k)):
    # time vf2 on graphs
    vf2_time_g = np.median(
        timeit.repeat(
            setup="import networkx as nx;import random;random.seed(11);d = random.choices(list(range(0, 5)), k ="
            + str(k[i])
            + ");g1 = nx.Graph(nx.configuration_model(d, seed = 11));g1.remove_edges_from(nx.selfloop_edges(g1)); g2 = nx.Graph(nx.configuration_model(d, seed = 11));g2.remove_edges_from(nx.selfloop_edges(g2))",
            stmt="nx.is_isomorphic(g1,g2)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2_all_times_graphs.append(vf2_time_g)

    # time vf2++ on graphs
    vf2pp_time_g = np.median(
        timeit.repeat(
            setup="import networkx as nx;import random;random.seed(11);d = random.choices(list(range(0, 5)), k ="
            + str(k[i])
            + ");g1 = nx.Graph(nx.configuration_model(d, seed = 11));g1.remove_edges_from(nx.selfloop_edges(g1)); g2 = nx.Graph(nx.configuration_model(d, seed = 11));g2.remove_edges_from(nx.selfloop_edges(g2))",
            stmt="nx.is_isomorphic(g1,g2)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2pp_all_times_graphs.append(vf2pp_time_g)

    # time vf2 on digraphs
    vf2_time_d = np.median(
        timeit.repeat(
            setup="import networkx as nx;import random;random.seed(11);d = random.choices(list(range(0, 5)), k ="
            + str(k[i])
            + ");g1 =nx.directed_configuration_model(d,d, create_using = nx.DiGraph, seed = 10);g1.remove_edges_from(nx.selfloop_edges(g1)); g2 =nx.directed_configuration_model(d,d, create_using = nx.DiGraph, seed = 11);g2.remove_edges_from(nx.selfloop_edges(g2))",
            stmt="nx.is_isomorphic(g1,g2)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2_all_times_digraphs.append(vf2_time_d)

    # time vf2++ on digraphs
    vf2pp_time_d = np.median(
        timeit.repeat(
            setup="import networkx as nx;import random;random.seed(11);d = random.choices(list(range(0, 5)), k ="
            + str(k[i])
            + ");g1 = nx.directed_configuration_model(d,d, create_using = nx.DiGraph, seed = 10);g1.remove_edges_from(nx.selfloop_edges(g1)); g2 = nx.directed_configuration_model(d,d, create_using = nx.DiGraph, seed = 11);g2.remove_edges_from(nx.selfloop_edges(g2))",
            stmt="nx.is_isomorphic(g1,g2)",
            timer=time.process_time,
            number=1,
            repeat=100,
        )
    )
    vf2pp_all_times_digraphs.append(vf2pp_time_d)

# Code used to generate the plot
"""
fig, ax = plt.subplots(1, 2)

fig.set_size_inches(10, 5)

plt.suptitle(
    "VF2 vs. VF2++ in random Graphs and DiGraphs with the same degree secuence",
    fontweight="bold",
)

# Plot vf2 and vf2++ in graphs

(vf2_line_g,) = ax[0].plot(
    k, vf2_all_times_graphs, label="vf2", linestyle="--", marker="o"
)
(vf2pp_line_g,) = ax[0].plot(
    k, vf2pp_all_times_graphs, label="vf2++", linestyle="--", marker="o"
)
ax[0].set_title("Graphs")
ax[0].set_ylabel("Execution Time (seconds)")
ax[0].set_xlabel("Number of nodes")

(vf2_line_d,) = ax[1].plot(
    k, vf2_all_times_digraphs, label="vf2", linestyle="--", marker="o"
)
(vf2pp_line_d,) = ax[1].plot(
    k, vf2pp_all_times_digraphs, label="vf2++", linestyle="--", marker="o"
)
ax[1].set_title("DiGraphs")
ax[1].set_ylabel("Execution Time (seconds)")
ax[1].set_xlabel("Number of nodes")

ax[0].legend(handles=[vf2_line_g, vf2pp_line_g])
ax[1].legend(handles=[vf2_line_d, vf2pp_line_d])

fig.tight_layout(pad=3.0)
"""
#Show plot that was generated beforehand
fig,ax = plt.subplots(1, figsize = (15, 10))
img = plt.imread("same_degree_seq.png")

ax.imshow(img)
plt.axis('off')
plt.show()
```

The results of the experiment on both graphs and directed graphs are quite similar. When the two graphs/directed graphs are not isomorphic, VF2 and VF2++ have similar performance. This outcome is understandable since both algorithms involve exploring all possible node matchings. However, it's also noteworthy that the enhancements in VF2++ do not negatively impact its performance even when all branches have to be partially explored. Additionally, it can be observed that the execution time on directed graphs is significantly higher than on graphs.

+++

## Protein Dataset

+++

To go one step further with our experiments we can test how the algorithms perform on specific datasets. We will work with a dataset of proteins. This dataset from TUDataset has 1113 graphs with node labels. The graphs have between 4 and 620 nodes.

The dataset source is: <https://chrsmrrs.github.io/datasets/>

To run this experiment by yourself you need to run the following script
[Measure VF2 and VF2++ on PROTEINS](proteins_dataset_vf2vsvf2pp.py)

```{code-cell}
# This plot was generated with the 900 smaller graphs and all measurements were repeated 300 times.
fig,ax = plt.subplots(1, figsize = (10, 10))
img = plt.imread("ex_PROTEINS.png")
plt.imshow(img)
plt.axis('off')
plt.show()
```

As we can see in the plot VF2++ performs significantly better than VF2 on the dataset. Also, the performance of both algorithms is the same as we saw in the previous experiments.

+++

## Final conclusions
After all the different experiments, We can conclude that
- VF2++ performed significantly better than VF2 in all experiments on positive instances. But it's important to keep in mind that these experiments depend a lot on the state of the machine that was used. And to perform a proper benchmarking of the algorithms we should experiment with more graphs of different sizes.
- The performance of VF2++ on the proteins dataset was significantly better than VF2 with similar results to the other experiments.
- In negative instances the performance of both algorithms was similar which means that the improvements in VF2++ don't introduce a notable overhead.

+++

## References
- L. P. Cordella, P. Foggia, C. Sansone, M. Vento, “An Improved Algorithm for Matching Large Graphs”, 3rd IAPR-TC15 Workshop on Graph-based Representations in Pattern Recognition, Cuen, pp. 149-159, 2001. <https://www.researchgate.net/publication/200034365_An_Improved_Algorithm_for_Matching_Large_Graphs>
- Jüttner, Alpár & Madarasi, Péter. (2018). “VF2++—An improved subgraph isomorphism algorithm”. Discrete Applied Mathematics. 242. <https://doi.org/10.1016/j.dam.2018.02.018>
