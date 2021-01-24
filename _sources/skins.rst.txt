Skins
=====

Starting from ``v.1.2.0``, PyXBMCt provides :class:`BaseSkin<pyxbmct.addonskin.BaseSkin>` and
:class:`Skin<pyxbmct.addonskin.Skin>` classes that allow you to customize
PyXBMCt UI elements appearance fully or partially.
To customize your UI skin you need to subclass one of those classes and
set your custom skin instance as ``pyxbmct.skin`` module-level property (see below).

:class:`BaseSkin<pyxbmct.addonskin.BaseSkin>` is an abstract class that allows you
to fully customize the appearance of PyXBMCt ``*Window`` classes.
You need to subclass it and define all your custom skin attributes -- image textures,
coorditate offsets, etc. -- as properties of your derived class.

The :class:`Skin<pyxbmct.addonskin.Skin>` can be subclassed to change only some
of the current PyXBMCt skin properties. The following example shows how to change the
fullscreen background of :class:`AddonFullWindow<pyxbmct.addonwindow.AddonFullWindow>`
class without altering other elements::

  import pyxbmct


  class MySkin(pyxbmct.Skin):
      @property
      def main_bg_img(self):
          return '/path/to/my/background_image.png'


  pyxbmct.addonwindow.skin = MySkin()


  # Then create your UI window class with the new background
  class MyCoolWindow(pyxbmct.AddonWindow):
    ...

