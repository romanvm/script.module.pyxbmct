# -*- coding: utf-8 -*-
# PyXBMCt framework module
#
# PyXBMCt is a mini-framework for creating Kodi (XBMC) Python addons
# with arbitrary UI made of Controls - decendants of xbmcgui.Control class.
# The framework uses image textures from Kodi Confluence skin.
#
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>
"""
This module contains all the Window classes of the PyXBMCt framework
"""

from __future__ import absolute_import, division, unicode_literals
import inspect
from abc import ABCMeta, abstractmethod
from .addonskin import skin
from .abstractgrid import AbstractGrid
from .addoncontrols import Button, List, RadioButton
from .addonwindowerror import AddonWindowError
from .kodiconstants import KEY_BUTTON_A, ACTION_PREVIOUS_MENU, ACTION_MOUSE_LEFT_CLICK
from .xbmc4xbox import isXBMC4XBOX

_XBMC4XBOX = isXBMC4XBOX()

# typing module only needed when running pytype and is not available on XBMC4XBOX AFAIK
try:
    import typing
except:
    pass

# kodi_six doesn't work on XBMC4XBOX
if _XBMC4XBOX:
    import xbmcgui
else:
    from .addoncontrols import Slider, Edit
    from six.moves import range
    from kodi_six import xbmcgui
    from six import with_metaclass


class AbstractWindow(AbstractGrid if _XBMC4XBOX else with_metaclass(ABCMeta, AbstractGrid)):
    """
    Top-level control window.

    The control windows serves as a parent widget for other XBMC UI controls
    much like Tkinter.Tk or PyQt QWidget class.

    This class is a basic "skeleton" for a control window.

    .. warning:: This is an abstract class and is not supposed to be instantiated directly!
    """

    if _XBMC4XBOX:
        __metaclass__ = ABCMeta

    def __init__(self):
        self._controls = []  # type: typing.List[xbmcgui.Control]
        self._actions_connected = []  # type: typing.List[typing.Tuple[typing.Union[int, xbmcgui.Control], typing.List[typing.Callable]]]
        self._controls_connected = []  # type: typing.List[typing.Tuple[typing.Union[int, xbmcgui.Control], typing.List[typing.Callable]]]
        # Need access to this class and this is not easy to obtain
        # as it is not the superclass of this one
        self._XBMCWindowClass = None
        for ancestor in inspect.getmro(self.__class__):
            if inspect.getmodule(ancestor) == inspect.getmodule(xbmcgui):
                self._XBMCWindowClass = ancestor
            # break
        if self._XBMCWindowClass is None:
            raise AddonWindowError("Could not find Window parent class")

    def getWindow(self):
        return self

    def autoNavigation(self, vertical_wrap_around=True,
                       horizontal_wrap_around=True, include_disabled=False,
                       include_invisible=False, controls_subset=None,
                       control_types=(Button, List, RadioButton) if _XBMC4XBOX \
                               else (Button, List, RadioButton, Slider, Edit)):
        """
        Automatically setup the navigation between controls in the Window

        :param vertical_wrap_around: if you navigate up from the topmost control it will take you to the bottommost control
        :param horizontal_wrap_around: if you navigate down from the bottommost control it will take you to the topmost control
        :param include_disabled: include controls that are disabled
        :param include_invisible: include controls that are currently not visible
        :param controls_subset: pass in a specific set of controls to set up the navigation for (only these controls will be effacted and then can will only be set up to navigate to each other)
        :param control_types: the types of controls to consider for the navigation
        """
        # type: (bool, bool, bool, bool, typing.Iterable[xbmcgui.Control], typing.Tuple[typing.Any, ...]) -> None
        if controls_subset is None:
            controls = self._controls
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
        # type: (int, int, int, int, int, int) -> None
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

    def getRows(self):
        """
        Get grid rows count.

        :raises: :class:`AddonWindowError` if a grid has not yet been set.
        """
        # type: () -> int
        try:
            return self.rows  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Grid layout is not set! Call setGeometry first.')

    def getColumns(self):
        """
        Get grid columns count.

        :raises: :class:`AddonWindowError` if a grid has not yet been set.
        """
        # type: () -> int
        try:
            return self.columns  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Grid layout is not set! Call setGeometry first.')

    def getX(self):
        """Get X coordinate of the top-left corner of the window."""
        # type: () -> int
        try:
            return self.x  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getY(self):
        """Get Y coordinate of the top-left corner of the window."""
        # type: () -> int
        try:
            return self.y  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getWindowWidth(self):
        """Get window width."""
        # type: () -> int
        try:
            return self._width  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getWindowHeight(self):
        """Get window height."""
        # type: () -> int
        try:
            return self._height  # pytype: disable=attribute-error
        except AttributeError:
            raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def connect(self, event, callback):
        """
        Connect an event to a function.

        :param event: event to be connected.
        :param callback: callback object the event is connected to.

        An event can be an instance of a Control object or an integer key action code.
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
        # type: (typing.Union[int, xbmcgui.Control], typing.Callable) -> None

        if isinstance(event, int):
            connect_list = self._actions_connected
        else:  # Event is actually a control
            if hasattr(event, "_connectCallback"):
                # Only connect the event if it returns true
                # or a new callable.
                should_connect = event._connectCallback(callback, self)
                if callable(should_connect):
                    callback = should_connect
                elif not should_connect:
                    return
            connect_list = self._controls_connected
        try:
            entry = next(entry for entry in connect_list if entry[0] == event)

            entry[1].append(callback)
        except:
            connect_list.append((event, [callback]))

    def connectEventList(self, events, callback):
        """
        Connect a list of controls/action codes to a function.

        See :meth:`connect` docstring for more info.
        """
        # type: (typing.List[typing.Union[int, xbmcgui.Control]], typing.Callable) -> None
        for event in events:
            self.connect(event, callback)

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
        # type: (typing.Union[int, xbmcgui.Control], typing.Callable) -> None
        if isinstance(event, int):
            event_list = self._actions_connected
        else:
            event_list = self._controls_connected

        for event_index in range(len(event_list)):
            if event == event_list[event_index][0]:
                if callback == None:
                    event_list.pop(event_index)
                    return
                else:
                    callback_list = event_list[event_index][1]
                    for callback_index in range(len(callback_list)):
                        if callback == callback_list[callback_index]:
                            if len(callback_list) == 1:
                                event_list.pop(event_index)
                            else:
                                callback_list.pop(callback_index)  # pytype: disable=attribute-error
                            return  # May leave an empty list
                    raise AddonWindowError('The action or control %s is not connected to function! %s' %
                                           (str(event), str(callback)))

        raise AddonWindowError('The action or control %s is not connected!' % str(event))

    def disconnectEventList(self, events, callback=None):
        """
        Disconnect a list of controls/action codes from functions.

        See :func:`disconnect` docstring for more info.

        :param events: the list of events to be disconnected.
        :param callback: callback related to each of the events to be disconnected (if None then all callbacks are disconnected).
        :raises: :class:`AddonWindowError` if at least one event in the list
            is not connected to any function.
        """
        # type: (typing.Iterable[typing.Union[int, xbmcgui.Control]], typing.Callable) -> None
        for event in events:
            self.disconnect(event, callback)

    def _executeConnected(self, event, connected_list):
        """
        Execute a connected event (an action or a control).

        This is a helper method not to be called directly.
        """
        # type: (typing.Union[int, xbmcgui.Control], typing.List[typing.Tuple[typing.Union[int, xbmcgui.Control], typing.List[typing.Callable]]]) -> None
        for item in connected_list:
            if item[0] == event:
                for callback in item[1]:
                    callback()
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
        # type: (xbmcgui.Control) -> None
        pass

    def setFocus(self, control):
        # type: (xbmcgui.Control) -> None
        do_set_focus = True
        if hasattr(control, '_focusedCallback'):
            do_set_focus = control._focusedCallback()
        if do_set_focus:
            self._XBMCWindowClass.setFocus(self, control)

    def onFocus(self, control):
        """
        Catch focused controls.

        :param control: is an instance of :class:`xbmcgui.Control` class.
        """
        # type: (xbmcgui.Control) -> None
        if hasattr(control, '_focusedCallback'):
            control._focusedCallback()

    def addControl(self, control):
        """
        Wrapper for xbmcgui.Window.addControl.

        :param control: the control to add.

        .. note:: In most circumstances you should use placeControl.
        .. note:: Only use this method if want to to place and element in a Group it using pixel coordinates

        Example::

            window.addControls(label)
        """
        # type: (xbmcgui.Control) -> None
        self._controls.append(control)
        self._XBMCWindowClass.addControl(self, control)

    def addControls(self, controls):
        """
        Wrapper for xbmcgui.Window.addControls.

        :param controls: iterable containing the controls to add.

        .. note:: In most circumstances you should use placeControl.
        .. note:: Only use this method if want to to place and element in a Group it using pixel coordinates

        Example::

            window.addControls([label, button])
        """
        # type: (typing.Iterable[xbmcgui.Control]) -> None
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
        # type: (xbmcgui.Control) -> None
        if hasattr(control, "_removedCallback"):
            control._removedCallback(self)
        self._XBMCWindowClass.removeControl(self, control)

    def removeControls(self, controls):
        """
        Remove multiple controls from the window grid layout.

        :param controls: an iterable of control instances to be removed from the grid.

        Example::

            self.removeControl(self.label)
        """
        # type: (typing.Iterable[xbmcgui.Control]) -> None
        for control in controls:
            self.removeControl(control)

    def onAction(self, action):
        """
        Catch button actions.

        :param action: an instance of :class:`xbmcgui.Action` class.
        """
        # type: (xbmcgui.Action) -> None
        if action == ACTION_PREVIOUS_MENU:
            self.close()  # pytype: disable=attribute-error
        # On control is not called on XBMC4XBOX for subclasses of the built in
        # controls. However onAction is.
        elif _XBMC4XBOX and hasattr(action, 'getButtonCode') and action.getButtonCode() in (
                KEY_BUTTON_A, ACTION_MOUSE_LEFT_CLICK):
            control = self.getFocus()  # pytype: disable=attribute-error
            if isinstance(control, (Button, RadioButton, List)) and control.isEnabled():
                self.onControl(control)
        else:
            self._executeConnected(action, self._actions_connected)

    def onControl(self, control):
        """
        Catch activated controls.

        :param control: is an instance of :class:`xbmcgui.Control` class.
        """
        # type: (xbmcgui.Control) -> None
        self._executeConnected(control, self._controls_connected)


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
        # type: (str) -> None
        super(AddonWindow, self).__init__()
        self._setFrame(title)

    def onControl(self, control):
        """
        Catch activated controls.

        :param control: is an instance of :class:`xbmcgui.Control` class.
        """
        # type: (xbmcgui.Control) -> None
        if (hasattr(self, 'window_close_button') and
                control.getId() == self.window_close_button.getId()):
            self.close()  # pytype: disable=attribute-error
        else:
            super(AddonWindow, self).onControl(control)

    def _setFrame(self, title):
        """
        Set window frame

        Define paths to images for window background and title background textures,
        and set control position adjustment constants used in setGrid.

        This is a helper method not to be called directly.
        """
        # type: (str) -> None
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
        # type: (int, int, int, int, int, int, int) -> None
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

    def _raiseSetGeometryNotCalledError(self):
        """
        Helper method that raises an AddonWindowError  that states that setGeometry needs to be called. Used by methods
        that will fail if the window geometry is not defined.
        :raises AddonWindowError
        """
        # type: () -> None
        raise AddonWindowError('Window geometry is not defined! Call setGeometry first.')

    def getGridX(self):
        # type: () -> int
        try:
            val = self.x + self.win_padding
        except AttributeError:
            self._raiseSetGeometryNotCalledError()
        return val + skin.x_margin

    def getGridY(self):
        # type: () -> int
        try:
            val = self.y + self.win_padding
        except AttributeError:
            self._raiseSetGeometryNotCalledError()
        return val + skin.y_margin + skin.title_back_y_shift + skin.header_height

    def getGridWidth(self):
        # type: () -> int
        try:
            val = self._width - 2 * self.win_padding
        except AttributeError:
            self._raiseSetGeometryNotCalledError()
        return val - 2 * skin.x_margin

    def getGridHeight(self):
        # type: () -> int
        try:
            val = self._height - 2 * self.win_padding
        except AttributeError:
            self._raiseSetGeometryNotCalledError()
        return val - skin.header_height - skin.title_back_y_shift - 2 * skin.y_margin

    def setWindowTitle(self, title=''):
        """
        Set window title.

        .. warning:: This method must be called **AFTER** (!!!) :meth:`setGeometry`,
            otherwise there is some werid bug with all skin text labels set to the ``title`` text.

        Example::

            self.setWindowTitle('My Cool Addon')
        """
        # type: (str) -> None
        self.title_bar.setLabel(title)

    def getWindowTitle(self):
        """Get window title."""
        # type: () -> str
        return self.title_bar.getLabel()


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
        # type: (str) -> None
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
        # type: (str) -> None
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
