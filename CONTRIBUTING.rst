.. _contributor_guide:

Contributor Guide
=================

.. note::
   This document assumes some familiarity with contributing to open source
   scientific Python projects using GitHub pull requests. If this does not
   describe you, you may first want to see the `Contributing FAQ <https://github.com/networkx/networkx/blob/main/doc/developer/new_contributor_faq.rst>`_.

.. _dev_workflow:

Development Workflow
--------------------

1. If you are a first-time contributor:

   * Go to `https://github.com/networkx/nx-guides
     <https://github.com/networkx/nx-guides>`_ and click the
     "fork" button to create your own copy of the project.

   * Clone the project to your local computer::

      git clone git@github.com:your-username/nx-guides.git

   * Navigate to the folder networkx and add the upstream repository::

      git remote add upstream git@github.com:networkx/nx-guides.git

   * Now, you have remote repositories named:

     - ``upstream``, which refers to the ``nx-guides`` repository
     - ``origin``, which refers to your personal fork

   * Next, you need to set up your build environment.
     Here are instructions for two popular environment managers:

     * ``venv`` (pip based)

       ::

         # Create a virtualenv named ``nx-guides-dev`` that lives in the directory of
         # the same name
         python -m venv nx-guides-dev
         # Activate it
         source nx-guides-dev/bin/activate
         # Install main development and runtime dependencies of nx-guides
         pip install -r requirements.txt

     * ``conda`` (Anaconda or Miniconda)

       ::

         # Create a conda environment named ``nx-guides-dev``
         conda create --name nx-guides-dev
         # Activate it
         conda activate nx-guides-dev
         # Install main development and runtime dependencies of nx-guides
         conda install -c conda-forge --file requirements.txt

   * Finally, we recommend you use a pre-commit hook, which runs black when
     you type ``git commit``::

       pre-commit install

2. Develop your contribution:

   * Pull the latest changes from upstream::

      git checkout main
      git pull upstream main

   * Create a branch for the feature you want to work on. Since the
     branch name will appear in the merge message, use a sensible name
     such as 'bugfix-for-issue-1480'::

      git checkout -b bugfix-for-issue-1480

   * Commit locally as you progress (``git add`` and ``git commit``)

3. Submit your contribution:

   * Push your changes back to your fork on GitHub::

      git push origin bugfix-for-issue-1480

   * Go to GitHub. The new branch will show up with a green Pull Request
     button---click it.

   * If you want, post on the `mailing list
     <http://groups.google.com/group/networkx-discuss>`_ to explain your changes or
     to ask for review.

4. Review process:

   * Every Pull Request (PR) update triggers a set of `continuous integration
     <https://en.wikipedia.org/wiki/Continuous_integration>`_ services
     that check that the code is up to standards and passes all our tests.
     These checks must pass before your PR can be merged.  If one of the
     checks fails, you can find out why by clicking on the "failed" icon (red
     cross) and inspecting the build and test log.

   * Reviewers (the other developers and interested community members) will
     write inline and/or general comments on your PR to help
     you improve its implementation, documentation, and style.  Every single
     developer working on the project has their code reviewed, and we've come
     to see it as friendly conversation from which we all learn and the
     overall code quality benefits.  Therefore, please don't let the review
     discourage you from contributing: its only aim is to improve the quality
     of project, not to criticize (we are, after all, very grateful for the
     time you're donating!).

   * To update your PR, make your changes on your local repository
     and commit. As soon as those changes are pushed up (to the same branch as
     before) the PR will update automatically.

   .. note::

      If the PR closes an issue, make sure that GitHub knows to automatically
      close the issue when the PR is merged.  For example, if the PR closes
      issue number 1480, you could use the phrase "Fixes #1480" in the PR
      description or commit message.


Divergence from ``upstream main``
---------------------------------

If GitHub indicates that the branch of your Pull Request can no longer
be merged automatically, merge the main branch into yours::

   git fetch upstream main
   git merge upstream/main

If any conflicts occur, they need to be fixed before continuing.  See
which files are in conflict using::

   git status

Which displays a message like::

   Unmerged paths:
     (use "git add <file>..." to mark resolution)

     both modified:   file_with_conflict.txt

Inside the conflicted file, you'll find sections like these::

   <<<<<<< HEAD
   The way the text looks in your branch
   =======
   The way the text looks in the main branch
   >>>>>>> main

Choose one version of the text that should be kept, and delete the
rest::

   The way the text looks in your branch

Now, add the fixed file::


   git add file_with_conflict.txt

Once you've fixed all merge conflicts, do::

   git commit

.. note::

   Advanced Git users may want to rebase instead of merge,
   but we squash and merge PRs either way.


Guidelines
----------

* All code should have tests.
* All code should be documented, to the same
  `standard <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_
  as NumPy and SciPy.
* All changes are reviewed.  Ask on the
  `mailing list <http://groups.google.com/group/networkx-discuss>`_ if
  you get no response to your pull request.
* New default dependencies should be easy to install on all
  platforms, widely-used in the community, and have demonstrated potential for
  wide-spread use in NetworkX.
* Use the following import conventions::

   import numpy as np
   import scipy as sp
   import matplotlib as mpl
   import matplotlib.pyplot as plt
   import pandas as pd
   import networkx as nx

  After importing `sp`` for ``scipy``::

   import scipy as sp

  use the following imports::

   import scipy.linalg  # call as sp.linalg
   import scipy.sparse  # call as sp.sparse
   import scipy.sparse.linalg  # call as sp.sparse.linalg
   import scipy.stats  # call as sp.stats
   import scipy.optimize  # call as sp.optimize

  For example, many libraries have a ``linalg`` subpackage: ``nx.linalg``,
  ``np.linalg``, ``sp.linalg``, ``sp.sparse.linalg``. The above import
  pattern makes the origin of any particular instance of ``linalg`` explicit.


Bugs
----

Please `report bugs on GitHub <https://github.com/networkx/nx-guides/issues>`_.

Policies
--------

All interactions with the project are subject to the `Code of Conduct <CODE_OF_CONDUCT.rst>`_.

We also follow these policies:

* `Networkx Deprecations Policy <https://github.com/networkx/networkx/blob/main/doc/developer/deprecations.rst>`_
* :doc:`Python version support <nep-0029-deprecation_policy>`
