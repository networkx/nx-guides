---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3
    name: python3
---

<!-- #region id="QqmEP19zFVew" -->
# Contributors Guide (DRAFT)
<!-- #endregion -->

<!-- #region id="lUOvQg1MGRIo" -->
## A Brief Roadmap for First-time Contributors

If you want to contribute to nx-guides and already decided on an algorithm to work on, here is a simple roadmap you can follow:

1.   Clone `nx-guides` repository to your local machine.
2.   Create a folder with the name of your algorithm under `nx-guides/content/algorithms`.
3.   Create your markdown notebook under the folder you created in Step 2.
4.  Create images and data folders under the folder you created in Step 2. If you use any static images and data, please put them under corresponding folders. (Optional)
5.   Add your notebook's path to index.md file under `nx-guides/content/algorithms`.
6.  When you complete your work and feel ready, push your changes to the repository and open a PR for review.
<!-- #endregion -->

<!-- #region id="4dKrGBiRIhYZ" -->
## Some Tips
<!-- #endregion -->

<!-- #region id="vt0xsWsIDA1K" -->
### 1. Your notebook should be a `.md` file.

Your notebook should be in markdown notebook format. 

If you normally use `.ipynb` notebooks to work on, you can convert them to `.md` using the following `jupytext` command:

```
jupytext --to markdown <notebook-name>.ipynb
```


<!-- #endregion -->

<!-- #region id="XByALcTUDm1X" -->
### 2. Use code-generated images as much as possible.

Showing how to make high-quality visualizations of graph/network data is one of the primary goals of nx-guides tutorials! For this, images (especially graph visualizations) should be generated directly by code in the notebook as much as possible.

If you also prefer to include static images to your notebook, you 
<!-- #endregion -->

<!-- #region id="buq5ho4UDwLw" -->
### 3. Add requirements to ```requirements.txt```

If you prefer to install and use other libraries, add related requirements to ```requirements.txt``` under ```nx-guides``` repository. (I.e. Do not install requirements using ```pip install``` command in your notebook.)
<!-- #endregion -->

<!-- #region id="39L-DjZREctA" -->
### 4. User input is not supported yet.

Our notebooks do not support getting input from the reader yet. Although it is an idea we consider for future, please keep narrative notebooks for now.
<!-- #endregion -->

<!-- #region id="6TqY5A99JgXc" -->
### 5. Do not forget to add path of your notebook to `index.md`.

You should include the path of your notebook in index.md file under `nx-guides/content/algorithms`.
<!-- #endregion -->

<!-- #region id="o8wvepdRKPFK" -->
### 6. Header Levels

Header levels should be incremented one by one. If you jump from level 2 to level 4 header, for example, msyt will produce an error to prevents you from passing the tests. In this example, if the current header level is 2, the following header level needs to be either 2 or 3.
<!-- #endregion -->

<!-- #region id="sHw3aPpOKfJU" -->
### 7. You do not need to implement the algorithm in the same exact way as done inside NetworkX.

The goal of nx-guides is to provide a pedagogical source for NetworkX algorithms. For this, you do not have to include source code of the algorithm as it is under NetworkX. If possible, feel free to remove bits that you think can be better compressed :)
<!-- #endregion -->

<!-- #region id="78u0INXfL47X" -->
### 8. Feel free to use real-world datasets

One of the aims of nx-guides notebooks is to use different algorithms to explore and analyse real world datasets. Feel free to use them if you believe it is useful.

Here is a good source for datasets:

http://snap.stanford.edu/data/index.html
<!-- #endregion -->
