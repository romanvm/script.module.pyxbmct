# -*- coding: utf-8 -*-

import sys
import os
from unittest import mock

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(basedir, 'script.module.pyxbmct', 'lib'))

import xbmc
import xbmcgui

kodi_six_mock = mock.MagicMock()
kodi_six_mock.xbmc = xbmc
kodi_six_mock.xbmcgui = xbmcgui

sys.modules['kodi_six'] = kodi_six_mock

import pyxbmct

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'alabaster',
]

autodoc_member_order = 'bysource'
autodoc_default_flags = ['members', 'show-inheritance']
autosummary_generate = True
intersphinx_mapping = {'https://docs.python.org/2.7': None,
                       'http://romanvm.github.io/Kodistubs': None}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'PyXBMCt'
copyright = u'2015, Roman Miroshnychenko'
author = u'Roman Miroshnychenko'

language = None

exclude_patterns = ['_build']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'

html_theme_options = {
    'github_button': True,
    'github_type': 'star&v=2',
    'github_user': 'romanvm',
    'github_repo': 'script.module.pyxbmct',
    'github_banner': True,
    'description': 'A GUI micro-framework for Kodi mediacenter addons',
    'font_family': 'Georgia',
}

html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

html_show_sourcelink = False

htmlhelp_basename = 'PyXBMCtdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'PyXBMCt.tex', u'PyXBMCt Documentation',
   u'Roman Miroshnychenko', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pyxbmct', u'PyXBMCt Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'PyXBMCt', u'PyXBMCt Documentation',
   author, 'PyXBMCt', 'One line description of project.',
   'Miscellaneous'),
]
