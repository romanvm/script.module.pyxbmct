# -*- coding: utf-8 -*-
# PyXBMCt framework module
#
# PyXBMCt is a mini-framework for creating Kodi (XBMC) Python addons
# with arbitrary UI made of Controls - decendants of xbmcgui.Control class.
# The framework uses image textures from Kodi Confluence skin.
#
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>
"""
This module contains all classes and constants of PyXBMCt framework
"""

from __future__ import absolute_import, division, unicode_literals

import platform

XBMC4XBOX = platform.system() == "XBMC4Xbox"

# kodi_six doesn't work on XBMC4XBOX
if XBMC4XBOX:
    range = xrange
    import xbmc, xbmcgui, inspect
else:
    from future.builtins import range
    from kodi_six import xbmc, xbmcgui

import os
from abc import ABCMeta, abstractmethod

from .addonskin import Skin

skin = Skin()

# Text alignment constants. Mixed variants are obtained by bit OR (|)
ALIGN_LEFT = 0
"""Align left"""
ALIGN_RIGHT = 1
"""Align right"""
ALIGN_CENTER_X = 2
"""Align center horisontally"""
ALIGN_CENTER_Y = 4
"""Align center vertically"""
ALIGN_CENTER = 6
"""Align center by both axis"""
ALIGN_TRUNCATED = 8
"""Align truncated"""
ALIGN_JUSTIFY = 10
"""Align justify"""

# Kodi key action codes.
# More codes available in xbmcgui module
ACTION_PREVIOUS_MENU = 10
"""ESC action"""
ACTION_NAV_BACK = 92
"""Backspace action"""
ACTION_MOVE_LEFT = 1
"""Left arrow key"""
ACTION_MOVE_RIGHT = 2
"""Right arrow key"""
ACTION_MOVE_UP = 3
"""Up arrow key"""
ACTION_MOVE_DOWN = 4
"""Down arrow key"""
ACTION_MOUSE_WHEEL_UP = 104
"""Mouse wheel up"""
ACTION_MOUSE_WHEEL_DOWN = 105
"""Mouse wheel down"""
ACTION_MOUSE_DRAG = 106
"""Mouse drag"""
ACTION_MOUSE_MOVE = 107
"""Mouse move"""
ACTION_MOUSE_LEFT_CLICK = 100
"""Mouse click"""

KEY_BUTTON_A = 256
"""XBMC4XBOX A button pressed"""


def _set_textures(textures, kwargs):
    """Set texture arguments for controls."""
    for texture in textures:
        if kwargs.get(texture) is None:
            kwargs[texture] = textures[texture]


class AddonWindowError(Exception):
    """Custom exception"""
    pass


class AbstractGrid(object):
    """
    Grid functionality mixin.
    

    Mixin for parent widgets for other XBMC UI controls
    much like Tkinter.Tk or PyQt QWidget class.
    
    .. warning:: This is an abstract class and is not supposed to be instantiated directly!
    """
    __metaclass__ = ABCMeta

    def __init__(self, window):
        """
        :param window: the window that the grid will exist in
        """
        self._window = window

    @abstractmethod
    def getRows(self):
        """
        Get grid rows count.
        """
        raise NotImplementedError

    @abstractmethod
    def getColumns(self):
        """
        Get grid columns count.
        """
        raise NotImplementedError

    @abstractmethod
    def getGridX(self):
        raise NotImplementedError

    @abstractmethod
    def getGridY(self):
        raise NotImplementedError

    @abstractmethod
    def getGridWidth(self):
        raise NotImplementedError

    @abstractmethod
    def getGridHeight(self):
        raise NotImplementedError

    def _setGrid(self):
        """
        Set window grid layout of rows x columns.

        This is a helper method not to be called directly.
        """
        self.tile_width = self.getGridWidth() // self.getColumns()
        self.tile_height = self.getGridHeight() // self.getRows()

    @abstractmethod
    def addControl(self, control):
        raise NotImplementedError

    @abstractmethod
    def setAnimation(self, control):
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
        control_x = (self.getGridX() + self.tile_width * column) + pad_x
        control_y = (self.getGridY() + self.tile_height * row) + pad_y
        control_width = self.tile_width * columnspan - 2 * pad_x
        control_height = self.tile_height * rowspan - 2 * pad_y
        control.setPosition(control_x, control_y)
        control.setWidth(control_width)
        control.setHeight(control_height)
        if hasattr(control, "_placedCallback"):
            control._placedCallback(self._window, row, column, rowspan, columnspan, pad_x, pad_y)

        try:
            self.addControl(control)
            self.setAnimation(control)
        except AttributeError:
            raise AddonWindowError('Window is not set! Pass window when calling the constructor.')


# Inheritance for the sake of pytype seeing getX etc. xbmcgui.Control does not exist on XBMC4XBOX
class ControlMixin(object if XBMC4XBOX else xbmcgui.Control):
    """
    Basic control functionality mixin.

    Provides utility methdos and wrappers for some existing methods to support PyXBMCt

    .. warning:: This is an mixin class and is not supposed to be instantiated directly!
    """

    def __eq__(self, other):
        if hasattr(other, 'getId'):
            return self.getId() == other.getId()
        return False

    def isEnabled(self):
        """
        Determine if a control is enabled or not.

        Example::

            enabled = self.isEnabled()
        """
        # Test this way so that a constructor is not needed
        # to set the intial values
        return not hasattr(self, "_is_enabled") or self._is_enabled

    if XBMC4XBOX:
        def isVisible(self):
            """
            Determine if the control is visible or not.

            Example::

                enabled = self.isVisible()
            """
            return not hasattr(self, "_is_visible") or self._is_visible

        def getX(self):
            return self.getPosition()[0]

        def getY(self):
            return self.getPosition()[1]

        def setVisible(self, is_visible):
            """
            Set whether the control is visible or not.

            :param is_visible: boolean to determine if the control is visible.

            Example::

                self.setVisible(False)
            """
            self._is_visible = is_visible
            for ancestor in inspect.getmro(self.__class__):
                if inspect.getmodule(ancestor) == xbmcgui:
                    ancestor.setVisible(self, is_visible)
                    return

        def setEnabled(self, is_enabled):
            """
            Set whether the control is enabled or not.

            :param is_enabled: boolean to determine if the control is enabled.

            Example::

                self.setEnabled(False)
            """
            self._is_enabled = is_enabled
            for ancestor in inspect.getmro(self.__class__):
                if inspect.getmodule(ancestor) == xbmcgui:
                    ancestor.setEnabled(self, is_enabled)
                    return
    else:
        # isVisible is available by default so setVisible wrapper is not needed

        def setEnabled(self, is_enabled):
            """
            Set whether the control is enabled or not.

            :param is_enabled: boolean to determine if the control is enabled.

            Example::

                self.setEnabled(False)
            """
            self._is_enabled = is_enabled
            xbmcgui.Control.setEnabled(self, is_enabled)

    def getMidpoint(self):
        """
        Get the (x,y) coordinates of the controls midpoint.

        Example::

            x, y = self.getMidpoint()
        """
        x = self.getX()
        y = self.getY()
        width = self.getWidth()
        height = self.getHeight()
        return (x + (width / 2), y + (height / 2))


class Label(ControlMixin, xbmcgui.ControlLabel):
    """
    Label(label, font=None, textColor=None, disabledColor=None, alignment=0,hasPath=False, angle=0)

    ControlLabel class.

    Implements a simple text label.

    :param label: text string
    :type label: str
    :param font: font used for label text. (e.g. ``'font13'``)
    :type font: str
    :param textColor: hex color code of enabled label's label. (e.g. ``'0xFFFFFFFF'``)
    :type textColor: str
    :param disabledColor: hex color code of disabled label's label. (e.g. ``'0xFFFF3300'``)
    :type disabledColor: str
    :param alignment: alignment of label. **Note**: see ``xbfont.h``
    :type alignment: int
    :param hasPath: ``True`` = stores a path / ``False`` = no path.
    :type hasPath: bool
    :param angle: angle of control. (``+`` rotates CCW, ``-`` rotates CW)
    :type angle: int

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.label = Label('Status', angle=45)
    """

    def __new__(cls, *args, **kwargs):
        return super(Label, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class FadeLabel(ControlMixin, xbmcgui.ControlFadeLabel):
    """
    FadeLabel(font=None, textColor=None, _alignment=0)

    Control that scrolls label text.

    Implements a text label that can auto-scroll very long text.

    :param font: font used for label text. (e.g. ``'font13'``)
    :type font: str
    :param textColor: hex color code of fadelabel's labels. (e.g. ``'0xFFFFFFFF'``)
    :type textColor: str
    :param _alignment: alignment of label. **Note**: see ``xbfont.h``
    :type _alignment: int

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.fadelabel = FadeLabel(textColor='0xFFFFFFFF')
    """

    def __new__(cls, *args, **kwargs):
        return super(FadeLabel, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class TextBox(ControlMixin, xbmcgui.ControlTextBox):
    """
    TextBox(font=None, textColor=None)

    ControlTextBox class

    Implements a box for displaying multi-line text.
    Long text is truncated from below. Also supports auto-scrolling.

    :param font: font used for text. (e.g. ``'font13'``)
    :type font: str
    :param textColor: hex color code of textbox's text. (e.g. ``'0xFFFFFFFF'``)
    :type textColor: str

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.textbox = TextBox(textColor='0xFFFFFFFF')
    """

    def __new__(cls, *args, **kwargs):
        return super(TextBox, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class Image(ControlMixin, xbmcgui.ControlImage):
    """
    Image(filename, aspectRatio=0, colorDiffuse=None)

    ControlImage class.

    Implements a box for displaying ``.jpg``, ``.png``, and ``.gif`` images.

    :param filename: path or URL to an image file.
    :type filename: str
    :param aspectRatio: (values: ``0`` = stretch (default), ``1`` = scale up (crops), ``2`` = scale down (black bars)
    :type aspectRatio: int
    :param colorDiffuse: for example, ``'0xC0FF0000'`` (red tint)
    :type colorDiffuse: str

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.image = Image('d:\images\picture.jpg', aspectRatio=2)
    """

    def __new__(cls, *args, **kwargs):
        return super(Image, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class Button(ControlMixin, xbmcgui.ControlButton):
    """
    Button(label, focusTexture=None, noFocusTexture=None, textOffsetX=CONTROL_TEXT_OFFSET_X, textOffsetY=CONTROL_TEXT_OFFSET_Y, alignment=4, font=None, textColor=None, disabledColor=None, angle=0, shadowColor=None, focusedColor=None)

    ControlButton class.

    Implements a clickable button.

    :param label: button caption
    :type label: str
    :param focusTexture: filename for focus texture.
    :type focusTexture: str
    :param noFocusTexture: filename for no focus texture.
    :type noFocusTexture: str
    :param textOffsetX: x offset of label.
    :type textOffsetX: int
    :param textOffsetY: y offset of label.
    :type textOffsetY: int
    :param alignment: alignment of label. **Note**: see ``xbfont.h``
    :type alignment: int
    :param font: font used for label text. (e.g. ``'font13'``)
    :type font: str
    :param textColor: hex color code of enabled button's label. (e.g. ``'0xFFFFFFFF'``)
    :type textColor: str
    :param disabledColor: hex color code of disabled button's label. (e.g. ``'0xFFFF3300'``)
    :type disabledColor: str
    :param angle: angle of control. (``+`` rotates CCW, ``-`` rotates CW)
    :type angle: int
    :param shadowColor: hex color code of button's label's shadow. (e.g. ``'0xFF000000'``)
    :type shadowColor: str
    :param focusedColor: hex color code of focused button's label. (e.g. ``'0xFF00FFFF'``)
    :type focusedColor: str

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.button = Button('Status', font='font14')
    """

    def __new__(cls, *args, **kwargs):
        textures = {'focusTexture': os.path.join(skin.images, 'Button', 'KeyboardKey.png'),
                    'noFocusTexture': os.path.join(skin.images, 'Button', 'KeyboardKeyNF.png')}
        _set_textures(textures, kwargs)
        if kwargs.get('alignment') is None:
            kwargs['alignment'] = ALIGN_CENTER
        return super(Button, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class RadioButton(ControlMixin, xbmcgui.ControlRadioButton):
    """
    RadioButton(label, focusTexture=None, noFocusTexture=None, textOffsetX=None, textOffsetY=None, _alignment=None, font=None, textColor=None, disabledColor=None, angle=None, shadowColor=None, focusedColor=None, focusOnTexture=None, noFocusOnTexture=None, focusOffTexture=None, noFocusOffTexture=None)

    ControlRadioButton class.

    Implements a 2-state switch.

    :param label: label text.
    :type: str or unicode
    :param focusTexture: filename for focus texture.
    :type focusTexture: str
    :param noFocusTexture: filename for no focus texture.
    :type noFocusTexture: str
    :param textOffsetX: x offset of label.
    :type textOffsetX: int
    :param textOffsetY: y offset of label.
    :type textOffsetY: int
    :param _alignment: alignment of label - *Note, see xbfont.h
    :type _alignment: int
    :param font: font used for label text. (e.g. 'font13')
    :type font: str
    :param textColor: hexstring -- color of enabled radio button's label. (e.g. '0xFFFFFFFF')
    :type textColor: str
    :param disabledColor: hexstring -- color of disabled radio button's label. (e.g. '0xFFFF3300')
    :type disabledColor: str
    :param angle: angle of control. (+ rotates CCW, - rotates CW)
    :type angle: int
    :param shadowColor: hexstring -- color of radio button's label's shadow. (e.g. '0xFF000000')
    :type shadowColor: str
    :param focusedColor: hexstring -- color of focused radio button's label. (e.g. '0xFF00FFFF')
    :type focusedColor: str
    :param focusOnTexture: filename for radio focused/checked texture.
    :type focusOnTexture: str
    :param noFocusOnTexture: filename for radio not focused/checked texture.
    :type noFocusOnTexture: str
    :param focusOffTexture: filename for radio focused/unchecked texture.
    :type focusOffTexture: str
    :param noFocusOffTexture: filename for radio not focused/unchecked texture.
    :type noFocusOffTexture: str

    .. note:: To customize RadioButton all 4 abovementioned textures need to be provided.

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.radiobutton = RadioButton('Status', font='font14')
    """

    def __new__(cls, *args, **kwargs):
        if not XBMC4XBOX and xbmc.getInfoLabel('System.BuildVersion')[:2] >= '13':
            textures = {'focusTexture': os.path.join(skin.images, 'RadioButton', 'MenuItemFO.png'),
                        'noFocusTexture': os.path.join(skin.images, 'RadioButton', 'MenuItemNF.png'),
                        'focusOnTexture': os.path.join(skin.images, 'RadioButton', 'radiobutton-focus.png'),
                        'noFocusOnTexture': os.path.join(skin.images, 'RadioButton', 'radiobutton-focus.png'),
                        'focusOffTexture': os.path.join(skin.images, 'RadioButton', 'radiobutton-nofocus.png'),
                        'noFocusOffTexture': os.path.join(skin.images, 'RadioButton', 'radiobutton-nofocus.png')}
        else:  # This is for compatibility with Frodo and earlier versions.
            textures = {'focusTexture': os.path.join(skin.images, 'RadioButton', 'MenuItemFO.png'),
                        'noFocusTexture': os.path.join(skin.images, 'RadioButton', 'MenuItemNF.png'),
                        'TextureRadioFocus': os.path.join(skin.images, 'RadioButton', 'radiobutton-focus.png'),
                        'TextureRadioNoFocus': os.path.join(skin.images, 'RadioButton', 'radiobutton-nofocus.png')}
        _set_textures(textures, kwargs)
        return super(RadioButton, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


# Edit is not supported on Xbox using the Python API
if not XBMC4XBOX:
    class Edit(ControlMixin, xbmcgui.ControlEdit):
        """
        Edit(label, font=None, textColor=None, disabledColor=None, _alignment=0, focusTexture=None, noFocusTexture=None, isPassword=False)

        ControlEdit class. Edit is not supported on Xbox using the Python API

        Implements a clickable text entry field with an on-screen keyboard.

        :param label: text string.
        :type label: str or unicode
        :param font: [opt] font used for label text. (e.g. 'font13')
        :type font: str
        :param textColor: [opt] hexstring -- color of enabled label's label. (e.g. '0xFFFFFFFF')
        :type textColor: str
        :param disabledColor: [opt] hexstring -- color of disabled label's label. (e.g. '0xFFFF3300')
        :type disabledColor: str
        :param _alignment: [opt] lignment of label - *Note, see xbfont.h
        :type _alignment: int
        :param focusTexture: [opt] filename for focus texture.
        :type focusTexture: str
        :param noFocusTexture: [opt] filename for no focus texture.
        :type noFocusTexture: str
        :param isPassword: [opt] if ``True``, mask text value.
        :type isPassword: bool

        .. note:: You can use the above as keywords for arguments and skip certain optional arguments.
            Once you use a keyword, all following arguments require the keyword.
            After you create the control, you need to add it to the window with ``placeControl()``.

        Example::

            self.edit = Edit('Status')
        """

        def __new__(cls, *args, **kwargs):
            textures = {'focusTexture': os.path.join(skin.images, 'Edit', 'button-focus.png'),
                        'noFocusTexture': os.path.join(skin.images, 'Edit', 'black-back2.png')}
            _set_textures(textures, kwargs)
            return super(Edit, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class List(ControlMixin, xbmcgui.ControlList):
    """
    List(font=None, textColor=None, buttonTexture=None, buttonFocusTexture=None, selectedColor=None, _imageWidth=10, _imageHeight=10, _itemTextXOffset=10, _itemTextYOffset=2, _itemHeight=27, _space=2, _alignmentY=4)

    ControlList class.

    Implements a scrollable list of items.

    :param font: string - font used for items label. (e.g. 'font13')
    :param textColor: hexstring - color of items label. (e.g. '0xFFFFFFFF')
    :param buttonTexture: string - filename for no focus texture.
    :param buttonFocusTexture: string - filename for focus texture.
    :param selectedColor: integer - x offset of label.
    :param _imageWidth: integer - width of items icon or thumbnail.
    :param _imageHeight: integer - height of items icon or thumbnail.
    :param _itemTextXOffset: integer - x offset of items label.
    :param _itemTextYOffset: integer - y offset of items label.
    :param _itemHeight: integer - height of items.
    :param _space: integer - space between items.
    :param _alignmentY: integer - Y-axis alignment of items label - *Note, see xbfont.h

    .. note:: After you create the control, you need to add it to the window with placeControl().

    Example::

        self.cList = List('font14', space=5)
    """

    def __new__(cls, *args, **kwargs):
        textures = {'buttonTexture': os.path.join(skin.images, 'List', 'MenuItemNF.png'),
                    'buttonFocusTexture': os.path.join(skin.images, 'List', 'MenuItemFO.png')}
        _set_textures(textures, kwargs)
        return super(List, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class Group(ControlMixin, xbmcgui.ControlGroup, AbstractGrid):
    """
    Group(rows, columns)

    ControlGroup class.

    Implements a secondary grid (with its own coordinate system) that controls can be placed in.
    Allowing for finer control over where controls are placed in a window.

    :param rows: integer - the number of rows in the grid
    :param columns: integer - the number of columns in the grid

    .. note:: After you create the control, you need to add it to the window with placeControl().

    .. warning:: You must place Group in a window before adding controls to it!

    Example::

        self.group = Group(1,2)
    """

    def __new__(cls, rows, columns, *args, **kwargs):
        return super(Group, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)

    def getGridX(self):
        return self.getX()

    def getGridY(self):
        return self.getY()

    def getGridWidth(self):
        return self.getWidth()

    def getGridHeight(self):
        return self.getHeight()

    def getRows(self):
        """
        Get grid rows count.
        """
        return self._rows

    def getColumns(self):
        """
        Get grid columns count.
        """
        return self._columns

    def __init__(self, rows, columns, *args, **kwargs):
        self._rows = rows
        self._columns = columns
        self._controls = []

    def addControl(self, control):
        self._controls.append(control)
        self._window.addControl(control)

    def setAnimation(self, control):
        self._window.setAnimation(control)

    def _removedCallback(self, window):
        self.removeAllChildren()

    def removeControl(self, control):
        """
        Remove a control from the window grid layout.

        :param control: control instance to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        self._controls.remove(control)
        self._window.removeControl(control)

    def removeControls(self, controls):
        """
        Remove multiple controls from the window grid layout.

        :param controls: an iterable of control instances to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        for control in controls:
            self.removeControl(control)

    def removeAllChildren(self):
        """
        Removes all the Group's children (and all their children) from the window.

        Example::

            group.removeAllChildren()
        """
        self.removeControls(self._controls)

    def setVisible(self, is_visible):
        """
        Sets the group (and it all its current children) to be either visible or invisible.

        :param is_visible: determines whether or the group and its current children should be visible or not.

        Example::

            group.setVisible(False)
        """
        xbmcgui.ControlGroup.setVisible(self, is_visible)
        for control in self._controls:
            control.setVisible(is_visible)

    def setVisibleCondition(self, is_visible, allow_hidden_focus=False):
        """
        See the XBMC documentation
        """
        xbmcgui.ControlGroup.setVisibleCondition(self, is_visible, allow_hidden_focus)
        for control in self._controls:
            control.setVisibleCondition(is_visible, allow_hidden_focus)

    def setEnabled(self, is_enabled):
        """
        Sets the group (and it all its current children) to be either enabled or disabled.

        :param is_enabled: determines whether or the group and its current children should be enabled or not.

        Example::

            group.setVisible(setEnabled)
        """
        xbmcgui.ControlGroup.setEnabled(self, is_enabled)
        for control in self._controls:
            control.setEnabled(is_enabled)

    def setEnableCondition(self, is_enabled):
        """
        See the XBMC documentation
        """
        xbmcgui.ControlGroup.setEnableCondition(self, is_enabled)
        for control in self._controls:
            control.setEnableCondition(is_enabled)

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the grid has been placed
        """
        AbstractGrid.__init__(self, window)
        self._setGrid()

    def _focussedCallback(self):
        # Want to divert focus to the first control if possible
        # it doesn't really make sense for a container to have focus
        if self._controls:
            self._window.setFocus(self._controls[0])
            return False
        else:
            return True


# Slider is not supported on Xbox using the Python API
if not XBMC4XBOX:
    class Slider(ControlMixin, xbmcgui.ControlSlider):
        """
        Slider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
        
        ControlSlider class.
        
        Implements a movable slider for adjusting some value.
        
        :param textureback: string -- image filename.
        :param texture: string -- image filename.
        :param texturefocus: string -- image filename.
        :param orientation: int -- slider orientation
        
        .. note:: After you create the control, you need to add it to the window with placeControl().
        
        Example::
        
            self.slider = Slider()
        """

        def __new__(cls, *args, **kwargs):
            textures = {'textureback': os.path.join(skin.images, 'Slider', 'osd_slider_bg.png'),
                        'texture': os.path.join(skin.images, 'Slider', 'osd_slider_nibNF.png'),
                        'texturefocus': os.path.join(skin.images, 'Slider', 'osd_slider_nib.png')}
            _set_textures(textures, kwargs)
            if xbmc.getInfoLabel('System.BuildVersion')[:2] >= '17':
                kwargs['orientation'] = xbmcgui.HORIZONTAL
            return super(Slider, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)


class AbstractWindow(AbstractGrid):
    """
    Top-level control window.
    
    The control windows serves as a parent widget for other XBMC UI controls
    much like Tkinter.Tk or PyQt QWidget class.
    
    This class is a basic "skeleton" for a control window.

    .. warning:: This is an abstract class and is not supposed to be instantiated directly!
    """

    def __init__(self):
        # GridMixin
        super(AbstractWindow, self).__init__(self)
        self.controls = []
        self.actions_connected = []
        self.controls_connected = []

    def autoNavigation(self, vertical_wrap_around=True,
                       horizontal_wrap_around=True, include_disabled=False,
                       include_invisible=False, controls_subset=None,
                       control_types=(Button, List, RadioButton) if XBMC4XBOX \
                               else (Button, List, RadioButton, Slider, Edit)):
        if controls_subset is None:
            controls = self.controls
        else:
            controls = controls_subset

        controls = [c for c in controls if \
                    (control_types == None or isinstance(c, control_types)) and \
                    (include_disabled or c.isEnabled()) and \
                    (include_invisible or c.isVisible())]

        # Note: coordinates are measured from the top left of the window
        # and a controls coordinates refer to its top left corner

        for control in controls:
            nearest_left = None
            nearest_right = None
            nearest_up = None
            nearest_down = None

            wrap_around_move_left = None
            wrap_around_move_right = None
            wrap_around_move_down = None
            wrap_around_move_up = None

            control_x = control.getX()
            control_y = control.getY()
            control_midpoint_x, control_midpoint_y = control.getMidpoint()
            control_width = control.getWidth()
            control_height = control.getHeight()

            for neighbour in controls:
                neighbour_x = neighbour.getX()
                neighbour_y = neighbour.getY()
                neighbour_midpoint_x, neighbour_midpoint_y = neighbour.getMidpoint()
                neighbour_midpoint_x_dif = abs(neighbour_midpoint_x - control_midpoint_x)
                neighbour_midpoint_y_dif = abs(neighbour_midpoint_y - control_midpoint_y)

                # Ensure that the neighbour is not too high or low
                if neighbour_y < control_y + control_height and neighbour_y + neighbour.getHeight() > control_y:
                    if neighbour_x < control_x and (nearest_left == None or nearest_left_x < neighbour_x or (
                            nearest_left_x == neighbour_x and neighbour_midpoint_y_dif < nearest_left_midpoint_y_dif)):
                        nearest_left = neighbour
                        nearest_left_x = neighbour_x
                        nearest_left_midpoint_y_dif = neighbour_midpoint_y_dif
                    elif neighbour_x > control_x and (nearest_right == None or nearest_right_x > neighbour_x or (
                            nearest_right_x == neighbour_x and neighbour_midpoint_y_dif < nearest_right_midpoint_y_dif)):
                        nearest_right = neighbour
                        nearest_right_x = neighbour_x
                        nearest_right_midpoint_y_dif = neighbour_midpoint_y_dif

                    if horizontal_wrap_around:
                        # check if nearest_left/right is none as if a suitable
                        # control to the left or right has been found there will
                        # be no wrap around
                        if nearest_left == None and neighbour_x > control_x and (
                                wrap_around_move_left == None or wrap_around_move_left_x < neighbour_x or (
                                wrap_around_move_left_x == neighbour_x and neighbour_midpoint_y_dif < wrap_around_move_left_midpoint_y_dif)):
                            wrap_around_move_left = neighbour
                            wrap_around_move_left_x = neighbour_x
                            wrap_around_move_left_midpoint_y_dif = neighbour_midpoint_y_dif
                        elif nearest_right == None and neighbour_x < control_x and (
                                wrap_around_move_right == None or wrap_around_move_right_x > neighbour_x or (
                                wrap_around_move_right_x == neighbour_x and neighbour_midpoint_y_dif < wrap_around_move_right_midpoint_y_dif)):
                            wrap_around_move_right = neighbour
                            wrap_around_move_right_x = neighbour_x
                            wrap_around_move_right_midpoint_y_dif = neighbour_midpoint_y_dif

                if neighbour_x < control_x + control_width and neighbour_x + neighbour.getWidth() > control_x:
                    if neighbour_y > control_y and (nearest_down == None or nearest_down_y > neighbour_y or (
                            nearest_down_y == neighbour_y and neighbour_midpoint_x_dif < nearest_down_midpoint_x_dif)):
                        nearest_down = neighbour
                        nearest_down_midpoint_x_dif = neighbour_midpoint_x_dif
                        nearest_down_y = neighbour_y
                    elif neighbour_y < control_y and (nearest_up == None or nearest_up_y < neighbour_y or (
                            nearest_up_y == neighbour_y and neighbour_midpoint_x_dif < nearest_up_midpoint_x_dif)):
                        nearest_up = neighbour
                        nearest_up_midpoint_x_dif = neighbour_midpoint_x_dif
                        nearest_up_y = neighbour_y

                    if vertical_wrap_around:
                        if nearest_down == None and neighbour_y < control_y and (
                                wrap_around_move_down == None or wrap_around_move_down_y > neighbour_y or (
                                wrap_around_move_down_y == neighbour_y and neighbour_midpoint_x_dif < wrap_around_move_down_midpoint_x_dif)):
                            wrap_around_move_down = neighbour
                            wrap_around_move_down_midpoint_x_dif = neighbour_midpoint_x_dif
                            wrap_around_move_down_y = neighbour_y
                        elif nearest_up == None and neighbour_y > control_y and (
                                wrap_around_move_up == None or wrap_around_move_up_y < neighbour_y or (
                                wrap_around_move_up_y == neighbour_y and neighbour_midpoint_x_dif < wrap_around_move_up_midpoint_x_dif)):
                            wrap_around_move_up = neighbour
                            wrap_around_move_up_midpoint_x_dif = neighbour_midpoint_x_dif
                            wrap_around_move_up_y = neighbour_y

            if nearest_left:
                control.controlLeft(nearest_left)
            elif wrap_around_move_left:
                control.controlLeft(wrap_around_move_left)

            if nearest_right:
                control.controlRight(nearest_right)
            elif wrap_around_move_right:
                control.controlRight(wrap_around_move_right)

            if nearest_down:
                control.controlDown(nearest_down)
            elif wrap_around_move_down:
                control.controlDown(wrap_around_move_down)

            if nearest_up:
                control.controlUp(nearest_up)
            elif wrap_around_move_up:
                control.controlUp(wrap_around_move_up)

    def setGeometry(self, width_, height_, rows_, columns_, pos_x=-1, pos_y=-1):
        """
        Set width, height, Grid layout, and coordinates (optional) for a new control window.
        
        :param width_: widgh of the created window.
        :param height_: height of the created window.
        :param rows_: # rows of the Grid layout to place controls on.
        :param columns_: # colums of the Grid layout to place controls on.
        :param pos_x: (opt) x coordinate of the top left corner of the window.
        :param pos_y: (opt) y coordinates of the top left corner of the window.
        
        If pos_x and pos_y are not privided, the window will be placed
        at the center of the screen.

        Example::
        
            self.setGeometry(400, 500, 5, 4)
        """
        self._width = width_
        self._height = height_
        self.rows = rows_
        self.columns = columns_
        if pos_x > 0 and pos_y > 0:
            self.x = pos_x
            self.y = pos_y
        else:
            self.x = 640 - width_ // 2
            self.y = 360 - height_ // 2
        self._setGrid()

    def getRows(self):
        """
        Get grid rows count.

        :raises: :class:`AddonWindowError` if a grid has not yet been set.
        """
        try:
            return self.rows  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Grid layout is not set! Call setGeometry first.')

    def getColumns(self):
        """
        Get grid columns count.

        :raises: :class:`AddonWindowError` if a grid has not yet been set.
        """
        try:
            return self.columns  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Grid layout is not set! Call setGeometry first.')

    def getX(self):
        """Get X coordinate of the top-left corner of the window."""
        try:
            return self.x # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getY(self):
        """Get Y coordinate of the top-left corner of the window."""
        try:
            return self.y # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getWindowWidth(self):
        """Get window width."""
        try:
            return self._width # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getWindowHeight(self):
        """Get window height."""
        try:
            return self._height # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def connect(self, event, callback):
        """
        Connect an event to a function.

        :param event: event to be connected.
        :param callback: callback object the event is connected to.

        An event can be an inctance of a Control object or an integer key action code.
        Several basic key action codes are provided by PyXBMCt. ``xbmcgui`` module
        provides more action codes.

        You can connect the following Controls: :class:`Button`, :class:`RadioButton`
        and :class:`List`. Other Controls do not generate any control events when activated
        so their connections won't work.

        To catch :class:`Slider` events you need to connect the following key actions:
        ``ACTION_MOVE_LEFT``, ``ACTION_MOVE_RIGHT`` and ``ACTION_MOUSE_DRAG``, and do a check
        whether the ``Slider`` instance is focused.

        ``callback`` parameter is a function or a method to be executed on when the event is fired.

        .. warning:: For connection you must provide a function object without brackets ``()``,
            not a function call!

        ``lambda`` can be used as to call another function or method with parameters known at runtime.

        Examples::

            self.connect(self.exit_button, self.close)

        or::

            self.connect(ACTION_NAV_BACK, self.close)
        """

        if isinstance(event, int):
            connect_list = self.actions_connected
        else:  # Event is actually a control
            if hasattr(event, "_connectCallback"):
                # Only connect the event if it returns true
                # or a new callable.
                should_connect = event._connectCallback(callback, self)
                if callable(should_connect):
                    callback = should_connect
                elif not should_connect:
                    return
            connect_list = self.controls_connected
        try:
            entry = next(entry for entry in connect_list if entry[0] == event)

            if not isinstance(entry[1], list):
                entry[1] = [entry[1], callback]
            else:
                entry[1].append(callback)
        except:
            connect_list.append([event, callback])

    def connectEventList(self, events, function):
        """
        Connect a list of controls/action codes to a function.

        See :meth:`connect` docstring for more info.
        """
        for event in events:
            self.connect(event, function)

    def disconnect(self, event, callback=None):
        """
        Disconnect an event from a function.

        An event can be an inctance of a Control object or an integer key action code
        which has previously been connected to a function or a method.

        :param event: event to be disconnected.
        :param callback: callback related to the event to be disconnected (if None then all callbacks are disconnected).
        :raises: :class:`AddonWindowError` if an event is not connected to any function.

        Examples::

            self.disconnect(self.exit_button)

        or::

            self.disconnect(ACTION_NAV_BACK)
        """
        if isinstance(event, int):
            event_list = self.actions_connected
        else:
            event_list = self.controls_connected

        for event_index in range(len(event_list)):
            if event == event_list[event_index][0]:
                if callback == None:
                    event_list.pop(event_index)
                    return
                else:
                    callback_list = event_list[event_index][1]
                    for callback_index in range(len(callback_list)):
                        if callback == callback_list[callback_index]:
                            callback_list.pop(callback_index)
                            return
                    raise AddonWindowError('The action or control %s is not connected to function!' % str(callback))

        raise AddonWindowError('The action or control %s is not connected!' % event)

    def disconnectEventList(self, events, callback=None):
        """
        Disconnect a list of controls/action codes from functions.

        See :func:`disconnect` docstring for more info.

        :param events: the list of events to be disconnected.
        :param callback: callback related to each of the events to be disconnected (if None then all callbacks are disconnected).
        :raises: :class:`AddonWindowError` if at least one event in the list
            is not connected to any function.
        """
        for event in events:
            self.disconnect(event, callback)

    def _executeConnected(self, event, connected_list):
        """
        Execute a connected event (an action or a control).

        This is a helper method not to be called directly.
        """
        for item in connected_list:
            if item[0] == event:
                if isinstance(item[1], list):
                    for callback in item[1]:
                        callback()
                else:
                    item[1]()
                break

    def setAnimation(self, control):
        """
        Set animation for control

        :param control: control for which animation is set.

        This method is called automatically to set animation properties for all controls
        added to the current addon window instance -- both for built-in controls
        (window background, title bar etc.) and for controls added with :meth:`placeControl`.

        It receives a control instance as the 2nd positional argument (besides ``self``).
        By default the method does nothing, i.e. no animation is set for controls.
        To add animation you need to re-implement this method in your child class.

        E.g::

            def setAnimation(self, control):
                control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=1000',),
                                        ('WindowClose', 'effect=fade start=100 end=0 time=1000',)])
        """
        pass


class AddonWindow(AbstractWindow):
    """
    Top-level control window.

    The control windows serves as a parent widget for other XBMC UI controls
    much like ``Tkinter.Tk`` or PyQt ``QWidget`` class.
    This is an abstract class which is not supposed to be instantiated directly
    and will raise exeptions. It is designed to be implemented in a grand-child class
    with the second inheritance from ``xbmcgui.Window`` or ``xbmcgui.WindowDialog``
    in a direct child class.

    This class provides a control window with a background and a header
    similar to top-level widgets of desktop UI frameworks.

    .. warning:: This is an abstract class and is not supposed to be instantiated directly!
    """

    def __init__(self, title=''):
        """Constructor method."""
        super(AddonWindow, self).__init__()
        self._setFrame(title)

    def _setFrame(self, title):
        """
        Set window frame

        Define paths to images for window background and title background textures,
        and set control position adjustment constants used in setGrid.

        This is a helper method not to be called directly.
        """
        # Window background image
        self.background_img = skin.background_img
        # Background for a window header
        self.title_background_img = skin.title_background_img
        self.background = xbmcgui.ControlImage(-10, -10, 1, 1, self.background_img)
        self.addControl(self.background)
        self.setAnimation(self.background)
        self.title_background = xbmcgui.ControlImage(-10, -10, 1, 1, self.title_background_img)
        self.addControl(self.title_background)
        self.setAnimation(self.title_background)
        self.title_bar = xbmcgui.ControlLabel(-10, -10, 1, 1, title, alignment=skin.header_align,
                                              textColor=skin.header_text_color, font='font13_title')
        self.addControl(self.title_bar)
        self.setAnimation(self.title_bar)
        self.window_close_button = xbmcgui.ControlButton(-100, -100, skin.close_btn_width, skin.close_btn_height, '',
                                                         focusTexture=skin.close_button_focus,
                                                         noFocusTexture=skin.close_button_no_focus)
        self.addControl(self.window_close_button)
        self.setAnimation(self.window_close_button)

    def setGeometry(self, width_, height_, rows_, columns_, pos_x=-1, pos_y=-1, padding=5):
        """
        Set width, height, Grid layout, and coordinates (optional) for a new control window.

        :param width_: new window width in pixels.
        :param height_: new window height in pixels.
        :param rows_: # of rows in the Grid layout to place controls on.
        :param columns_: # of colums in the Grid layout to place controls on.
        :param pos_x: (optional) x coordinate of the top left corner of the window.
        :param pos_y: (optional) y coordinate of the top left corner of the window.
        :param padding: (optional) padding between outer edges of the window
        and controls placed on it.

        If ``pos_x`` and ``pos_y`` are not privided, the window will be placed
        at the center of the screen.

        Example::

            self.setGeometry(400, 500, 5, 4)
        """
        self.win_padding = padding
        super(AddonWindow, self).setGeometry(width_, height_, rows_, columns_, pos_x, pos_y)
        self.background.setPosition(self.x, self.y)
        self.background.setWidth(self._width)
        self.background.setHeight(self._height)
        self.title_background.setPosition(self.x + skin.x_margin, self.y + skin.y_margin + skin.title_back_y_shift)
        self.title_background.setWidth(self._width - 2 * skin.x_margin)
        self.title_background.setHeight(skin.header_height)
        self.title_bar.setPosition(self.x + skin.x_margin + skin.title_bar_x_shift,
                                   self.y + skin.y_margin + skin.title_bar_y_shift)
        self.title_bar.setWidth(self._width - 2 * skin.x_margin)
        self.title_bar.setHeight(skin.header_height)
        self.window_close_button.setPosition(self.x + self._width - skin.close_btn_x_offset,
                                             self.y + skin.y_margin + skin.close_btn_y_offset)

    def _ifSetGeometryNotCalledRaiseError(self):
        """
        Helper method that raises an AddonWindowError  that states that setGeometry needs to be called. Used by methods
        that will fail if the window geometry is not defined.
        :raises AddonWindowError
        """
        raise  AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getGridX(self):
        try:
            val = self.x + self.win_padding
        except:
            self._ifSetGeometryNotCalledRaiseError()
        return val + skin.x_margin

    def getGridY(self):
        try:
            val = self.y + self.win_padding
        except:
            self._ifSetGeometryNotCalledRaiseError()
        return val + skin.y_margin + skin.title_back_y_shift + skin.header_height

    def getGridWidth(self):
        try:
            val = self._width - 2 * self.win_padding
        except:
            self._ifSetGeometryNotCalledRaiseError()
        return val - 2 * skin.x_margin

    def getGridHeight(self):
        try:
            val = self._height - 2 * self.win_padding
        except:
            self._ifSetGeometryNotCalledRaiseError()
        return val - skin.header_height - skin.title_back_y_shift - 2 * skin.y_margin

    def setWindowTitle(self, title=''):
        """
        Set window title.

        .. warning:: This method must be called **AFTER** (!!!) :meth:`setGeometry`,
            otherwise there is some werid bug with all skin text labels set to the ``title`` text.

        Example::

            self.setWindowTitle('My Cool Addon')
        """
        self.title_bar.setLabel(title)

    def getWindowTitle(self):
        """Get window title."""
        return self.title_bar.getLabel()

    def addControl(self, control):
        """
        Wrapper for xbmcgui.Window.addControl.

        :param control: the control to add.

        .. note:: In most circumstances you should use placeControl.
        .. note:: Only use this method if want to to place and element in a Group it using pixel coordinates

        Example::

            window.addControls(label)
        """
        self.controls.append(control)
        xbmcgui.Window.addControl(self, control)

    def addControls(self, controls):
        """
        Wrapper for xbmcgui.Window.addControls.

        :param controls: iterable containing the controls to add.

        .. note:: In most circumstances you should use placeControl.
        .. note:: Only use this method if want to to place and element in a Group it using pixel coordinates

        Example::

            window.addControls([label, button])
        """
        # addControls is not directly available on XBMC4XBOX
        # so this implementation is the most portable
        for control in controls:
            self.addControl(control)

    def removeControl(self, control):
        """
        Remove a control from the window grid layout.

        :param control: control instance to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        if hasattr(control, "_removedCallback"):
            control._removedCallback(self)
        xbmcgui.Window.removeControl(self, control)

    def removeControls(self, controls):
        """
        Remove multiple controls from the window grid layout.

        :param controls: an iterable of control instances to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        for control in controls:
            self.removeControl(control)

    def setFocus(self, control):
        do_set_focus = True
        if hasattr(control, '_focussedCallback'):
            do_set_focus = control._focussedCallback()
        if do_set_focus:
            xbmcgui.Window.setFocus(self, control)

    def onAction(self, action):
        """
        Catch button actions.

        :param action: an instance of :class:`xbmcgui.Action` class.
        """
        if action == ACTION_PREVIOUS_MENU:
            self.close()
        # On control is not called on XBMC4XBOX for subclasses of the built in
        # controls. However onAction is.
        elif XBMC4XBOX and hasattr(action, 'getButtonCode') and action.getButtonCode() in (
                KEY_BUTTON_A, ACTION_MOUSE_LEFT_CLICK):
            control = self.getFocus()
            if isinstance(control, (Button, RadioButton, List)) and control.isEnabled():
                self.onControl(control)
        else:
            self._executeConnected(action, self.actions_connected)

    def onControl(self, control):
        """
        Catch activated controls.

        :param control: is an instance of :class:`xbmcgui.Control` class.
        """
        if (hasattr(self, 'window_close_button') and
                control.getId() == self.window_close_button.getId()):
            self.close()
        else:
            self._executeConnected(control, self.controls_connected)

    def onFocus(self, control):
        """
        Catch focused controls.

        :param control: is an instance of :class:`xbmcgui.Control` class.
        """
        if hasattr(control, '_focussedCallback'):
            control._focussedCallback()


class BlankFullWindow(AbstractWindow, xbmcgui.Window):
    """
    BlankFullWindow()

    Addon UI container with a solid background.

    This is a blank window with a black background and without any elements whatsoever.
    The decoration and layout are completely up to an addon developer.
    The window controls can hide under video or music visualization.
    """
    pass


class BlankDialogWindow(AbstractWindow, xbmcgui.WindowDialog):
    """
    BlankDialogWindow()

    Addon UI container with a transparent background.

    This is a blank window with a transparent background and without any elements whatsoever.
    The decoration and layout are completely up to an addon developer.
    The window controls are always displayed over video or music visualization.
    """
    pass


class AddonFullWindow(AddonWindow, xbmcgui.Window):
    """
    AddonFullWindow(title='')

    Addon UI container with a solid background.

    ``AddonFullWindow`` instance is displayed on top of the main background image --
    ``self.main_bg`` -- and can hide behind a fullscreen video or music viaualisation.

    Minimal example::

        addon = AddonFullWindow('My Cool Addon')
        addon.setGeometry(400, 300, 4, 3)
        addon.doModal()
    """

    def __new__(cls, title='', *args, **kwargs):
        return super(AddonFullWindow, cls).__new__(cls, *args, **kwargs)

    def _setFrame(self, title):
        """
        Set the image for for the fullscreen background.
        """
        # Image for the fullscreen background.
        self.main_bg_img = skin.main_bg_img
        # Fullscreen background image control.
        self.main_bg = xbmcgui.ControlImage(1, 1, 1280, 720, self.main_bg_img)
        self.addControl(self.main_bg)
        super(AddonFullWindow, self)._setFrame(title)

    def setBackground(self, image=''):
        """
        Set the main bacground to an image file.

        :param image: path to an image file as str.

        Example::

            self.setBackground('/images/bacground.png')
        """
        self.main_bg.setImage(image)


class AddonDialogWindow(AddonWindow, xbmcgui.WindowDialog):
    """
    AddonDialogWindow(title='')

    Addon UI container with a transparent background.

    .. note:: ``AddonDialogWindow`` instance is displayed on top of XBMC UI,
        including fullscreen video and music visualization.

    Minimal example::

        addon = AddonDialogWindow('My Cool Addon')
        addon.setGeometry(400, 300, 4, 3)
        addon.doModal()
    """