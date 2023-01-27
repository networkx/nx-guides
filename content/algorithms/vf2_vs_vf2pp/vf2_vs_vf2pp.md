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

**(TODO: maybe link to the isomorphism notebook)**

**What's new on VF2++?** 
- Node ordering: Previously the order in which the nodes were explored was determined by the labels. In this new algorithm, a particular node order is defined for every graph in order to explore the "rarest" nodes first. The "rarest" nodes are defined based on the graph structure.   
- Simple-to-check cutting rules. These new rules are cheaper than the old ones but are just as effective to determine if a branch is unfruitful. 
- A non-recursive implementation that saves both time and space. 

Let's see an example of how to use VF2 and VF2++ to test for isomorphism with NetworkX.

```{code-cell} ipython3
import networkx as nx

G = nx.bull_graph()

print("VF2:  ", nx.is_isomorphic(G, G)) #VF2

print("VF2++: ",nx.vf2pp_is_isomorphic(G,G)) #VF2++
```

## Analysis: General approach 
To compare the performance of both algorithms we will run the algorithms over many different types of graphs and digraphs. The analysis will be divided as follows:
- Graphs (with and without labels)
    - Dense 
    - Sparce 
    - Densification of graphs: From sparce to dense
    - Connected vs unconnected 
- Digraphs (with and without labels)
    - Dense 
    - Sparce 
    - From sparce to dense

+++

To measure execution time we can use the function *timeit(setup, stmt, number )*. Where *stmt* is the code that we want to time, *setup* is the code needed to run stmt but that we don't want to time and *number* is how many times stmt is run. 

Let's see an example:

```{code-cell} ipython3
import timeit

sleep_time = timeit.timeit(setup = "import time", #Setup code
              stmt = "time.sleep(2)", #Code to be timed  
              number = 1) #Number of times my code is going to be executed 

print("I was asleep for " + str(sleep_time) + " seconds")
```

Given that the state of the CPU can change the execution time of our code it's important to repeat our measurements many times and the consider some way to summarize our data. We can use the median. To achive this we will use *repeat(setup, stmt, timer, number, repeat)*. 
Let's measure how much time it takes to create a balanced tree with networkX. We will repeat it 100 times and then take the median of all measumerements.

```{code-cell} ipython3
import numpy as np
import time
np.median(timeit.repeat(setup = "import networkx as nx", #Setup not included into
              stmt = "G = nx.balanced_tree(10, 2)", #Code to be measured 
              timer = time.process_time, #Only measure time used by the process running this code
              number = 1, 
              repeat = 100)) #repetitions
```

For more information about timeit: <https://docs.python.org/3/library/timeit.html>

+++

**Disclaimer:** The graphs used in the following examples are going to be small because the execution time grows exponentially as we increase the size of the graphs otherwise the examples are going to take too much time to run. In order to do a more exhaustive benchmarking we need to repeat all the measurements many times and use bigger graphs. This notebook does not intend to be a proper benchmarking but rather a general analysis of the performance of both algorithms. 

```{code-cell} ipython3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
```

**TODO: delete if not used**

```{code-cell} ipython3
def density(n, m):
    return m/(n*(n-1)/2)
```

## Graphs ( Without labels) 

+++

### Complete Graphs 
We can compare both algorithms on complete graphs as a way to see how these algorithms behave on dense graphs.
Let's measure how much it takes for both algorithms to run in complete graphs as we increase the number of nodes in the graphs. For these graphs we are interested in identifying positive instances, in other words, we want to test graphs that are isomorphic. 

```{code-cell} ipython3
vf2_all_times = [] #VF2 time measurements 
vf2pp_all_times = [] #VF2++ time measurements

for i in range(10, 120, 10):
    #time vf2 
    vf2_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.complete_graph(" + str(i) +")",
                             stmt= "nx.is_isomorphic(G,G)", timer = time.process_time,
                                       number=1, repeat=100))
    vf2_all_times.append(vf2_time)
    
    #time vf2++
    vf2pp_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.complete_graph(" + str(i) +")",
                               stmt= "nx.vf2pp_is_isomorphic(G,G)", timer = time.process_time,
                                         number=1, repeat=100))
    vf2pp_all_times.append(vf2pp_time)

#Plot results 
fig, ax = plt.subplots()

x = list(range(10, 120, 10)) #x labels

vf2_line, = ax.plot(x,  vf2_all_times, label = "vf2", linestyle='--', marker='o')
vf2pp_line, = ax.plot(x,vf2pp_all_times,label = "vf2++", linestyle='--', marker='o')

plt.title("VF2 vs. VF2++ on complete graphs", fontweight = "bold")
plt.ylabel("Execution Time (seconds)")
plt.xlabel("Number of nodes")  
ax.legend(handles=[vf2_line, vf2pp_line])

plt.show()
```

As expected VF2++ performs better than VF2 as we increase the number of nodes. We can see that the curve of VF2 grows significantly faster compared to the curve of VF2++.  From this experiment, we can't affirm that VF2++ has a linear behavior on complete graphs but in this particular experiment, it does look like VF2++ has a linear behavior. It's important to note that this may not be true on bigger graphs.  

+++

### Random Regular Graphs

+++

A random $d$-regular graph is a graph randomly selected from all $d$-regular graphs of $n$ vertices, where $3\leq d < n$ and $nr$ is even. A $d$-regular graph is a graph where each node has exactly $d$ neighbors. That means that all nodes have the same degree. These graphs are interesting for our experiments because as we increase $d$ we will have graphs that get denser. This way we can easily test how the algorithms perform as we make graphs denser. In our example, we take a graph of 15 nodes and we will increase $d$. Again We will focus on positive instances. 

```{code-cell} ipython3
vf2_all_times = []
vf2pp_all_times = []


for i in range(0, 10,  2):
    #vf2 
    vf2_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.random_regular_graph("+ str(i) +",15 , seed= 104)",
                             stmt= "nx.is_isomorphic(G,G)",timer = time.process_time,
                                       number=1, repeat = 100))
    vf2_all_times.append(vf2_time)
    
    #vf2++
    vf2pp_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.random_regular_graph("+ str(i) +",15 , seed= 104)",
                             stmt= "nx.vf2pp_is_isomorphic(G,G)",timer = time.process_time,
                                       number=1, repeat = 100))
    vf2pp_all_times.append(vf2pp_time)

#Plot results 
fig, ax = plt.subplots()

x = list(range(0, 10,  2))

vf2_line, = ax.plot(x, vf2_all_times, label = "vf2", linestyle='--', marker='o')
vf2pp_line, = ax.plot(x, vf2pp_all_times,label = "vf2++", linestyle='--', marker='o')

plt.title("VF2 vs. VF2++ on random regular graphs of 15 nodes", fontweight = "bold")
plt.ylabel("Execution Time (seconds)")
plt.xlabel("Number of neighbours")
ax.legend(handles=[vf2_line, vf2pp_line])

plt.show()
```

Once again VF2++ is significantly faster than VF2. It's interesting to analyze that VF2++ execution time doesn't always grow as graphs get denser. This could be explained because the node ordering works better on some graphs than on others. For some graphs, unfruitful matching functions may be explored first resulting in VF2++ being slower in some smaller graphs. 

+++

## Erdos-Renyi Random graphs
A random erdos-renyi graph $G_{n, p}$ is a graph of $n$ nodes where all possible edges are added with probability $p$. With these graphs we can easily create graphs with similar density for multiple values of $n$. We will use them to see how the algorithms behave on graphs with the same density as we increase the number of nodes in positive instances.
Let's do this experiment for different values of $p$:

+++

### TODO: case p = 0.8 and put all plots together

```{code-cell} ipython3
p = [0.1, 0.3, 0.5, 0.6]

vf2_all_times = []
vf2pp_all_times = []

for j in range(0,len(p)):
    vf2 = []
    vf2pp = []
    for i in range(0, 101, 10):
        #vf2 
        vf2_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.erdos_renyi_graph("+ str(i) +"," + str(p[j]) +", seed= 200)",
                                 stmt= "nx.is_isomorphic(G,G)", timer = time.process_time,
                                 number=1, repeat = 100))
        vf2.append(vf2_time)

        #vf2++
        vf2pp_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.erdos_renyi_graph("+ str(i) +", " + str(p[j]) +" , seed= 200)",
                                 stmt= "nx.vf2pp_is_isomorphic(G,G)", timer = time.process_time,
                                 number=1, repeat = 100))
        vf2pp.append(vf2pp_time)
    vf2_all_times.append(vf2)
    vf2pp_all_times.append(vf2pp)

#Plot results 
fig, axs = plt.subplots(2, 2)

fig.set_size_inches(10, 5)

x = list(range(0, 101, 10))

plt.suptitle("VF2 vs. VF2++ on random erdos-renyi graphs", fontweight = "bold")

vf2_line1, = axs[0][0].plot(x,  vf2_all_times[0], label = "vf2", linestyle='--', marker='o')
vf2pp_line1, = axs[0][0].plot(x, vf2pp_all_times[0],label = "vf2++", linestyle='--', marker='o')
axs[0][0].set_title("p = 0.1")
axs[0][0].set_ylabel("Execution Time (seconds)")
axs[0][0].set_xlabel("Number of nodes")

vf2_line2, = axs[0][1].plot(x,  vf2_all_times[1], label = "vf2", linestyle='--', marker='o')
vf2pp_line2, = axs[0][1].plot(x, vf2pp_all_times[1],label = "vf2++", linestyle='--', marker='o')
axs[0][1].set_title("p = 0.3")
axs[0][1].set_ylabel("Execution Time (seconds)")
axs[0][1].set_xlabel("Number of nodes")

vf2_line2, = axs[1][0].plot(x,  vf2_all_times[2], label = "vf2", linestyle='--', marker='o')
vf2pp_line2, = axs[1][0].plot(x, vf2pp_all_times[2],label = "vf2++", linestyle='--', marker='o')
axs[1][0].set_title("p = 0.5")
axs[1][0].set_ylabel("Execution Time (seconds)")
axs[1][0].set_xlabel("Number of nodes")

vf2_line2, = axs[1][1].plot(x,  vf2_all_times[3], label = "vf2", linestyle='--', marker='o')
vf2pp_line2, = axs[1][1].plot(x, vf2pp_all_times[3],label = "vf2++", linestyle='--', marker='o')
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

## Create graphs from a degree secuence 

To test on negative instances, in other words, graphs that are not isomorphic we need to create graphs with the same degree sequence. For that, we can use *nx.configuration_model(degree_sequence)* that creates a random graph with the given degree sequence. The degree sequence must have an even sum. Let's see in an example how can we experiment with this:

```{code-cell} ipython3
#Example
import random
random.seed(11) #Set a random seed 
d = random.choices(list(range(0, 5)), k =11) #Create a list with 11 random numbers in [0, 5]

print( "is even? ", np.sum(d)%2 == 0)

#Create 2 diffenrent random graphs with the same degree secuence 
g1 = nx.Graph(nx.configuration_model(d, seed = 10))
g1.remove_edges_from(nx.selfloop_edges(g1))

g2 = nx.Graph(nx.configuration_model(d, seed = 11))
g2.remove_edges_from(nx.selfloop_edges(g2))

print(nx.Graph(g1))
print("Are isomorphic? " , nx.is_isomorphic(g1, g2))
```

Then we can create 2 random graphs with the same degree sequence and check that they are not isomorphic.

```{code-cell} ipython3

vf2_all_times = []
vf2pp_all_times = []

for i in range(0, 10,  2):
    #vf2 
    vf2_time = np.median(timeit.repeat(
        setup = "import networkx as nx;import random;random.seed(11);d = random.choices(list(range(0, 5)), k =10);g1 = nx.configuration_model(d, seed = 10);g2 = nx.configuration_model(d, seed = 11)",
                             stmt= "nx.is_isomorphic(g1,g2)",timer = time.process_time,
                                       number=1, repeat = 100))
    vf2_all_times.append(vf2_time)
    
    #vf2++
    vf2pp_time = np.median(timeit.repeat(
        setup = "import networkx as nx;import random;random.seed(11);d = random.choices(list(range(0, 5)), k =10);g1 = nx.configuration_model(d, seed = 10);g2 = nx.configuration_model(d, seed = 11)",
                             stmt= "nx.is_isomorphic(g1,g2)",timer = time.process_time,
                                       number=1, repeat = 100))
    vf2pp_all_times.append(vf2pp_time)

#Plot results 
fig, ax = plt.subplots()

x = list(range(0, 10,  2))

vf2_line, = ax.plot(x,vf2_all_times, label = "vf2", linestyle='--', marker='o')
vf2pp_line, = ax.plot(x,vf2pp_all_times,label = "vf2++", linestyle='--', marker='o')

plt.title("VF2 vs. VF2++ on random graphs with the same degree secuence", fontweight = "bold")
plt.ylabel("Execution Time (seconds)")
plt.xlabel("Number of nodes")
ax.legend(handles=[vf2_line, vf2pp_line]) 

plt.show()
```

## - With labels (node vs edges)

+++

- Same graph with same attributes and same graphs with different attr

+++

# Digraphs

+++

Complete digraphs

```{code-cell} ipython3
vf2_all_times = []
vf2pp_all_times = []

for i in range(1, 120, 10):
    #time vf2 
    vf2_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.complete_graph(" + str(i) +", nx.DiGraph())",
                             stmt= "nx.is_isomorphic(G,G)", timer = time.process_time,
                                       number=1, repeat=100))
    vf2_all_times.append(vf2_time)
    
    #time vf2++
    vf2pp_time = np.median(timeit.repeat(setup = "import networkx as nx;G = nx.complete_graph(" + str(i) +", nx.DiGraph())",
                               stmt= "nx.vf2pp_is_isomorphic(G,G)", timer = time.process_time,
                                         number=1, repeat=100))
    vf2pp_all_times.append(vf2pp_time)

#Plot results 
fig, ax = plt.subplots()

vf2_line, = ax.plot(vf2_all_times, label = "vf2", linestyle='--', marker='o')
vf2pp_line, = ax.plot(vf2pp_all_times,label = "vf2++", linestyle='--', marker='o')

x = list(range(0, 120, 10))

plt.title("VF2 vs. VF2++ on complete graphs", fontweight = "bold")
plt.ylabel("Execution Time (seconds)")
plt.xlabel("Number of nodes(TODO: fix)")
ax.legend(handles=[vf2_line, vf2pp_line])
#ax.set_xticklabels(x) TODO: fix x labels 

plt.show()
```

# Final Conclusions

+++

# References
- TODO: Add Papers
