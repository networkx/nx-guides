<div class="cell markdown">

# Distance Measures in Networkx

Distance measures are used in physical cosmology to give a natural
notion of the distance between two objects or eventsin the universe.
They are often used to tie some observable quantity to another quantity
that is not directly observable, but is more convenient for calculation.

In a graph we look at distance when it comes to connected graph. In case
of a disconnected graph (G) and vertex A and B are in different
components we say that the distance between A and B is infinity. We will
be looking at different aspect of distance when it comes to graph.

</div>

<div class="cell code" data-execution_count="112">

``` python
import networkx as nx
import matplotlib.pyplot as plt
```

</div>

<div class="cell markdown">

## Eccentricity

It is defined as the maximum distance of one vertex from other
vertex.The maximum distance between a vertex to all other vertices is
considered as the eccentricity of the vertex. It is denoted by e(V).

<br><br> The eccentricity is very important factor, from the
eccentricity of different vertices we can get the radius, diameter,
center and periphery.

</div>

<div class="cell code" data-execution_count="113">

``` python
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (6, 8), (6,9), (8,9)])
nx.draw(G, with_labels = "True")
```

<div class="output display_data">

![](675c49d72b8a67494ffbf9e21d8131dded4e9018.png)

</div>

</div>

<div class="cell code" data-execution_count="114">

``` python
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (6, 8), (6,9), (8,9)])
dict(nx.eccentricity(G))
```

<div class="output execute_result" data-execution_count="114">

    {1: 4, 2: 3, 3: 3, 4: 4, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4}

</div>

</div>

<div class="cell markdown">

The eccentricity Of G which was returned shows the maximum distance of
one node to another. Let's examine the case of node 1.

Eccentricity of node 1, it's maximum distance will be leaving from
(1-2,3-6,6-9) or (1-2, 5-6, 6-8) which gives a maximum distance of 4.
so, <br> <br> e(1) = 4

</div>

<div class="cell markdown">

nx.eccentricity(G) returns all the nodes in our Graph along as it's
eccentricity. Nevertheless, we can always precise the nodes with want.

</div>

<div class="cell code" data-execution_count="115">

``` python
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (6, 8), (6,9), (8,9)])
dict(nx.eccentricity(G, v=[1, 6])) # This returns the eccentrity of node 1 and 6 only
```

<div class="output execute_result" data-execution_count="115">

    {1: 4, 6: 3}

</div>

</div>

<div class="cell markdown">

## Diameter

The diameter of a graph is the maximum eccentricity of any vertex in the
graph. That is, it is the greatest distance between any pair of
vertices. To find the diameter of a graph, first find the shortest path
between each pair of vertices. The greatest length of any of these paths
is the diameter of the graph.

</div>

<div class="cell markdown">

Diameter is the maximum eccentricity, if we look at the eccentricity of
the graph below, the overall maximum eccentricity is 3 and hence the
diameter.

</div>

<div class="cell code" data-execution_count="116">

``` python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.eccentricity(G)
```

<div class="output execute_result" data-execution_count="116">

    {1: 3, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3}

</div>

</div>

<div class="cell code" data-execution_count="117">

``` python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])

color_map = []
for node in G:
    if node == (nx.diameter(G)):
        color_map.append('yellow')
    else:
        color_map.append('purple')
nx.draw(G, node_color=color_map, with_labels="True")
```

<div class="output display_data">

![](89b05ae0ef8fb43c77888250c7d78eba16f0f8eb.png)

</div>

</div>

<div class="cell markdown">

## Periphery

The Periphery has nodes, with eccentricity equal to the diameter. It
denotes a sparsely connected, usally non-central set of nodes, which are
linked to the core. <br> <br> Therfore, <br> e(V) = diameter(G) gives
the periphery

</div>

<div class="cell code" data-execution_count="118">

``` python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.periphery(G)
```

<div class="output execute_result" data-execution_count="118">

    [1, 4, 5, 6]

</div>

</div>

<div class="cell markdown">

## Radius

The radius of a graph is the minumum graph eccentricity of any graph
vertex in a graph. This holds for a connected graph. For a disconnected
graph there is an infinite radius. The radius is also called the
smallest eccentricity in a graph.

</div>

<div class="cell code" data-execution_count="119">

``` python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.radius(G)
```

<div class="output execute_result" data-execution_count="119">

``` 
2
```

</div>

</div>

<div class="cell code" data-execution_count="120">

``` python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
color_map = []
for node in G:
    if node == (nx.radius(G)):
        color_map.append('yellow')
    else:
        color_map.append('purple')
nx.draw(G, node_color=color_map, with_labels="True")
```

<div class="output display_data">

![](3d6fe3346273bc0c4a5bb39db49e88713682e1f6.png)

</div>

</div>

<div class="cell markdown">

## Center

The center of a graph is the set of all vertices of minimum
eccentricity,that is, the set of all vertices u where the greatest
distance d(u,v) to other vertices v is minimal. Equivalently, it is the
set of vertices with eccentricity equal to the graph's radius.

</div>

<div class="cell markdown">

e(v) = radius(G) then v is the central node and the set of all such
nodes makes the center of G

</div>

<div class="cell code" data-execution_count="121">

``` python
import networkx as nx
G = nx.Graph([(1, 2), (2, 3), (3, 4), (2,5), (3,6), (5, 6),(5,7), (7, 8), (6, 9)])
list(nx.center(G))
```

<div class="output execute_result" data-execution_count="121">

    [2, 5, 6]

</div>

</div>

<div class="cell code" data-execution_count="122">

``` python
G = nx.Graph([(1, 2), (2, 3), (2, 4), (3,5), (3, 6)])
nx.center(G)
```

<div class="output execute_result" data-execution_count="122">

    [2, 3]

</div>

</div>

<div class="cell markdown">

## Barycenter

The barycenter is the center of mass of two or more bodies that orbit
one another and is the point about which the bodies orbit. Did you know
the barycenter is sometimes called the median.

</div>

<div class="cell code" data-execution_count="123">

``` python
G = nx.Graph([(0, 1), (1, 2), (1, 5), (5, 4), (2, 4), (2, 3), (4, 3), (3, 6)])
nx.barycenter(G)
```

<div class="output execute_result" data-execution_count="123">

    [2]

</div>

</div>

<div class="cell markdown">

## Resistance Distance

In graph theory, the resistance distance between two vertices of a
simple connected graph, G, is equal to the resistance between two
equivalent points on an electrical network, constructed so as to
correspond to G, with each edge being replaced by a 1 ohm resistance. It
is a metric on graphs.

</div>

<div class="cell code" data-execution_count="124">

``` python
G = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4), (5, 4), (5, 3), (4, 1), (3, 6)])
nx.resistance_distance(G, 3, 5)
```

<div class="output execute_result" data-execution_count="124">

    0.625

</div>

</div>

<div class="cell markdown">

## Extrema Bounding

We can use the extrema bounding to calculate the diameter, radius,
center, eccentricity , barycenter and periperal

</div>

<div class="cell code" data-execution_count="125">

``` python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="diameter")
```

<div class="output execute_result" data-execution_count="125">

``` 
3
```

</div>

</div>

<div class="cell code" data-execution_count="126">

``` python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="radius")
```

<div class="output execute_result" data-execution_count="126">

``` 
2
```

</div>

</div>

<div class="cell code" data-execution_count="127">

``` python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="center")
```

<div class="output execute_result" data-execution_count="127">

    [1, 2]

</div>

</div>

<div class="cell code" data-execution_count="128">

``` python
G = nx.path_graph(4)
nx.extrema_bounding(G, compute="periphery")
```

<div class="output execute_result" data-execution_count="128">

    [0, 3]

</div>

</div>

<div class="cell code" data-execution_count="4">

``` python
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
facebook = pd.read_csv('amazon0302.txt.gz',  sep=' ')
facebook
```

<div class="output error" data-ename="FileNotFoundError" data-evalue="[Errno 2] No such file or directory: &#39;amazon0302.txt.gz&#39;">

    ---------------------------------------------------------------------------
    FileNotFoundError                         Traceback (most recent call last)
    /home/anne/Documents/Projects/outreachy/2022-round-1/Lukong123/distance_measures.ipynb Cell 31' in <cell line: 6>()
          <a href='vscode-notebook-cell:/home/anne/Documents/Projects/outreachy/2022-round-1/Lukong123/distance_measures.ipynb#ch0000030?line=3'>4</a> import matplotlib.pyplot as plt
          <a href='vscode-notebook-cell:/home/anne/Documents/Projects/outreachy/2022-round-1/Lukong123/distance_measures.ipynb#ch0000030?line=4'>5</a> from random import randint
    ----> <a href='vscode-notebook-cell:/home/anne/Documents/Projects/outreachy/2022-round-1/Lukong123/distance_measures.ipynb#ch0000030?line=5'>6</a> facebook = pd.read_csv('amazon0302.txt.gz',  sep=' ')
          <a href='vscode-notebook-cell:/home/anne/Documents/Projects/outreachy/2022-round-1/Lukong123/distance_measures.ipynb#ch0000030?line=6'>7</a> facebook
    
    File ~/.local/lib/python3.8/site-packages/pandas/util/_decorators.py:311, in deprecate_nonkeyword_arguments.<locals>.decorate.<locals>.wrapper(*args, **kwargs)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=304'>305</a> if len(args) > num_allow_args:
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=305'>306</a>     warnings.warn(
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=306'>307</a>         msg.format(arguments=arguments),
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=307'>308</a>         FutureWarning,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=308'>309</a>         stacklevel=stacklevel,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=309'>310</a>     )
    --> <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/util/_decorators.py?line=310'>311</a> return func(*args, **kwargs)
    
    File ~/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py:680, in read_csv(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, squeeze, prefix, mangle_dupe_cols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, error_bad_lines, warn_bad_lines, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=664'>665</a> kwds_defaults = _refine_defaults_read(
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=665'>666</a>     dialect,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=666'>667</a>     delimiter,
       (...)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=675'>676</a>     defaults={"delimiter": ","},
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=676'>677</a> )
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=677'>678</a> kwds.update(kwds_defaults)
    --> <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=679'>680</a> return _read(filepath_or_buffer, kwds)
    
    File ~/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py:575, in _read(filepath_or_buffer, kwds)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=571'>572</a> _validate_names(kwds.get("names", None))
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=573'>574</a> # Create the parser.
    --> <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=574'>575</a> parser = TextFileReader(filepath_or_buffer, **kwds)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=576'>577</a> if chunksize or iterator:
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=577'>578</a>     return parser
    
    File ~/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py:933, in TextFileReader.__init__(self, f, engine, **kwds)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=929'>930</a>     self.options["has_index_names"] = kwds["has_index_names"]
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=931'>932</a> self.handles: IOHandles | None = None
    --> <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=932'>933</a> self._engine = self._make_engine(f, self.engine)
    
    File ~/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py:1217, in TextFileReader._make_engine(self, f, engine)
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1212'>1213</a>     mode = "rb"
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1213'>1214</a> # error: No overload variant of "get_handle" matches argument types
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1214'>1215</a> # "Union[str, PathLike[str], ReadCsvBuffer[bytes], ReadCsvBuffer[str]]"
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1215'>1216</a> # , "str", "bool", "Any", "Any", "Any", "Any", "Any"
    -> <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1216'>1217</a> self.handles = get_handle(  # type: ignore[call-overload]
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1217'>1218</a>     f,
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1218'>1219</a>     mode,
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1219'>1220</a>     encoding=self.options.get("encoding", None),
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1220'>1221</a>     compression=self.options.get("compression", None),
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1221'>1222</a>     memory_map=self.options.get("memory_map", False),
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1222'>1223</a>     is_text=is_text,
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1223'>1224</a>     errors=self.options.get("encoding_errors", "strict"),
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1224'>1225</a>     storage_options=self.options.get("storage_options", None),
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1225'>1226</a> )
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1226'>1227</a> assert self.handles is not None
       <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/parsers/readers.py?line=1227'>1228</a> f = self.handles.handle
    
    File ~/.local/lib/python3.8/site-packages/pandas/io/common.py:714, in get_handle(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=710'>711</a>     assert isinstance(handle, str)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=711'>712</a>     # error: Incompatible types in assignment (expression has type
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=712'>713</a>     # "GzipFile", variable has type "Union[str, BaseBuffer]")
    --> <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=713'>714</a>     handle = gzip.GzipFile(  # type: ignore[assignment]
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=714'>715</a>         filename=handle,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=715'>716</a>         mode=ioargs.mode,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=716'>717</a>         **compression_args,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=717'>718</a>     )
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=718'>719</a> else:
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=719'>720</a>     handle = gzip.GzipFile(
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=720'>721</a>         # No overload variant of "GzipFile" matches argument types
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=721'>722</a>         # "Union[str, BaseBuffer]", "str", "Dict[str, Any]"
       (...)
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=724'>725</a>         **compression_args,
        <a href='file:///home/anne/.local/lib/python3.8/site-packages/pandas/io/common.py?line=725'>726</a>     )
    
    File /usr/lib/python3.8/gzip.py:173, in GzipFile.__init__(self, filename, mode, compresslevel, fileobj, mtime)
        <a href='file:///usr/lib/python3.8/gzip.py?line=170'>171</a>     mode += 'b'
        <a href='file:///usr/lib/python3.8/gzip.py?line=171'>172</a> if fileobj is None:
    --> <a href='file:///usr/lib/python3.8/gzip.py?line=172'>173</a>     fileobj = self.myfileobj = builtins.open(filename, mode or 'rb')
        <a href='file:///usr/lib/python3.8/gzip.py?line=173'>174</a> if filename is None:
        <a href='file:///usr/lib/python3.8/gzip.py?line=174'>175</a>     filename = getattr(fileobj, 'name', '')
    
    FileNotFoundError: [Errno 2] No such file or directory: 'amazon0302.txt.gz'

</div>

</div>
