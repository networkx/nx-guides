
In this tutorial, we are going to talk about the graph coloring methods implemented in networkx. In the graph coloring problems, we assign minimum possible labels/colors that are subjected to certain conditions.

+++

In networkx, there are two types of graph coloring methods (both are vertex coloring methods):

1. Greedy Coloring:


        - Constraints/Conditions:
                1. directly connected nodes should not have the same color
                
2.  Equitable Coloring:


        - Constraints/Conditions: 
                1. directly connected node should not be same color
                2. The number of nodes for each color should differ at max by 1/2



```{code-cell}
# Import the libraries
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import networkx as nx
import matplotlib.animation as animation
import numpy as np
import folium
import json
import requests

%matplotlib inline
```

### Greedy Coloring:

The priority of colors/labels assigned is given by the strategies. Below is the list of strategies in networkx.
You can also add your custom strategy.

```{code-cell}
# Load the stratagies for the greedy coloring present in the networkx library
strategies = nx.coloring.greedy_coloring.STRATEGIES
```

```{code-cell}
print("\n".join(strategies.keys()))
```

    largest_first
    random_sequential
    smallest_last
    independent_set
    connected_sequential_bfs
    connected_sequential_dfs
    connected_sequential
    saturation_largest_first
    DSATUR
    

```{code-cell}
def custom_strategy_implementation(G, colors):
    """
    In this strategy we are returning the priority according to
    betweeness centrality of each node.
    Parameters:
    ----------
    G: Graph object
    colors: dictionary of colors
    yield:
    ------
      node with highest priority in this case betweeness centrality
    """
    # Calculate betweeness centrality
    centrality = nx.betweenness_centrality(G)
    # Sort the nodes according to betweeness centrality
    centrality = sorted(centrality, key=centrality.get)
    # Return the node with highest priority
    yield from centrality
```

```{code-cell}
strategies["custom_strategy_implementation"] = custom_strategy_implementation
```

```{code-cell}
# Generate a random graph
random_graph = nx.erdos_renyi_graph(9, 0.5, seed=4)
# Plot the graph
nx.draw(random_graph, with_labels=True)
```



+++

![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_7_0.png)
    


```{code-cell}
# Get the greedy coloring for all the strategies
colors = {
    current_strategy: nx.greedy_color(random_graph, strategy=current_strategy)
    for current_strategy in strategies
}
```

```{code-cell}
# Show the greedy coloring for selected strategy: DSATUR
selected_strategy = "DSATUR"

# Get the position of the nodes
pos = nx.spring_layout(random_graph, seed=32)
# Get the node order
node_order = list(colors[selected_strategy].keys())
# Get the node colors
node_colors = list(colors[selected_strategy].values())

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 10))

# Create the legend
create_legend = plt.cm.RdYlGn
legend = create_legend(np.arange(create_legend.N))
# Plot the legend
ax.imshow(
    [legend],
    extent=[0.6, 1, 0.85, 0.9],
)
# Plot the nodes
nx.draw_networkx_nodes(
    node_order,
    pos=pos,
    node_color=node_colors,
    node_size=500,
    alpha=0.7,
    cmap=plt.cm.RdYlGn,
    label="Node",
    ax=ax,
)
# Plot the labels
nx.draw_networkx_labels(random_graph, pos=pos, font_size=10, font_family="sans-serif")
# Plot the edges
nx.draw_networkx_edges(random_graph, pos=pos)
```





    <matplotlib.collections.LineCollection at 0x18e6f8b0eb0>




    
![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_9_1.png)
    

+++

#### Creating animation of the strategies as more nodes are added 

```{code-cell}
# Create subgraphs for animation
subgraphs = [
    nx.subgraph(random_graph, list(range(i))) for i in range(1, len(random_graph.nodes))
]
```

```{code-cell}
# Update function for animation: This function will be called for each frame
def update(i):
    """
    Update the plot for each frame

    Parameters
    ----------
    i : int
       The current frame number
    """
    j = 0
    create_legend = plt.cm.RdYlGn
    legend = create_legend(np.arange(create_legend.N))

    for current_strategy in strategies:
        # Clear the previous plot
        ax[j].clear()

        # Get the node colors
        node_colors = [
            colors[current_strategy].get(node) for node in subgraphs[i].nodes
        ]
        # Plot the networkx graph
        nx.draw(
            subgraphs[i],
            pos=pos,
            ax=ax[j],
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            cmap=plt.cm.RdYlGn,
            font_size=10,
            font_family="sans-serif",
            alpha=0.7,
        )
        # Set the title
        ax[j].set_title(current_strategy)
        # Update for the next plot
        j += 1
```

```{code-cell}
%matplotlib agg

# Create the figure and axis
fig, all_axes = plt.subplots(5, 2, figsize=(20, 20))
# Flatten the axes
ax = all_axes.flat

# Create the animation
ani = animation.FuncAnimation(
    fig,
    func=update,
    frames=len(subgraphs),
)
```

```{code-cell}
# Save the animation as gif
gif_file_path = r"greedy_coloring.gif"
writergif = animation.PillowWriter(fps=1)
ani.save(gif_file_path, writer=writergif)
```

```{code-cell}
# Display the animation from the gif file
def display_animation(gif_file_path):
    from IPython.display import Image

    display(Image(data=open(gif_file_path, "rb").read(), format="png"))
```

```{code-cell}
display_animation(gif_file_path)
```



+++

![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_16_0.png)
    

+++

#### Four Color Theorom:
    - Example of the use of greedy coloring
    - The four color theorom states that any maps with neighbours requires only 4 or less colors 
    - The below uses indian map and shows the example of the four color theorom

```{code-cell}
%matplotlib inline


intial_location = (21.1458, 79.0882)

m = folium.Map(location=intial_location, zoom_start=4)
```

```{code-cell}
indian_map_url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
indian_map_data = json.loads(requests.get(indian_map_url).text)
```

```{code-cell}
# load the states data
state_data = gpd.read_file(indian_map_url)
```

```{code-cell}
# load the state boundaries (Uncomment the below line to get interactive map)
# state_data.explore(m=m)
```




+++

![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_21_0.png)
    



```{code-cell}
def get_neighbor_links(row):
    neighbors = state_data[state_data.geometry.touches(row["geometry"])].ID_1.tolist()
    return neighbors
```

```{code-cell}
state_data["neighbors"] = state_data.apply(get_neighbor_links, axis=1)
```

```{code-cell}
state_data["neighbors"] = state_data.apply(lambda x: get_neighbor_links(x), axis=1)
```

```{code-cell}
indian_states = nx.from_pandas_edgelist(
    state_data.explode(column="neighbors"), "ID_1", "neighbors"
)
indian_states.remove_node(np.nan)
```

```{code-cell}
pos = nx.spring_layout(indian_states, seed=32)
nx.draw(indian_states, with_labels=True)
```



+++

![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_26_0.png)
    


```{code-cell}
india_state_colors = {
    current_strategy: nx.greedy_color(
        indian_states, strategy=strategies[current_strategy]
    )
    for current_strategy in strategies
}

#
```

```{code-cell}
selected_strategy = "custom_strategy_implementation"
```

```{code-cell}
pos = nx.spring_layout(indian_states, seed=20)

nx.draw_networkx_nodes(
    list(india_state_colors[selected_strategy].keys()),
    pos=pos,
    node_color=list(india_state_colors[selected_strategy].values()),
    node_size=500,
    alpha=0.7,
    cmap=plt.cm.RdYlGn,
    label="Node",
)
nx.draw_networkx_labels(indian_states, pos=pos, font_size=10, font_family="sans-serif")
patch = nx.draw_networkx_edges(indian_states, pos=pos)
```



+++

![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_29_0.png)
    


```{code-cell}
state_data["color"] = state_data["ID_1"].map(india_state_colors[selected_strategy])
state_data["color"].fillna(
    0, inplace=True
)  # assigning default color to states without any neighbours
```

```{code-cell}
state_data.explore(
    m=m,
    column="color",
    cmap="RdYlGn",
)
folium.LayerControl().add_to(m)  # use folium to add layer control
```





    <folium.map.LayerControl at 0x18e6f8f8c40>




```{code-cell}
# Show the map, uncomment the below line to get interactive map
# m
```




+++

![png](graph-coloring/graph_coloring_files/graph-coloring/graph_coloring_32_0.png)
