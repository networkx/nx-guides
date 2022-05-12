---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Centrality Algorithms

```python
import networkx as nx
import matplotlib.pyplot as plt
import random as ran
import numpy as np
import seaborn as sns
import pandas as pd
```

```python
G = nx.read_gml("data/polblogs.gml")
```

# Initial Analysis of the Network

```python
print("Number of Nodes in the Network is {}".format(nx.number_of_nodes(G)))
print("Number of Edges in the Network is {}".format(nx.number_of_edges(G)))
print(nx.is_directed(G))
```

**Source**\
http://www-personal.umich.edu/~mejn/netdata/ \
It represents hyperlinks between weblogs on US politics, recorded in 2005.\
It is a Directed MultiGraph Network with **1490** nodes and **19090** edges. Each node represents a Political Blog.

```python
def max_vals(func):
    centrality = func
    highest_nodes, highest_vals = [], []
    sorted_list = list(sorted(centrality.items(), key = lambda item : item  [1]))[-5:]
    for u,v in sorted_list:
        highest_nodes.append(u)
        highest_vals.append(v)

    print(highest_nodes)
    print([round(num, 2) for num in highest_vals])   
    
def distribution(func , title, limits):
    centrality = func
    plt.figure(figsize = (8, 5))
    plt.hist(centrality.values(), bins = np.arange(limits[0],limits[1],limits[2]), density = True, alpha = 0.65, edgecolor = "black")
    sns.kdeplot(list(centrality.values()),color="purple", shade = True, label = "KDE plot of {}".format(title))
    plt.legend()
    plt.xlim(limits[0],limits[1])
    plt.xlabel(title)
    plt.ylabel("Count")
    plt.title("Distribution of {}".format(title))
    plt.show()
```

# Degree Centrality

```python
max_vals(nx.degree_centrality(G))
distribution(nx.degree_centrality(G), "Degree Centrality", [0,0.4, 0.01])
```

```python
max_vals(nx.in_degree_centrality(G))
distribution(nx.in_degree_centrality(G), "In-Degree Centrality", [0,0.3, 0.01])
```

```python
max_vals(nx.out_degree_centrality(G))
distribution(nx.out_degree_centrality(G), "In-Degree Centrality", [0,0.2, 0.01])
```

## Analysis of Degree Centrality

| Rank  | **Degree**            | **Value** | **In-degree**         | **Value** | **Out-degree**            | **Value** |
|-------|-----------------------|-----------|-----------------------|-----------|---------------------------|-----------|
| **1** | blogsforbush.com      | 0.31      | dailykos.com          | 0.23      | blogsforbush.com          | 0.17      |
| **2** | dailykos.com          | 0.26      | instapundit.com       | 0.19      | newleftblogs.blogspot.com | 0.09      |
| **3** | instapundit.com       | 0.24      | talkingpointsmemo.com | 0.18      | politicalstrategy.org     | 0.09      |
| **4** | atrios.blogspot.com   | 0.24      | atrios.blogspot.com   | 0.18      | madkane.com/notable.html  | 0.09      |
| **5** | talkingpointsmemo.com | 0.19      | drudgereport.com      | 0.16      | cayankee.blogs.com        | 0.08      |

1. According to the Values summarised above, **"blogsforbus.com"** and **"dailykos.com"** seems like the most Central Blog depending on Degree. While  "blogsforbus.com" has a very high Out Degree, "dailykos.com" has highest In-degree. 
2. From the plots , it is clear that a large part of the blogs are not connected to the Network. They have 0 Degree in all.
3. The Degree Centrality follows a **Scale-Free Distribution**.


# Closeness Centrality

```python
max_vals(nx.closeness_centrality(G))
distribution(nx.closeness_centrality(G), "Closeness Centrality", [0,0.4, 0.01])
```

1. There are a large number of nodes that are having very low Closeness Centrality. 
2. It almost follows a Normal distribution around 0.20 after that.
3. "dailykos.com" has **highest Closeness Centrality**.


# Betweenness Centrality

```python
max_vals(nx.betweenness_centrality(G))
distribution(nx.betweenness_centrality(G), "Betweenness Centrality", [0,0.1, 0.005])
```

1. There are a large number of nodes that are having very low Betweenness Centrality. 
2. It follows a Scale Free Distribution.
3. "blogsforbush.com" has **highest Betweenness Centrality**.


# Harmonic Centrality

```python
max_vals(nx.harmonic_centrality(G))
distribution(nx.harmonic_centrality(G), "Harmonic Centrality", [0,650,50])
```

1. It follows a similar Pattern to the Closeness Centrality.
2. "dailykos.com" has **highest Harmonic Centrality**.


# Reaching

```python
node = ran.choice(list(G.nodes()))
local_reach_cent = nx.local_reaching_centrality(G, node)
print('Political Blog is {}'.format(node))
print("Local Reach Centrality is {:.2f}".format(local_reach_cent))
```

This value gives the percentage of nodes that can be reached through that particular node.\
Till now the most Central nodes seemed like  'dailykos.com' and 'blogsforbush.com'. Comparing the Local Reaching of both gives:

```python
print("Local Reach Centrality for 'dailykos.com' is {:.2f}".format(nx.local_reaching_centrality(G, 'dailykos.com')))
print("Local Reach Centrality for 'blogsforbush.com' is {:.2f}".format(nx.local_reaching_centrality(G, 'blogsforbush.com')))
```

It has same value for both **'dailykos.com' and 'blogsforbush.com'.**

```python
global_reach_cent = nx.global_reaching_centrality(G)
print("Global Reach Centrality is {:.2f}".format(global_reach_cent))
```

# Load Centrality

```python
max_vals(nx.load_centrality(G))
distribution(nx.load_centrality(G), "Load Centrality", [0,0.1,0.01])
```

1. Most Nodes are having a Load Centrality lower than 0.01. 
2. Highest value obtained is 0.09 : for "blogsforbush.com".


# Group Centrality

3 Random nodes are taken from the Network and its Group Centrality is seen.

```python
sources = ran.sample(G.nodes(), 3)
print("The nodes are {}".format(sources))
print("In-degree Centrality of these are {:.2f}".format(nx.group_in_degree_centrality(G, sources)))
```

```python
print("Out-degree Centrality of these are {:.2f}".format(nx.group_out_degree_centrality(G, sources)))
```

# Dispersion

```python
largest = max(nx.strongly_connected_components(G), key=len)
R = ran.sample(largest, 20)

comb = [[i,j] for i in list(R) for j in list(R)]

dispersion = [nx.dispersion(G, u, v) for [u,v] in comb]

data = {'Source': [comb[i][0] for i in range(len(comb))], 'Target': [comb[i][1] for i in range(len(comb))], "Dispersion": dispersion}
df = pd.DataFrame(data)
```

```python
values = df.pivot("Source", "Target", "Dispersion")
plt.figure(figsize = (12,12))
sns.heatmap(values, annot=True)
```

The Figure above shows the dispersion between any two nodes that are randomly chosen from the most strongly connected Component within the Network. Higher the Dispersion, less connected will be their Mutual Ties. 


# Voterank

```python
nx.voterank(G, 10)
```

1. This algorithm helps in understanding the most Influential Nodes in a Network. 
2. The above 10 Blogs are the most influential ones.
3. "blogsforbush.com" is the **most Influential** in the Network.


# Summary

Based on all the Centrality Algorithms that can be used for this type of Network, the Blogs that had highest values in each case are:

| Centrality Algorithm       | **Node with Highest Value** |
|----------------------------|:---------------------------:|
| **Degree Centrality**      |      'blogsforbush.com'     |
| **In-Degree Centrality**   |        'dailykos.com'       |
| **Out_Degree Centrality**  |      'blogsforbush.com'     |
| **Closeness Centrality**   |        'dailykos.com'       |
| **Betweenness Centrality** |      'blogsforbush.com'     |
| **Harmonic Centrality**    |        'dailykos.com'       |
| **Local Reaching**         |             Same            |
| **Load Centrality**        |      'blogsforbush.com'     |
| **Voterank**               |      'blogsforbush.com'     |




1. Based on several Algorithms, it is difficult to just name one node as the Central one. 
2. Here both the Political Blogs **'blogsforbush.com'** and **'dailykos.com'**  are exerting a big influence within the Network. 
3. Moving from one Blog to another, the hyperlinks have some sort of connection with these two at the end. 

**This allows us to conclude that studying these two blogs will bring about the best results if any change is brought in any.**
