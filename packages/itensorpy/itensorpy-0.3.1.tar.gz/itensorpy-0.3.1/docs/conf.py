"""
Configuration file for the Sphinx documentation builder.
"""

import os
import sys
import inspect
import importlib
import datetime

# Add the project root to the path so we can import the package
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'iTensorPy'
copyright = f'{datetime.datetime.now().year}, iTensorPy Contributors'
author = 'iTensorPy Contributors'

# Import the package to get the version
import src.itensorpy
version = src.itensorpy.__version__
release = version

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
]

# Configuration
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = '.rst'
master_doc = 'index'
language = None
pygments_style = 'sphinx'

# Theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sympy': ('https://docs.sympy.org/latest/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# autodoc settings
autodoc_member_order = 'bysource'
autoclass_content = 'both'
