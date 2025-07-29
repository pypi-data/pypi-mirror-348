Getting started
===============

Install
-------

.. code-block:: console

   $ pip install dataguy

Usage in three lines
--------------------

.. code-block:: python

   import os
   import seaborn as sns
   import dataguy as dg
   # Set the Anthropic API key as an environment variable
   os.environ["ANTHROPIC_API_KEY"] = "your_anthropic_api_key_here"

   from dataguy import DataGuy
   dg = dg.DataGuy()
   iris = sns.load_dataset("iris")
   dg.set_data(iris)

   dg.wrangle_data()
   ...

What next?
----------

* Browse the :doc:`API reference <api/index>`.
* See the Jupyter notebook examples in the *examples/* folder.
