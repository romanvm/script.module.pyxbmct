Estuary Skin Support
====================

Starting from v.17 (Krypton) Kodi got a new default skin -- Estuary. PyXBMCt supports Estuary and automatically
selects its appearance -- Confluence-based or Estuary-based -- depending on Kodi version by default.
PyXBMCt appearance can also be selected explicitly::

  import pyxbmct

  pyxbmc.skin.estuary = True  # False: use old design

  # Then create your UI elements

You can also subclass :class:`Skin<pyxbmct.addonskin.Skin>` class to chanage
:class:`AddonDialogWindow<pyxbmct.addonwindow.AddonDialogWindow>` or
:class:`AddonFullWindow<pyxbmct.addonwindow.AddonFullWindow>` appearance.
The following example shows how to change :class:`AddonFullWindow<pyxbmct.addonwindow.AddonFullWindow>`
fullscreen background without altering other elements::

  import pyxbmct


  class MySkin(pyxbmct.Skin):
      @property
      def main_bg_img(self):
          return '/path/to/my/background_image.png'


  pyxbct.skin = MySkin()
  # Then create your UI
