Using PyXBMCt In Your Addon
===========================

PyXBMCt addon module is included in the official Kodi (XBMC) repo. So to use it, first you need to add
the following string into ``<requires>`` section of your ``addon.xml``::

    <import addon="script.module.pyxbmct" />

Then you need to import pyxbmct module into the namespace of your addon::

    import pyxbmct

