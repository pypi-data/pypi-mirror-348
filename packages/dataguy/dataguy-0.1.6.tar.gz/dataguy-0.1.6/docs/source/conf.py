from __future__ import annotations

import datetime
import importlib.metadata as metadata
import os
import sys
print(sys.path)
from pathlib import Path

# Debug: Check installed packages
print("Installed packages:", [d.name for d in metadata.distributions()])

# Debug: Test importing dataguy
try:
    import dataguy
    print("Successfully imported dataguy")
except ImportError as e:
    print(f"Failed to import dataguy: {e}")

# -- Path setup --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# -- Project information -----------------------------------------------------
project = "DataGuy"
author = "István Magyary, Sára Viemann, Bálint Kristóf"
copyright = f"{datetime.datetime.now().year}, {author}"
release = metadata.version("dataguy") if "dataguy" in metadata.packages_distributions() else "0.1.6"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "myst_parser",
]

autosummary_generate = True
napoleon_numpy_docstring = True
napoleon_google_docstring = False
add_module_names = False

templates_path = ["_templates"]
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
