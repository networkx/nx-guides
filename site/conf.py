# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'nx-guides'
copyright = '2022, NetworkX developers'
author = 'NetworkX developers'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
]

# MyST configuration
myst_heading_anchors = 2
myst_enable_extensions = ["dollarmath"]
# if `True` then a transition line(----) will be placed before any footnotes
myst_footnote_transition = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'
html_title = 'NetworkX Notebooks'
html_logo = '_static/networkx_banner.svg'
# html_favicon
html_theme_options = {
    "github_url": "https://github.com/networkx/nx-guides/",
    "repository_url": "https://github.com/networkx/nx-guides/",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "path_to_docs": "site/",
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for MyST-NB configuration -----------------------------------

# Bump up per cell execution timeout to 300 seconds (from default 30 seconds)
nb_execution_timeout = 300
nb_execution_show_tb = True  # Print tracebacks to stderr
