# -*- coding: utf-8 -*-
# PyXBMCt framework module
#
# PyXBMCt is a mini-framework for creating Kodi (XBMC) Python addons
# with arbitrary UI made of Controls - decendants of xbmcgui.Control class.
# The framework uses image textures from Kodi Confluence skin.
#
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>

from __future__ import absolute_import, division, unicode_literals
from abc import ABCMeta, abstractmethod
from .xbmc4xbox import isXBMC4XBOX

_XBMC4XBOX = isXBMC4XBOX()

# typing module only needed when running pytype and is not available on _XBMC4XBOX AFAIK
try:
    import typing
except:
    pass

# kodi_six doesn't work on XBMC4XBOX
if _XBMC4XBOX:
    import xbmcgui
else:
    from kodi_six import xbmcgui
    from six import with_metaclass

class AbstractGrid(object if _XBMC4XBOX else with_metaclass(ABCMeta, object)):
    """
    Grid functionality mixin.


    Mixin for parent widgets for other XBMC UI controls
    much like Tkinter.Tk or PyQt QWidget class.

    .. warning:: This is an abstract class and is not supposed to be instantiated directly!
    """
    if _XBMC4XBOX:
        __metaclass__ = ABCMeta

    @abstractmethod
    def getRows(self):
        """
        Get grid rows count.
        """
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def getColumns(self):
        """
        Get grid columns count.
        """
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def getGridX(self):
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def getGridY(self):
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def getGridWidth(self):
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def getGridHeight(self):
        # type: () -> int
        raise NotImplementedError

    def getTileWidth(self):
        if not hasattr(self, "_tile_width"):
            self._tile_width = self.getGridWidth() // self.getColumns()
        return self._tile_width

    def getTileHeight(self):
        if not hasattr(self, "_tile_height"):
            self._tile_height = self.getGridHeight() // self.getRows()
        return self._tile_height

    @abstractmethod
    def addControl(self, control):
        # type: (xbmcgui.Control) -> None
        raise NotImplementedError

    @abstractmethod
    def setAnimation(self, control):
        # type: (xbmcgui.Control) -> None
        raise NotImplementedError

    @abstractmethod
    def getWindow(self):
        # type: () -> xbmcgui.Window
        raise NotImplementedError

    def placeControl(self, control, row, column, rowspan=1, columnspan=1, pad_x=5, pad_y=5):
        """
        Place a control within the window grid layout.

        :param control: control instance to be placed in the grid.
        :param row: row number where to place the control (starts from 0).
        :param column: column number where to place the control (starts from 0).
        :param rowspan: set when the control needs to occupy several rows.
        :param columnspan: set when the control needs to occupy several columns.
        :param pad_x: horisontal padding.
        :param pad_y: vertical padding.
        :raises: :class:`AddonWindowError` if a grid has not yet been set.

        Use ``pad_x`` and ``pad_y`` to adjust control's aspect.
        Negative padding values can be used to make a control overlap with grid cells next to it, if necessary.

        Example::

            self.placeControl(self.label, 0, 1)
        """
        # type: (xbmcgui.Control, int, int, int, int, int, int) -> None
        tile_width = self.getTileWidth()
        tile_height = self.getTileHeight()
        control_x = (self.getGridX() + tile_width * column) + pad_x
        control_y = (self.getGridY() + tile_height * row) + pad_y
        control_width = tile_width * columnspan - 2 * pad_x
        control_height = tile_height * rowspan - 2 * pad_y
        control.setPosition(control_x, control_y)
        control.setWidth(control_width)
        control.setHeight(control_height)

        self.addControl(control)
        self.setAnimation(control)

        if hasattr(control, "_placedCallback"):
            control._placedCallback(self.getWindow(), row, column, rowspan, columnspan, pad_x, pad_y)