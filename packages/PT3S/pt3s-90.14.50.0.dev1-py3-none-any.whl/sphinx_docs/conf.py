# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import subprocess
from datetime import datetime
sys.path.insert(0, os.path.abspath(r'C:\Users\jablonski\3S\PT3S'))

project = 'PT3S'
current_year = datetime.now().year
copyright = f'1986-{current_year}, 3S Consult GmbH'
author = '3S Consult GmbH'
release = '90.14.50.0.dev1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.viewcode', 'sphinx.ext.doctest','nbsphinx','sphinx_copybutton','sphinx.ext.extlinks']
#,'sphinx.ext.inheritance_diagram'
#graphviz_dot = 'dot'

todo_include_todos=True

templates_path = [r'C:\Users\jablonski\3S\PT3S']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints', '.virtual_documents', 'Planungsbeispiel.ipynb']#,'Example0.ipynb','Example1.ipynb','Example2.ipynb']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme' #'alabaster'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_logo = '_static/pt3s_logo.png'  # oder 'logo.svg', je nachdem, welche Datei Sie verwenden
html_favicon = '_static/favicon.ico'
html_theme_options = {
    'logo_only': True,  # Nur das Logo wird oben in der Seitenleiste angezeigt
    'style_external_links': False,
}
# This function will be called before Sphinx starts to build documents.
def setup(app):
    app.add_css_file('custom.css')


