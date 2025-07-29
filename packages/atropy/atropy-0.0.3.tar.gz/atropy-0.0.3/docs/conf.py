# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'atropy'
copyright = '2025, Julian Mangott, Stefan Brunner, Lukas Einkemmer, Martina Prugger'
author = 'Julian Mangott, Stefan Brunner, Lukas Einkemmer, Martina Prugger'
release = '0.0.3'

# Add source directory to syystem path
import os
import sys
sys.path.insert(0, os.path.abspath('../atropy/src'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']
# Display todos by setting to true
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# Mock problematic imports
autodoc_mock_imports = ["xarray", "atropy_core"]
