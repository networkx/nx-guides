---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Network Analysis of World Trade

+++

In this tutorial we will explore the World Trade using network analysis. We will understand how to use NetworkX for visualizing, analyzing and synthetically representing the network trade data.

We use the [BACI-CEPII dataset](http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37) that contains data on bilateral trade relations of 200 countries at the product level. Products correspond to the "Harmonized System" nomenclature (6 digit code). Compiled by the French research center CEPII, it addresses the limitations of the original UN ComTrade database, which suffers from numerous missing flows.

```{code-cell} ipython3
# imports
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    from mpl_toolkits.basemap import Basemap as Basemap
    importBasemap = True
except:
    print("Basemap cannot be imported, so Geographic visualizations will be plotted without underlying cartograph.")
    importBasemap = False
```

For the sake of convenience and scope of this tutorial, the data for trade flows of three product categories - Natural Gas (Hs6: 271111), Coffee (Hs6: 090111) and Diamonds (Hs6: 710210) was extracted to three separate CSV files. These are now imported as pandas dataframe, from where they can be converted to NetworkX Graph objects.

```{code-cell} ipython3
natural_gas = pd.read_csv("data/natural_gas.csv")
coffee = pd.read_csv("data/coffee.csv")
diamonds = pd.read_csv("data/diamonds.csv")

# latitude longitudes information of countries
country_locations = pd.read_csv("data/locations.csv")
```

```{code-cell} ipython3
edges_natural_gas = pd.DataFrame(
    {
        "source": list(natural_gas["exporter"]),
        "target": list(natural_gas["importer"]),
        "value": list(natural_gas["value"]),
        "quantity": list(natural_gas["quantity"]),
    }
)

edges_diamonds = pd.DataFrame(
    {
        "source": list(diamonds["exporter"]),
        "target": list(diamonds["importer"]),
        "value": list(diamonds["value"]),
        "quantity": list(diamonds["quantity"]),
    }
)

edges_coffee = pd.DataFrame(
    {
        "source": list(coffee["exporter"]),
        "target": list(coffee["importer"]),
        "value": list(coffee["value"]),
        "quantity": list(coffee["quantity"]),
    }
)
```

```{code-cell} ipython3
G_natural_gas = nx.from_pandas_edgelist(
    edges_natural_gas, edge_attr=True, create_using=nx.DiGraph()
)
G_coffee = nx.from_pandas_edgelist(
    edges_coffee, edge_attr=True, create_using=nx.DiGraph()
)
G_diamonds = nx.from_pandas_edgelist(
    edges_diamonds, edge_attr=True, create_using=nx.DiGraph()
)
```

The trade network of each commodity is represented as a directed graph comprising countries (vertices) and trade relationships (edges), with the edges starting from the export countries and pointing to the import countries. Each edge consists of two attributes - value of the trade and the quantity of the traded commodity, that can act as weights for the edges.

+++

## Introduction

+++

Before we begin with the analysis, it is important to answer the following question -

<i><b>Why do we want to look at international trade data using Network Analysis?</b></i>

Network analysis offers a unique perspective on international trade data, focusing on the interrelationships between countries rather than individual statistics. It considers the structural dimension, accounting for the influence of other countries in trade relations.

In general, the <i>effect of others</i> could be reduced eventually to the <i>average effect of others</i>. In that case, the implicit assumption is that the peers are somehow homogeneous, so that the mean is a meaningful central statistic of the distribution of peers characteristics.

However, this is generally not the case in social networks, which are instead characterized by a high degree of heterogeneity and a power law distribution of the topological properties of the network’s nodes.

Let us look at the trade network of coffee to understand this further.

```{code-cell} ipython3
# power-law distribution
outdeg_dict = nx.out_degree_centrality(G_coffee)
outdeg_dict = dict(sorted(outdeg_dict.items(), key=lambda item: item[1], reverse=True))
plt.figure(figsize=(25, 10))
plt.plot(outdeg_dict.keys(), outdeg_dict.values(), marker="o", linestyle="-", color="b")
plt.show()
```

It can be seen that this trade network is heterogenous with a power-law distribution of outdegree centrality which implies that the majority of global trade is dominated by a few countries, while many others have limited trade activities.

This finding hughlights the importance of understanding the role of key players and hubs in the trade network for overall economic stability and resilience. It also helps build an understanding about economic inequality and the potential impacts of trade disruptions on less connected countries.

+++

## Visualizing World Trade

+++

### Geographic View

+++

A quite natural visualization of trade flows is through the use of a cartogram and arrows linking countries or geographical areas. In the following section we plot a geographic view of the world trade network of Natural Gas.

```{code-cell} ipython3
# function for visualization of trade network
# parameter "geo" determines whether it will be a geographic or topological view
# default value of "geo" is False i.e. default view is topological


def draw_pretty(G, geo=False):
    indeg_dict = nx.in_degree_centrality(G)
    outdeg_dict = nx.out_degree_centrality(G)
    low, *_, high = sorted(indeg_dict.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    nsize = [x * 20000 for x in outdeg_dict.values()]
    plt.figure(figsize=(40, 20))
    lat_long = {
        i: [a, b]
        for i, a, b in zip(
            country_locations.country, country_locations.long, country_locations.lat
        )
    }
    if geo:
        postemp=lat_long
        latitudes = [lat_long[country][1] for country in lat_long]
        longitudes = [lat_long[country][0] for country in lat_long]
        if(importBasemap):
            m = Basemap(projection='merc',llcrnrlon=-180,llcrnrlat=-80,urcrnrlon=180, urcrnrlat=80, lat_ts=0, resolution='l',suppress_ticks=True)
            m.drawcountries(linewidth = 1.5)
            m.drawstates(linewidth = 0.1)
            m.drawcoastlines(linewidth=1.5)
            longitudes, latitudes = m(longitudes, latitudes)
        pos = {}
        for count, (key, value) in enumerate(postemp.items()):
            if(key in G.nodes):
                pos[key] = (longitudes[count], latitudes[count])
    else:
        pos=nx.spring_layout(G, seed=1231)
    nx.draw(G, pos, with_labels=True, node_size=nsize, node_color=[mapper.to_rgba(i) for i in indeg_dict.values()], alpha = 0.7)
    plt.show()
```

In this visualization, by definition, the distance between countries in the network represents their geographical distance. As the color gradient of node moves from blue to red, the in degree centrality of that node becomes higher. This means that nodes that import from large number of countries will have a redder color. Whereas the nodes with bigger size are large exporters.

```{code-cell} ipython3
draw_pretty(G_natural_gas, geo=True)
```

The picture is efficient in showing the intensity of trade links between some countries and continents, highlighting some significant trends: 

- Asian countries like China, Korea, Singapore, Thailand, India and Japan are importers of Natural Gas from a large number of countries.
- USA is an exporter of Natural Gas to a large number of countries, and it also imports from a significant number of countries.
- Whereas Russia is a large exporter, but does not import from a lot of countries.
- There are large number of exporters in the European and African continent. European countries like France, Great Britain and Italy are also significant importers.

<b><i>While geographic visualization of international trade provides valuable insights into spatial patterns and regional concentrations of economic activities, it has its limitations when it comes to analyzing the interdependencies among countries. </i></b>

+++

To see why, let’s proceed with the following thought experiment.

Let’s imagine that we delete an arc from the above figure: the link between Russia (RUS) and Japan (JAP), for example. Nothing special will happen to the whole picture. Just the circle corresponding to the Russia would become marginally smaller and Japan will become less red, but from a structural point of view the rest of the picture will remain unaltered: the position of countries, being fixed by geography, is spatially unaffected, and so is the position of the other edges in the picture. 

Basically, the other countries’ trade is unaffected by the sudden loss of Russian exports to Japan.

Instead, if we want countries’ interactions to be accounted in determining the relative position of each country in the whole trading system, we should get rid of the constraint imposed by a geographical representation of international trade and move from physical space to topological space.

+++

### Topological View

+++

The use of force-directed algorithms overcome these limitations and offers a more comprehensive view of the global trade system. 

By adopting a topological view rather than a geographical one, we shift our focus from the spatial proximity of countries to the structural relationships within the entire trading system. The force-directed algorithm acts as a virtual spring system, where countries connected by trade links tend to be closer, and those with limited trade relations are positioned farther apart. This placement considers not only the direct bilateral connections but also the indirect effects of each country's trade partners on its position in the network.

Thus, it allows us to understand how a country's role in the global trade network is influenced not only by its direct trade partners but also by the behavior and position of its partners' partners, and so on. This concept is known as "structural interdependence," which means that the overall network structure affects individual countries' trade relationships.

```{code-cell} ipython3
draw_pretty(G_natural_gas, geo=False)
```

Now, when we remove the trade link between Russia and Japan, we can observe changes in the positioning of the nodes. The most noticeable change is the leftward shift of Russia in the figure. It now becomes closer to Italy, Sweden and the USA. This perspective allows us to analyze the ripple effects of changes in trade relationships and explore how disruptions or shifts in one part of the network might influence trade dynamics globally.

```{code-cell} ipython3
# removing trade link between Russia and Japan
G_natural_gas.remove_edge("RUS", "JPN")
draw_pretty(G_natural_gas, geo=False)
```

## Centrality Measures

+++

Centrality measures are very useful in comparing the roles of nodes within the network. In this tutorial, we will focus on degree, closeness, and betweenness centralities. The measures of centrality assess how influential a country is within the international trading system as a whole. Since there are different interpretations of each centrality criterion in a network, we should evaluate nodes on different criteria.

The number of incoming connection to a node is referred to as the "indegree" in directed networks, whereas the number of outbound connection from the node is referred to as the "outdegree." 

Closeness centrality is an indicator of the distance of a node from other nodes (in terms of topological distance) and measures how easily a node can be reached by other nodes. The closeness centrality of a nation in the trade network relates to how much it is impacted by other countries and how much it is affected by other countries.

In betweenness centrality, the location of the node in the network is more essential than the number of nodes linked. It indicates how important a country is in terms of connecting other countries. Countries having a high betweenness centrality operate as a commercial bridge with other countries in the trade network. Betweenness centrality therefore quantifies the extent to which a certain node operates as an intermediate or gatekeeper in the network.

```{code-cell} ipython3
total_outgoing_weight = {
    node: sum(
        data["value"] / 1000000 for _, _, data in G_coffee.out_edges(node, data=True)
    )
    for node in G_coffee
}

closeness = nx.closeness_centrality(G_coffee)
betweenness = nx.betweenness_centrality(G_coffee)
indegree = nx.in_degree_centrality(G_coffee)
outdegree = nx.out_degree_centrality(G_coffee)
```

```{code-cell} ipython3
# combining both dicts into one dataframe
df1 = pd.DataFrame(indegree.items(), columns=["country", "indegree"])
df2 = pd.DataFrame(outdegree.items(), columns=["country", "outdegree"])
df3 = pd.DataFrame(closeness.items(), columns=["country", "closeness"])
df4 = pd.DataFrame(betweenness.items(), columns=["country", "betweenness"])
df5 = pd.DataFrame(total_outgoing_weight.items(), columns=["country", "export_value"])
merged_df = pd.merge(df1, df2, on="country", how="inner")
merged_df = pd.merge(merged_df, df3, on="country", how="inner")
merged_df = pd.merge(merged_df, df4, on="country", how="inner")
merged_df = pd.merge(merged_df, df5, on="country", how="inner")

merged_df.sort_values(by=["export_value"], inplace=True, ascending=False)

with pd.option_context(
    "display.max_rows",
    None,
    "display.max_columns",
    None,
):
    print(merged_df)
```

From the above table, we can draw several insights about the world trade network of coffee:

1. Brazil (BRA) stands out as the biggest exporter of coffee, having high outdegree and export value. But, its indegree, betweenness and closeness values are all zero. This means that Brazil does not import coffee from other countries and is not closely connected in overall network.


2. Colombia (COL), Vietnam (VNM) and Ethiopia (ETH) are other major exporters of coffee in the world trade.


3. Other notable players include Germany (DEU), the United States (USA), and Italy (ITA), which have high indegree, outdegree, and centrality values, implying that they may act as important intermediaries in the coffee trade network.


4. Some countries have low indegree, outdegree, and centrality values, indicating they have limited involvement in the coffee trade network. Examples include Mauritania (MRT), Chad (TCD), and Luxembourg (LUX).

+++

## Community Detection

+++

Community analysis is used to decompose clusters of highly connected nodes into several relatively independent modules. The modularity measure is employed to assess the density of connections within communities compared to links between communities. 

Here, we detect communities in the trade network of Diamonds such that the modularity measure is maximised. The determination of community structures gives a clue to us whether there is also regionalization.

```{code-cell} ipython3
community = nx.community.greedy_modularity_communities(G_diamonds)

# function to create node colour list


def create_community_node_colors(graph, communities):
    number_of_colors = len(communities[0])
    colors = [
        "#D4FCB1",
        "#CDC5FC",
        "#FFC2C4",
        "#F2D140",
        "#F57160",
        "#2894F5",
        "#577D32",
    ][:number_of_colors]
    node_colors = []
    for node in graph:
        current_community_index = 0
        for community in communities:
            if node in community:
                node_colors.append(colors[current_community_index])
                break
            current_community_index += 1
    return node_colors


# function to plot graph with node colouring based on communities
def visualize_communities(graph, communities):
    node_colors = create_community_node_colors(graph, communities)
    # Calculate the total incoming weight for each node
    total_incoming_weight = {
        node: sum(data["value"] for _, _, data in graph.out_edges(node, data=True))
        for node in graph
    }
    # Get the maximum and minimum incoming weight values
    max_weight = max(total_incoming_weight.values())
    min_weight = min(total_incoming_weight.values())
    # Normalize the incoming weights to the desired node size range
    normalized_weights = {
        node: 10
        + ((total_incoming_weight[node] - min_weight) / (max_weight - min_weight)) * 90
        for node in graph
    }
    pos = {
        i: [a, b]
        for i, a, b in zip(
            country_locations.country, country_locations.long, country_locations.lat
        )
    }
    nx.draw(
        graph,
        pos=pos,
        node_size=[100 * normalized_weights[node] for node in graph],
        node_color=node_colors,
        with_labels=True,
        font_size=15,
        font_color="black",
        alpha=0.8
    )


plt.figure(figsize=(30, 20))
visualize_communities(G_diamonds, community)
plt.show()
```

In the above picture, each color symbolizes a different community. The size of node of each country is based on the total export value of that country.

We can draw several insights and potential relations in the way these countries are grouped into communities:

1. <b>Geographic Proximity:</b> The above picture provides a geographic view of the network, from which it is evident that some of the communities are grouped based on geographic proximity. For example, community of mainly European countries or the community of many Asian countries like China, Hong Kong, Indonesia, Singapore, and others. This suggests that countries in close geographic proximity have more significant trade ties within their respective communities.

2. <b>Economic Development:</b> Another possible grouping factor could be economic development. The largest community includes a mix of developed countries like the United States, Australia, and the United Kingdom, along with developing nations like India and South Africa that have significant influence on the global stage.

3. <b>Trading Partnerships:</b> Countries within a community may have stronger trading partnerships with each other compared to those outside the community. For instance, countries in the community that includes China, Hong Kong, Indonesia, Singapore, and others, may have established significant trade connections within the Asian region.

4. <b>Political or Cultural Ties:</b> Some communities might have formed due to political or cultural ties. For instance, the community consisting of countries like Armenia, Belarus, Kazakhstan, and Russia, were part of the former Soviet Union. Similarly, the community that includes Azerbaijan and Turkey, which share historical and cultural connections. This suggests that shared history, language, or culture could be contributing to the grouping of countries.

Since the size of the country is based on the values of exports from that country, we can also conclude that Canada, South Africa, Myanmar, Hong Kong and Great Britain are some of the largest exporters of diamonds in the world.

+++

## Conclusion

+++

This tutorial only scrapes the surface when using network analysis to study World Trade. One could go on to analyze different product categories, choose to focus only on a subset of countries (such as the BRICS, WTO etc.) or even incorporate a temporal dimension by comparing trade networks over the years. You could also choose to investigate how the trade network changes during major economic phenomenon, such as entrance of China in WTO, opening up of Indian economy in 1991 or the effects of the COVID-19 pandemic.

+++

## References:

1. [Network Analysis of World Trade using the BACI-CEPII dataset](https://re.public.polimi.it/retrieve/e0c31c0f-23b0-4599-e053-1705fe0aef77/Network%20Analysis%20of%20World%20Trade%20using%20the%20BACI-CEPII%20dataset_11311-862168_Tajoli.pdf)
2. https://wits.worldbank.org/trade/country-byhs6product.aspx?lang=en
3. http://snap.stanford.edu/class/cs224w-2016/projects/cs224w-21-final.pdf
4. https://www.eief.it/files/2010/10/luca-de-benedictis.pdf
5. https://repositorio.cepal.org/bitstream/handle/11362/45060/1/S1901067_en.pdf
6. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9589650/
