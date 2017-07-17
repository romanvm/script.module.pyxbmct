Skins
=====

Starting from ``v.1.2.0``, PyXBMCt provides :class:`BaseSkin<pyxbmct.addonskin.BaseSkin>` and
:class:`Skin<pyxbmct.addonskin.Skin>` classes that allow you to customize your
UI elements appearance fully or partially. To customize your UI skin you need
to subclass one of the following classes and set your skin to be used by PyXBMCt.

.. warning:: :class:`BaseSkin<pyxbmct.addonskin.BaseSkin>` is an abstract class.
  You need to subclass it and implement all its properties in your derived class.

The :class:`Skin<pyxbmct.addonskin.Skin>` can be subclassed to change only some
of its properties. The following example shows how to change
:class:`AddonFullWindow<pyxbmct.addonwindow.AddonFullWindow>` fullscreen background
without altering other elements::

  import pyxbmct


  class MySkin(pyxbmct.Skin):
      @property
      def main_bg_img(self):
          return '/path/to/my/background_image.png'


  pyxbmct.skin = MySkin()
  # Then create your UI

