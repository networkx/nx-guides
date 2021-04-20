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

project = 'networkx-notebooks'
copyright = '2021, NetworkX developers'
author = 'NetworkX developers'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "networkx": ("https://networkx.org/documentation/stable", None),
}

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
html_theme = 'pydata_sphinx_theme'
html_title = 'NetworkX Notebooks'
html_logo = '_static/networkx_logo.svg'
# html_favicon
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/networkx/notebooks/",
            "icon": "fab fa-github-square",
        },
        {
            "name": "Binder",
            "url": "https://mybinder.org/v2/gh/networkx/notebooks/main?urlpath=lab/tree/content",
            "icon": "fas fa-rocket",
        },
    ],
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "networkx",
    "github_repo": "notebooks",
    "github_version": "main",
    "doc_path": "site",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
