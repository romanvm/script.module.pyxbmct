.. PyXBMCt documentation master file, created by
   sphinx-quickstart on Tue Dec 01 13:51:23 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wellcome to PyXBMCt documentation!
==================================
A GUI micro-framework for Kodi meidacenter addons
-------------------------------------------------

PyXBMCt is a Python micro-framework created to simplify creating GUI for `Kodi (XBMC)`_ mediacenter addons.
It was inspired by PyQt (hence the name) and shares the same basic principles,
so those who are familiar with PyQt/PySide should feel themselves right at home.

The framework provides 4 base container classes, 9 ready-to-use widgets or, in Kodi terms, controls,
a Grid layout manager and an event connection manager.

PyXBMCt uses texture images from Kodi's default Confluence skin to decorate its visual elements.
Those textures are included in PyXBMCt, so UI based on it will have the same look in different skins.

PyXBMCt is essentially a thin wrapper around several :mod:`xbmcgui` classes so please consult
xbmcgui module documentation on how to use all features of PyXBMCt windows and controls.

PyXBMCt does not provide as many features and customization capabilites as skined GUIs based on
:class:`xbmcgui.WindowXML` and :class:`xbmcgui.WindowXMLDialog` classes but it is relatively easy to learn
and does not require the knowledge of Kodi skinning. PyXBMCt-based GUIs can be created entirely in Python.

.. _Kodi (XBMC): http://www.kodi.tv

Contents:

.. toctree::
   :maxdepth: 2

   classes
   controls
   grid
   connection
   using
   examples
   links
   pyxbmct


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
