# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


sys.path.insert(0, os.path.abspath('..'))

project = 'Pytero'
copyright = '2022-present, Devonte W'
author = 'Devonte W'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme'
]

intersphinx_mapping = {'py': ('https://docs.python.org/3', None)}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'

resource_links = {
    'discord': 'https://discord.com/invite/dwcfTjgn7S',
    'issues': 'https://github.com/PteroPackages/Pytero/issues'
}
