Using PyXBMCt In Your Addon
===========================

First, you need to make sure you have script.module.pyxbmct actually installed on your PC for development purposes. You need to either install your addon from a ZIP so that all the dependencies will be installed with it, or install another addon that have PyXBMCt as a dependency, like TVmaze Scrobbler. You can remove the additional addon afterwards if you want.

PyXBMCt addon module is included in the official Kodi (XBMC) repo. So to use it, you need to add
the following string into ``<requires>`` section of your ``addon.xml``::

    <import addon="script.module.pyxbmct" />

Then you need to import pyxbmct module into the namespace of your addon::

    import pyxbmct

