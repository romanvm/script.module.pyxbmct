# -*- coding: utf-8 -*-
# PyXBMCt framework module
#
# PyXBMCt is a mini-framework for creating Kodi (XBMC) Python addons
# with arbitrary UI made of Controls - decendants of xbmcgui.Control class.
# The framework uses image textures from Kodi Confluence skin.
#
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>
"""
This module contains all the controls of the PyXBMCt framework
"""

from __future__ import absolute_import, division, unicode_literals
import inspect
import os
from abc import ABCMeta, abstractmethod
from .addonskin import skin
from .abstractgrid import AbstractGrid
from .addonwindowerror import AddonWindowError
from .kodiconstants import *
from .xbmc4xbox import isXBMC4XBOX

_XBMC4XBOX = isXBMC4XBOX()

# typing module only needed when running pytype and is not available on XBMC4XBOX AFAIK
TYPE_CHECKING = False
try:
    import typing

    if typing.TYPE_CHECKING:
        TYPE_CHECKING = typing.TYPE_CHECKING
except:
    pass

# kodi_six doesn't work on
if _XBMC4XBOX:
    import xbmc, xbmcgui
else:
    from kodi_six import xbmc, xbmcgui
    from six import with_metaclass


def _set_textures(textures, kwargs):
    """Set texture arguments for controls."""
    for texture in textures:
        if kwargs.get(texture) is None:
            kwargs[texture] = textures[texture]


class ControlWithConnectCallback(object if _XBMC4XBOX else with_metaclass(ABCMeta, object)):
    """Abstract mixin class for controls that require a callback before events are connected to them"""

    if _XBMC4XBOX:
        __metaclass__ = ABCMeta

    @abstractmethod
    def _connectCallback(self, callback, window):
        """
        Called just before an event is connected to a control.
        If true is returned callback is connected to the control.
        If false is returned it is not.
        If a new callback is returned then that is connected instead.
        :param callback: the callback that is to be associated with the control
        :param window: the window on which the connect method was called
        """
        # type: (typing.Callable, xbmcgui.Window) -> typing.Union[bool, typing.Callable]
        raise NotImplementedError


class ControlWithPlacedCallback(object if _XBMC4XBOX else with_metaclass(ABCMeta, object)):
    """Abstract mixin class for controls that require a callback after they have been placed"""

    if _XBMC4XBOX:
        __metaclass__ = ABCMeta

    @abstractmethod
    def _placedCallback(self, window, row, column, rowspan, columnspan, pad_x, pad_y):
        """
        Called after the control has been placed in a Window or Group.
        :param window: the window in which the control has been placed
        :param row: the row in which the control was placed (top left corner)
        :param column: the column in which the control was placed (top left corner)
        :param rowspan: the number of rows that the control takes up
        :param columnspan: the number of columns that the control takes up
        :param pad_x: the number of pixels of padding inside the cell around the left and right sides of the control
        :param pad_y: the number of pixels of padding inside the cell around the top and bottom sides of the control
        """
        # type: (xbmcgui.Window, int, int, int, int, int, int) -> None
        raise NotImplementedError


class ControlWithRemovedCallback(object if _XBMC4XBOX else with_metaclass(ABCMeta, object)):
    """Abstract mixin class for controls that require a callback before they are removed"""

    if _XBMC4XBOX:
        __metaclass__ = ABCMeta

    @abstractmethod
    def _removedCallback(self, window):
        """
        Called just before a control is removed from the window
        :param window: The window the control is being removed from
        """
        # type: (xbmcgui.Window) -> None
        raise NotImplementedError


class ControlWithFocusedCallback(object if _XBMC4XBOX else with_metaclass(ABCMeta, object)):
    """Abstract mixin class for controls that require a callback before events are connected to them"""

    if _XBMC4XBOX:
        __metaclass__ = ABCMeta

    @abstractmethod
    def _focusedCallback(self):
        """
        Called when a control is focused either by manually calling Window.setFocus or
        by the user navigating to it.
        :returns The return value is only used when setFocus is called. If false the control won't be focused on.
        """
        # type: () -> bool
        raise NotImplementedError


# Inheritance for the sake of pytype seeing getX etc.
# xbmcgui.Control does not exist on XBMC4XBOX and inheriting from it on
# other platforms causes issues when calling the super constructor from
# any of the control classes below as it ends up Control's constructor
class ControlMixin(xbmcgui.Control if TYPE_CHECKING else object):
    """
    Basic control functionality mixin.

    Provides utility methods and wrappers for some existing methods to support PyXBMCt

    .. warning:: This is a mixin class and is not supposed to be instantiated directly!
    """

    def __eq__(self, other):
        if hasattr(other, 'getId'):
            return self.getId() == other.getId()
        return False

    def _getControlClass(self):
        if hasattr(self, '_controlClass'):
            return self._controlClass

        for ancestor in inspect.getmro(self.__class__):
            if inspect.getmodule(ancestor) == inspect.getmodule(xbmcgui):
                self._controlClass = ancestor
                return ancestor

        raise AddonWindowError("Could not find Control class")

    def isEnabled(self):
        """
        Determine if a control is enabled or not.

        Example::

            enabled = self.isEnabled()
        """
        # type: () -> bool
        # Test this way so that a constructor is not needed
        # to set the intial values
        return not hasattr(self, "_is_enabled") or self._is_enabled

    if _XBMC4XBOX:
        def isVisible(self):
            """
            Determine if the control is visible or not.

            Example::

                enabled = self.isVisible()
            """
            # type: () -> bool
            return not hasattr(self, "_is_visible") or self._is_visible

        def getX(self):
            # type: () -> int
            return self.getPosition()[0]

        def getY(self):
            # type: () -> int
            return self.getPosition()[1]

        def setVisible(self, is_visible):
            """
            Set whether the control is visible or not.

            :param is_visible: boolean to determine if the control is visible.

            Example::

                self.setVisible(False)
            """
            # type: (bool) -> None
            self._is_visible = is_visible
            self._getControlClass().setVisible(self, is_visible)

    def setEnabled(self, is_enabled):
        """
        Set whether the control is enabled or not.

        :param is_enabled: boolean to determine if the control is enabled.

        Example::

            self.setEnabled(False)
        """
        # type: (bool) -> None
        self._is_enabled = is_enabled
        self._getControlClass().setEnabled(self, is_enabled)

    def getMidpoint(self):
        """
        Get the (x,y) coordinates of the controls midpoint.

        Example::

            x, y = self.getMidpoint()
        """
        # type: () -> typing.Tuple[int, int]
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
        if not _XBMC4XBOX and xbmc.getInfoLabel('System.BuildVersion')[:2] >= '13':
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
if not _XBMC4XBOX:
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


class Group(ControlMixin, xbmcgui.ControlGroup, AbstractGrid, ControlWithPlacedCallback, ControlWithFocusedCallback,
            ControlWithRemovedCallback):
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
        # type: (int, int, typing.Any, typing.Any) -> None
        return super(Group, cls).__new__(cls, -10, -10, 1, 1, *args, **kwargs)

    def __init__(self, rows, columns, *args, **kwargs):
        # type: (int, int, typing.Any, typing.Any) -> None
        self._rows = rows
        self._columns = columns
        self._controls = []
        self._window = None

    def getWindow(self):
        # type: () -> xbmcgui.Window
        if not self._window:
            raise AddonWindowError("Group not placed!")
        else:
            return self._window

    def getGridX(self):
        # type: () -> int
        return self.getX()

    def getGridY(self):
        # type: () -> int
        return self.getY()

    def getGridWidth(self):
        # type: () -> int
        return self.getWidth()

    def getGridHeight(self):
        # type: () -> int
        return self.getHeight()

    def getRows(self):
        """
        Get grid rows count.
        """
        # type: () -> int
        return self._rows

    def getColumns(self):
        """
        Get grid columns count.
        """
        # type: () -> int
        return self._columns

    def addControl(self, control):
        # type: (xbmcgui.Control) -> None
        # getWindow will throw an error if the Group is not placed
        self.getWindow().addControl(control)
        self._controls.append(control)

    def setAnimation(self, control):
        # type: (xbmcgui.Control) -> None
        self._window.setAnimation(control)

    def _removedCallback(self, window):
        self.removeAllChildren()
        self._window = None

    def removeControl(self, control):
        """
        Remove a control from the window grid layout.

        :param control: control instance to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        # type: (xbmcgui.Control) -> None
        # getWindow will throw an error if Group is not placed
        self.getWindow().removeControl(control)
        self._controls.remove(control)

    def removeControls(self, controls):
        """
        Remove multiple controls from the window grid layout.

        :param controls: an iterable of control instances to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        # type: (typing.Iterable[xbmcgui.Control]) -> None
        # Need to copy the list of controls as we are changing
        # its size whilst iterating over it
        for control in list(controls):
            self.removeControl(control)

    def removeAllChildren(self):
        """
        Removes all the Group's children (and all their children) from the window.

        Example::

            group.removeAllChildren()
        """
        # type: () -> None
        self.removeControls(self._controls)

    def setVisible(self, is_visible):
        """
        Sets the group (and it all its current children) to be either visible or invisible.

        :param is_visible: determines whether or the group and its current children should be visible or not.

        Example::

            group.setVisible(False)
        """
        # type: (bool) -> None
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
        # type: (bool) -> None
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
        self._window = window

    def _focusedCallback(self):
        # type: () -> bool
        # Want to divert focus to the first control if possible
        # it doesn't really make sense for a container to have focus
        if self._controls:
            self._window.setFocus(self._controls[0])
            return False
        else:
            return True


# Slider is not supported on Xbox using the Python API
if not _XBMC4XBOX:
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
