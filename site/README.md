# Notebook-based sphinx site via `myst-nb`

This material in this directory comprises a sphinx site generated from the
Jupyter notebooks in `../notebooks`.
Sphinx generates the static site from the source `.ipynb` files via the 
[myst-nb](https://myst-nb.readthedocs.io/en/latest/) extension, which also
supports MyST-markdown and a text-based Jupyter `.md` notebook file format
(not used here).

## To build

1. Follow the instructions in the main README to install the necessary 
   dependencies for running the notebooks.
2. `pip install -r site/requirements.txt`
3. `cd site && make html`

The generated static site can then be viewed locally via, e.g.
`firefox _build/html/index.html`
