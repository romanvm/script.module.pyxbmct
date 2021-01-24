Base Classes
============

PyXBMCt provides 4 base classes: `AddonDialogWindow`_, `AddonFullWindow`_, `BlankDialogWindow and BlankFullWindow`_. These classes serve as containers for other UI elements (controls).
All base classes are "new-style" Python classes.

AddonDialogWindow
-----------------

:class:`AddonDialogWindow<pyxbmct.addonwindow.AddonDialogWindow>` class is based on :class:`xbmcgui.WindowDialog`
and provides an interface window with background and a title-bar.
The window serves as a parent control to other UI controls. Like all the other base classes,
:class:`AddonDialogWindow<pyxbmct.addonwindow.AddonDialogWindow>` has the Grid layout manager
to simplify arranging your UI controls and the event connection manager
to connect XBMC UI events to functions and methods of your addon.

.. figure:: _static/addon_dialog_window.jpg

  **AddonDialogWindow parent window**

The main control window of :class:`AddonDialogWindow<pyxbmct.addonwindow.AddonDialogWindow>`
is always displayed on top of Kodi UI, even video playback and music visualization, so it’s better suited for addons
that are not supposed to play video or music.

.. note:: Width, height and coordinates (optional) for the control window are specified
    in Kodi UI coordinate grid pixels.

The default resolution of UI coordinate grid is always 1280x720 regardless of your actual display resolution.
This way UI elements have the same visible size no matter what display resolution you use.

AddonFullWindow
---------------

:class:`AddonFullWinow<pyxbmct.addonwindow.AddonFullWindow>` is based on :class:`xbcmgui.Window` class.
It is similar to :class:`AddonDialogWindow<pyxbmct.addonwindow.AddonDialogWindow>` and also provides
a parent control window for other UI controls.
But, unlike :class:`AddonDialogWindow<pyxbmct.addonwindow.AddonDialogWindow>`,
it has a solid main background (for which the default Estuary or Confluence background is used)
and can hide under video or music visualization.

.. figure:: _static/addon_full_window.jpg

  **AddonFullWindow parent control window**

BlankDialogWindow and BlankFullWindow
-------------------------------------

:class:`BlankDialogWindow<pyxbmct.addonwindow.BlankDialogWindow>` and
:class:`BlankFullWindow<pyxbmct.addonwindow.BlankFullWindow>` are based on :class:`xbmcgui.WindowDialog`
and :class:`xbmcgui.Window` respectively.
They have no visual elements whatsoever, but, like the 2 previously described classes,
they provide the Grid layout and event connection managers.

Those classes are meant for DIY developers who want full control over the visual appearance of their addons.
