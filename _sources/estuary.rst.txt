Estuary Skin Support
====================

Starting from v.17 (Krypton) Kodi got a new default skin -- Estuary. PyXBMCt supports Estuary and automatically
selects its appearance -- Confluence-based or Estuary-based -- depending on Kodi version by default.
PyXBMCt appearance can also be set explicitly::

  import pyxbmct

  pyxbmct.skin.estuary = True  # False: use old design

  # Then create your UI elements

