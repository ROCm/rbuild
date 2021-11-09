.. rbuild documentation master file, created by
   sphinx-quickstart on Mon Nov  8 18:55:42 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Rocm build tool
===============

The ``rbuild`` is a cross-platform tool to help simplify building components in rocm. It is used as a layer over cmake inorder to install dependencies and then build the project using those dependencies all in one command. All dependencies and builds are done using local directories so there is need to use ``sudo`` or worry about it messing up the system installation of packages.

.. toctree::
   commands
   config
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
