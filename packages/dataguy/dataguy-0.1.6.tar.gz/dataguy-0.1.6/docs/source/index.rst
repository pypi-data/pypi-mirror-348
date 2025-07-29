Dataguy Documentation
=====================

Welcome to **DataGuy** — a Python package designed to simplify data science workflows using Large Language Models (LLMs).
It helps with intelligent data wrangling, analysis, and visualization for small-to-medium datasets.

- **GitHub**: `View the source code on GitHub <https://github.com/magistak/llm-data>`_
- **PyPI**: `Install from PyPI <https://pypi.org/project/dataguy>`_
- **Documentation**: `Read the full documentation <https://dataguy.readthedocs.io>`_
- **demo**: `Try the demo <https://colab.research.google.com/drive/1RhLC0b4RN1kVKAh3NqNPn_Axlc0Rn3L8?usp=sharing>`_

Features
--------

- **Automated Data Wrangling**: Clean and preprocess your data using LLM-generated code.
- **AI-Powered Data Visualization**: Describe a plot in words, and let DataGuy build it.
- **Intelligent Data Analysis**: Use natural language prompts to guide statistical summaries or comparisons.
- **Customizable Workflows**: Integrate with `pandas`, `matplotlib`, and more.
- **Safe Code Execution**: Built-in sandboxing to guard against untrusted code execution.
How It Works
============

DataGuy is an intelligent assistant for data exploration and analysis, powered by large language models (LLMs).
This section explains how DataGuy interprets your input, generates code, handles errors, and delivers results.

Overview
--------

The workflow consists of the following steps:

1. **Model Selection**
   DataGuy decides whether your input should be interpreted as a request for a description, a plot, or a code transformation. It selects the appropriate LLM mode accordingly.

2. **Context Building**
   A conversational context is created to track previous prompts, results, and errors. This ensures coherent interactions and allows for iterative improvements.

3. **Prompt Generation**
   Based on your task, DataGuy builds one of three prompt types:

   - **Text mode** for dataset summaries or explanations
   - **Image mode** for understanding uploaded visualizations
   - **Code mode** for generating and executing data operations

4. **LLM Interaction**
   The selected model writes Python code (e.g., `pandas`, `matplotlib`) or produces a natural language response. If execution fails, DataGuy resubmits the failed code with the error message for refinement.

5. **Safe Code Execution**
   Generated code is sandboxed and evaluated in a restricted environment to prevent dangerous operations.

6. **Caching and Retry Logic**
   Past results are cached to avoid duplicate computation. Failed executions are corrected automatically by feeding context back into the model.

Visual Workflow
---------------

.. image:: workflow.jpg
   :alt: DataGuy Workflow
   :width: 600px
   :align: center

Package Structure
---------------

.. image:: graphsum.png
   :alt: DataGuy Structure
   :width: 600px
   :align: center

Example Usage
-------------

.. code-block:: python

   from dataguy import DataGuy
   import seaborn as sns

   # Create the assistant
   dg = DataGuy()

   # Load the Iris dataset
   iris = sns.load_dataset("iris")
   dg.set_data(iris)

   # Wrangle the dataset
   cleaned_data = dg.wrangle_data()
   print("Cleaned Data:", cleaned_data)

   # Describe the dataset
   description = dg.describe_data()
   print("Dataset Description:", description)

Installation
------------

Install DataGuy via pip:

.. code-block:: bash

   pip install dataguy

Quickstart
----------

.. code-block:: python

   import os
   # Set the Anthropic API key as an environment variable
   os.environ["ANTHROPIC_API_KEY"] = "your_anthropic_api_key_here"

   from dataguy import DataGuy
   import seaborn as sns
   
   dg = DataGuy()
   iris = sns.load_dataset("iris")
   dg.set_data(iris)

   dg.wrangle_data()

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   how_it_works
   api/index
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
