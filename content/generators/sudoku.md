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
  version: 3.7.4
---

# Sudoku and Graph coloring

This notebook tries to help you understand the mathematics in the backdrop of the popular number placement puzzle -Sudoku. A Sudoku puzzle consists of a 9 x 9 grid of 81 cells. The objective is to fill the rest of the grid with digits from 1 to 9 such that no digit repeats within any row, column and speciﬁed 3 x 3 blocks.


```{code-cell} ipython3
import networkx as nx
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from random import sample
```

Informally the Sudoku graph is an undirected graph- its vertices represent the cells and edges represent pairs of cells that belong to the same row, column, or block of the puzzle. Formally this can be defined as:

> A Sudoku grid of rank $n$ is a $n^2 × n^2$ grid($X_n$) . It consists of $n^2$ disjoint $n × n$ grids. Graph of $X_n$, denoted as $GX_n$, is $(V, E)$ where cells of Sudoku grid form the vertices of its graph and two
cells are adjacent if they are either in the same row or column or block of $X_n$.

> $GX_n$ is a regular $(n^4, \frac{3n^6}{2} − n^5− \frac{n^4}{2})$ graph of degree $3n^2 − 2n − 1$  (1)

[Wikipedia Page - Sudoku Graph](https://en.wikipedia.org/wiki/Sudoku_graph)

Now, from (1) we can get that the graph of a Sudoku grid of rank 3 is a (81, 810) regular graph of degree 20. This can be verified informally- we have 81 cells in the standard sudoku where every cell is adjacent to 8 cells in its row + 8 cells in its column and 4 more leftover cells in its block, hence the degree 20.

Let's generate a random (filled) sudoku of rank n and then build further intuition


```{code-cell} ipython3
def generate_random_sudoku(n):
    rank  = n
    side  = rank*rank
    def pattern(row,col): return (rank*(row%rank)+row//rank+col)%side
    def shuffle(s): return sample(s,len(s))
    # generate random row and column indices
    rows  = [ x*rank + row for x in shuffle(range(rank)) for row in shuffle(range(rank)) ]
    cols  = [ x*rank + col for x in shuffle(range(rank)) for col in shuffle(range(rank)) ]

    numbers  = shuffle(range(1,rank*rank+1))

    board = [ [numbers[pattern(row,col)] for col in cols] for row in rows ]
    board = np.asarray(board)
    return board

# Now we can use the networkx generator for a sudoku graph `nx.sudoku_graph()`

```{code-cell} ipython3
G = nx.sudoku_graph(3)
```
Now here's the interesting part, we want to visualize all three different kinds of edge colors - for example red for the edges that belong to the same row, green for the edges that belong to the same column and blue for the edges that belong to the same block. Here's the code to do that, in this view we can see th three different edge colors as the three different ways two nodes can be adjacent in a sudoku graph. Observe that no edge connects the same two numbers, this is what it means to satisfy the constraints of a sudoku problem


```{code-cell} ipython3
def draw_sudoku(G, layout='grid'):
    """Return a sudoku graph with labeled nodes and colored edges.
    This visualization is a useful way to understand 
    Sudoku as a Graph coloring problem,
    where each number in the cells is a node and 
    two numbers being in the same row, column or box 
    is interpreted as an edge between their nodes.

    Parameters
    ----------
    G : Networkx Graph generated from nx.sudoku_graph()

    layout : preference of layout for positioning of nodes (default: grid, optional, type: string)
            grid - grid layout returns a sudoku like figure with nodes and edges instead of cells
            circle - circular layout returns concentric circles with the sudoku's graph, 
            it doesn't hold any special meaning, it is visually appealing to look at for n=3.
        

    Returns
    -------
    plot : Matplotlib plot or figure

    Examples
    --------
    >>> G = nx.sudoku_graph()
    >>> nx.draw_sudoku(G)

    """
    #the generator function we used earlier
    def generate_random_sudoku(n):
        base  = n
        side  = base*base
        def pattern(r,c): return (base*(r%base)+r//base+c)%side
        def shuffle(s): return sample(s,len(s)) 
        rBase = range(base) 
        rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,base*base+1))
        board=[]
        for r in rows:
            board += [nums[pattern(r,c)] for c in cols]
        return board

    # here we deduce n from the number of nodes, e.g. 81 nodes means n=3
    n = int(sqrt(sqrt(len(G.nodes()))))
    board = generate_random_sudoku(n)

    box_edges=[]
    row_edges=[]
    column_edges=[]
    
    # Now we want to separate the edges, we notice that if we create a $n^2 * n^2$ grid of the array [0,1..81] (nodes), then we can use some arithmetic(or algorithm if you would call it that) to get the indices of the nodes in the same row, column or box.

    l=[]
    for i in range(n):
        l.append((n*n)-i)
        l.append(i)
    
    for i,j in G.edges():
            val = abs(i-j)
            # Columns and rows are fairly straightforward -> 
            # quotient is same when divided by the total number of rows or column (n*n)
            if i//n*n==j//n*n:
                column_edges.append((i,j))
            # The difference between two nodes in the same row perfectly divides the total number of rows or columns (n*n)
            if val%n*n==0:
                row_edges.append((i,j))
            # Boxes are the tricky part, for indices of two nodes in the same box, they are in the form of n*n modulo 0 or n*n modulo 1... n*n modulo n or  n*n modulo n*n-0 or n*n # modulo n*n-1... n*n modulo n*n-n, using this logic we compute the array `l` which we match the remainders with. Additionally, the difference between two nodes in the # same box is $(n^2)*(n-1)+n$, I don't have a proof on my hand neither do I know of a reference, but it's based on logical inferences from the assumed structure of # networkx sudoku graph. For example let's consider the first box in a 9*9 sudoku, you can see that the first row of the box is [0,9,18,1,10,19,2,11,20], essentially the # difference of indices between two nodes in the same box can at the very maximum be $(n^2)*(n-1)+n-1$ or the two extreme diagonally across nodes (0, 20). 
            # Similar structure is followed for n=4, this is quite interesting and I'd be interested in a more theoretical understanding of this, as of now I think this is related # to the chromatic Polynomial of the numbers and because of the simple node indices used in networkx graph.

            if val%(n*n) in l and val<(n*n)*(n-1)+n:
                box_edges.append((i,j))

    # Here we choose the layout and pick positions accordingly

    if layout=='circular':
        pos=nx.circular_layout(G)
    if layout=='grid':
        pos = dict(zip(list(G.nodes()), nx.grid_2d_graph(n*n,n*n)))

    # We map the indices to actual sudoku board values 
    mapping = dict(zip(G.nodes(), board))
    
    # Time to plot!!
    plt.figure(1,figsize=(12,12)) 
    nx.draw(G, labels=mapping, pos=pos, with_labels=True, node_color='white')
    # Here we draw the edges with different colors
    nx.draw_networkx_edges(G,pos,edgelist=box_edges,width=2, alpha=0.5, edge_color="tab:red")
    nx.draw_networkx_edges(G,pos,edgelist=row_edges,width=2, alpha=0.5, edge_color="tab:green")
    nx.draw_networkx_edges(G,pos,edgelist=column_edges,width=2, alpha=0.5, edge_color="tab:blue")
    plt.show()

```

We couldn't see a lot of edges in the first figure because they fell on top of each other, this is perhaps a better view.


```{code-cell} ipython3
draw_sudoku(G, 'circular')
```

Is this the only way? can we do something more? yes! we can color the vertices and not edges, it's the same problem regardless.

> A k-coloring of a graph G is a vertex coloring that is an assignment of one of k possible colors to each vertex of G (i.e., a vertex coloring) such that no two adjacent vertices receive the same color.

How many colors would we need in this case? 9

Note: this is more than intuition, formally 9 is the chromatic number of a 2-distant coloring problem, you can learn more about it [here](https://mast.queensu.ca/~murty/sudoku-ams.pdf) !

Let's visualize this, we'll modify the drawing a little


```{code-cell} ipython3
#structure of the graph remains the same!
n = 3
G = nx.sudoku_graph(n)
pos = dict(zip(list(G.nodes()), nx.grid_2d_graph(n*n,n*n)))

# we map the nodes 1-9 to a colormap
mapping = dict(zip(G.nodes(), board.flatten()))
low, *_, high = sorted(mapping.values())
norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Pastel1)

plt.figure(1,figsize=(12,12))
nx.draw(G, pos, labels=mapping,node_size=1000,
        node_color=[mapper.to_rgba(i) for i in mapping.values()],
        with_labels=True)
#edges remain uncolored for the sake of visualization
nx.draw_networkx_edges(G,pos,edgelist=box_edges+row_edges+column_edges,width=2, alpha=0.5, )
plt.show()
```
