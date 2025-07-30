# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ticterm'
copyright = '2025, gitlab.com/tictaccc'
author = 'gitlab.com/tictaccc'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
import subprocess
sys.path.insert(0, os.path.abspath('..'))
import ticterm

release = subprocess.check_output(
    ['hatch', 'version'],
    cwd = './'
  ).strip().decode()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints'
]

autodoc_inherit_docstrings = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
