---
jupytext:
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  name: python3
---

# Contributors Guide

## A Brief Roadmap for First-time Contributors

The goal of nx-guides is to provide pedagogical notebooks about graph theory, network analysis, and NetworkX implementations (algorithms, etc.). This is a great place to get started with open source contribution!


If you want to contribute to nx-guides and already decided on a topic to work on, here are next steps:

1. Clone `nx-guides` repository to your local machine.
2. Add your markdown notebook to the appropriate folder (i.e. if you are adding a new algorithm, add a folder with its name in `nx-guides/content/algorithms` following the structure of the other algorithms).
3. Ensure you notebook fits the Format Guidelines in this document.
4. Use subdirectories for images and data. If you use any static images and data, please put them under corresponding folders. (optional)
5. Add your notebook's path to the index.md file.
6. When you complete your work and feel ready, push your changes to the repository and open a PR for review. 
7. Engage in any discussion about your changes. Be sure to clearly communicate your thoughts.
 

## Some Tips

### 1. Your notebook should be a `.md` file.

Your notebook should be in MyST markdown format (See: https://myst-parser.readthedocs.io/en/latest/index.html). 

If you normally use `.ipynb` notebooks to work on, you can convert them to `.md` using the following `jupytext` command:

```
jupytext  --to md:myst <notebook-name>.ipynb
```

### 2. Use code-generated images as much as possible.

Showing how to make high-quality visualizations of graph/network data is one of the primary goals of nx-guides tutorials! For this, images (especially graph visualizations) should be generated directly by code in the notebook as much as possible.

If you also prefer to include static images to your notebook, you 

### 3. Add requirements to ```requirements.txt```

If you prefer to install and use other libraries, add related requirements to ```requirements.txt``` under ```nx-guides``` repository. (I.e. Do not install requirements using ```pip install``` command in your notebook.)

### 4. User input is not supported yet.

Our notebooks do not support getting input from the reader yet. Although it is an idea we consider for future, please keep narrative notebooks for now.

### 5. Do not forget to add path of your notebook to `index.md`.

You should include the path of your notebook in index.md file under `nx-guides/content/algorithms`.

### 6. Header Levels

Header levels should be incremented one by one. If you jump from level 2 to level 4 header, for example, msyt will produce an error to prevents you from passing the tests. In this example, if the current header level is 2, the following header level needs to be either 2 or 3.

### 7. You do not need to implement the algorithm in the same exact way as done inside NetworkX.

nx-guides provides a pedagogical source for NetworkX algorithms. For this, you do not have to include source code of the algorithm as it is under NetworkX. If possible, feel free to remove bits that you think can be better compressed :)

### 8. Feel free to use real-world datasets

One of the aims of nx-guides notebooks is to use different algorithms to explore and analyse real world datasets. Feel free to use them if you believe it is useful.

Here is a good source for datasets:

http://snap.stanford.edu/data/index.html

### 9. What if the tests are still failing?

Once all tests are completed, you can see warnings and errors that prevents your PR from passing the tests. To do that, go to the bottom of "Conversation" page in your PR. There will be red cross signs on the left side of "ci/circleci: build-docs" test suite. Click on the "Details" link on the right side of it to see errors and warnings.

You can also click on the "Details" link on the right side of "ci/circleci: build-docs artifact". If your notebook is built, this will bring you to the full documentation for the project as if this branch was merged. You can then navigate to the notebook you have created and check that your documentation looks good.

### Environment

A good way to go about editing your markdown file is with Jupyter Notebook or other markdown file editors. Just make sure the metadata fits that of the other markdown files in nx-guides. 

## Format Guidelines

1. Write a clear title.
2. When introducing your topic, reference what problem you are solving and what part of NetworkX you are using.
3. Include an "import packages" section at the top of the notebook after your introduction.
Add all import statements for packages in a code cell underneath your introduction (see other notebooks for examples)
4. Comment code heavily, especially confusing sections. 
5. Cite all sources. Include in-text references and a references section at the bottom of the document.
For examples of how to write these references and cite, see other notebooks
