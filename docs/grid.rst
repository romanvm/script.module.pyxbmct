Grid Layout Manager
===================

The Grid layout manager helps to place UI controls within the parent window.
It is similar to PyQt’s QGridLayout or Tkniter’s Grid geometry manager.
The Grid layout manager is implemented through
:meth:`setGeometry<pyxbmct.addonwindow.AbstractWindow.setGeometry>` and
:meth:`placeControl<pyxbmct.addonwindow.AbstractWindow.placeControl>` methods of a base PyXBMCt class.

.. warning::
  Currently PyXBMCt does not support changing window geometry at runtime so you must call
  :meth:`setGeometry<pyxbmct.addonwindow.AbstractWindow.setGeometry>` method only once.

To place a control you simply provide it as the 1st positional argument to
:meth:`placeControl<pyxbmct.addonwindow.AbstractWindow.placeControl>` method,
and then specify a row and a column for the control as the next arguments,
and the control will be placed in a specific grid cell.
This eliminates the need to provide exact coordinates for each control and then fine-tune them.
If a control needs to occupy several grid cells, you can provide rowspan and/or columspan parameters to specify
how many cells it should take.

.. note::
  Row and column numbers start from zero, i.e. the top-left cell will have row# = ``0``, column# = ``0``.

The Grid layout manager does not check if a control will actually be placed within the parent window.
By providing a row and/or a column number which exceeds row and/or column count of the parent window,
a control can be placed outside the window, intentionally or unintentionally.
You need to check the visual appearance of your addon window and correct positions of controls, if necessary.

The Grid layout manager also works with xbmcgui controls, but when instantiating an xbmcgui control you need
to provide it with fake coordinates and size. Any integer values will do.

**Hint**: the size and aspect of an individual control can be adjusted with ``pad_x`` and ``pad_y`` parameters
of :meth:`placeControl<pyxbmct.addonwindow.AbstractWindow.placeControl>` method.
By default, both padding values equal ``5``.
