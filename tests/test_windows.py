# -*- coding: utf-8 -*-
# PyXBMCt framework module
#
# PyXBMCt is a mini-framework for creating Kodi (XBMC) Python addons
# with arbitrary UI made of Controls - decendants of xbmcgui.Control class.
# The framework uses image textures from Kodi Confluence skin.
#
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>
"""
This test case is for pyxbmct.AddonFullWindow and pyxbmct.AddonDialogWindow.
One test case is used for both classes as they are so similar as they only differ visually.
"""

import unittest2
import mock
import itertools
import pyxbmct

skin = pyxbmct.Skin()


class TestGroup(unittest2.TestCase):
    """
    This test case is for pyxbmct.AddonFullWindow and pyxbmct.AddonDialogWindow
    """

    def setUp(self):
        window_rows = 4
        window_columns = 4
        window_width = 1280
        window_height = 720

        self._window = pyxbmct.AddonFullWindow()
        self._window.getWidth = mock.MagicMock(return_value=window_width)
        self._window.getHeight = mock.MagicMock(return_value=window_height)

    def test_set_focus_no_focus_callback(self):
        label = pyxbmct.Label(None, None, None, None, None, None)

        with mock.patch('xbmcgui.Window.setFocus') as xbmcgui_window_set_focus:
            self._window.setFocus(label)
            xbmcgui_window_set_focus.assert_called_once_with(self._window, label)

    def test_set_focus_focus_callback_returns_false(self):
        label = pyxbmct.Label(None, None, None, None, None, None)
        label._focusedCallback = mock.MagicMock(return_value=False)

        with mock.patch('xbmcgui.Window.setFocus') as xbmcgui_window_set_focus:
            self._window.setFocus(label)
            with self.subTest("Focused callback called"):
                label._focusedCallback.assert_called_once_with()  # no arguments
            with self.subTest("Control not focused on"):
                xbmcgui_window_set_focus.assert_not_called()

    def test_set_focus_focus_callback_returns_true(self):
        label = pyxbmct.Label(None, None, None, None, None, None)
        label._focusedCallback = mock.MagicMock(return_value=True)

        with mock.patch('xbmcgui.Window.setFocus') as xbmcgui_window_set_focus:
            self._window.setFocus(label)
            with self.subTest("Focused callback called"):
                label._focusedCallback.assert_called_once_with()  # no arguments
            with self.subTest("Control not focused on"):
                xbmcgui_window_set_focus.assert_called_once_with(self._window, label)

    def test_connect_callback_returns_false(self):
        self._window.setGeometry(400, 300, 3, 3)
        label = pyxbmct.Label(None, None, None, None, None, None)
        label.getId = lambda: 12
        self._window.placeControl(label, 1, 1)

        callable = mock.MagicMock()
        label._connectCallback = mock.MagicMock(return_value=False)
        self._window.connect(label, callable)

        with self.subTest("Callable not called when attached"):
            callable.assert_not_called()

        with self.subTest("Callable not called"):
            self._window.onControl(label)
            callable.assert_not_called()

        with self.subTest("Cannot disconnect"):
            with self.assertRaises(pyxbmct.AddonWindowError):
                self._window.disconnect(label, callable)

    def test_connect_callback_returns_new_callable(self):
        self._window.setGeometry(400, 300, 3, 3)
        label = pyxbmct.Label(None, None, None, None, None, None)
        label.getId = lambda: 12
        self._window.placeControl(label, 1, 1)

        callable = mock.MagicMock()
        new_callable = mock.MagicMock()
        label._connectCallback = mock.MagicMock(return_value=new_callable)
        self._window.connect(label, callable)

        with self.subTest("Orginal callable not called when attached"):
            callable.assert_not_called()

        with self.subTest("New callable not called when attached"):
            callable.assert_not_called()

        with self.subTest("Orginal callable not called"):
            self._window.onControl(label)
            callable.assert_not_called()

        with self.subTest("Callable called"):
            new_callable.assert_called_once_with()

    def test_connect_callable_returns_true(self):
        self._window.setGeometry(400, 300, 3, 3)
        label = pyxbmct.Label(None, None, None, None, None, None)
        label.getId = lambda: 12
        self._window.placeControl(label, 1, 1)

        callable = mock.MagicMock()
        label._connectCallback = mock.MagicMock(return_value=True)

        self._window.connect(label, callable)

        with self.subTest("Callback called"):
            label._connectCallback.assert_called_once_with(callable, self._window)

        with self.subTest("Callable not called when attached"):
            callable.assert_not_called()

        with self.subTest("Callable called"):
            self._window.onControl(label)
            callable.assert_called_once_with()

        with self.subTest("Callable not called once disconnected"):
            self._window.disconnect(label, callable)
            callable.assert_called_once_with()  # Not called again

    def test_connect_callable_multiple_callbacks(self):
        self._window.setGeometry(400, 300, 3, 3)
        label = pyxbmct.Label(None, None, None, None, None, None)
        label.getId = lambda: 12
        self._window.placeControl(label, 1, 1)

        callable = mock.MagicMock()
        callable2 = mock.MagicMock()
        label._connectCallback = mock.MagicMock(return_value=True)

        self._window.connect(label, callable)
        self._window.connect(label, callable2)

        self._window.onControl(label)
        with self.subTest("Callable called"):
            callable.assert_called_once_with()

        with self.subTest("Callable 2 called"):
            callable2.assert_called_once_with()

        with self.subTest("Can disconnect callable 2"):
            self._window.disconnect(label, callable2)

        self._window.onControl(label)
        with self.subTest("Callable 2 not called once disconnected"):
            self.assertEqual(callable.call_count, 2)  # Called again
            callable2.assert_called_once_with()  # Not called again

        with self.subTest("Callable 2 re-connected, callable 1 disconnected"):
            self._window.connect(label, callable2)
            self._window.disconnect(label, callable)
            self._window.onControl(label)

            self.assertEqual(callable.call_count, 2)  # Not called again
            self.assertEqual(callable.call_count, 2)  # Called again

        with self.subTest("Callable 2 re-disconnected, not called again"):
            self._window.disconnect(label, callable2)
            self._window.onControl(label)

            self.assertEqual(callable.call_count, 2)  # Not called again
            self.assertEqual(callable.call_count, 2)  # Not called again

    def test_place_control_set_geometry_not_called(self):
        """
        Ensure that controls can't be placed in a Window when setGeometry has not yet been called
        """

        control = pyxbmct.Label(None, None, None, None, None, None)
        control._placedCallback = mock.MagicMock()
        control._removedCallback = mock.MagicMock()

        with self.subTest("AddonWindowError thrown"):
            with self.assertRaises(pyxbmct.AddonWindowError):
                self._window.placeControl(control, 0, 0)

        with self.subTest("Placed callback not called"):
            control._placedCallback.assert_not_called()

        with self.subTest("Removed callback not called"):
            control._removedCallback.assert_not_called()

    def test_place_and_remove_control_callbacks(self):
        """
        Ensure that controls place and remove callbacks are called (only) when they are placed or removed
        """
        control = pyxbmct.Label(None, None, None, None, None, None)
        control._placedCallback = mock.MagicMock()
        control._removedCallback = mock.MagicMock()

        self._window.setGeometry(400, 300, 3, 3)

        self._window.placeControl(control, 0, 0)

        with self.subTest("Removed callback not called (before removal)"):
            control._removedCallback.assert_not_called()

        self._window.removeControl(control)

        # Exact values and the fact that is called on placement are tested elsewhere
        with self.subTest("Placed callback called"):
            control._placedCallback.assert_called_once()

        with self.subTest("Removed callback called once (after removal)"):
            control._removedCallback.assert_called_once_with(self._window)

    def test_remove_controls(self):
        """
        Tests pyxbmct.AddonFullWindow.removeControls. Ensures that only the correct controls are removed and the only
        the removed callbacks that are called are the ones for those controls, and that they are called with the correct
        parameters.
        """

        self._window.setGeometry(1000, 500, 7, 8)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control._removedCallback = mock.MagicMock()

        control2 = pyxbmct.Label(None, None, None, None, None, None)

        control3 = pyxbmct.Label(None, None, None, None, None, None)
        control3._removedCallback = mock.MagicMock()

        control4 = pyxbmct.Label(None, None, None, None, None, None)
        control4._removedCallback = mock.MagicMock()

        self._window.placeControl(control, 0, 0)
        self._window.placeControl(control2, 1, 0)
        self._window.placeControl(control3, 1, 1)
        self._window.placeControl(control4, 2, 1)

        # Added later so it they be called when the control is placed
        control2._placedCallback = mock.MagicMock()
        control3._placedCallback = mock.MagicMock()

        with self.subTest("Removed callback not called (before removal)"):
            control._removedCallback.assert_not_called()

        with self.subTest("Removed callback not called (before removal)"):
            control4._removedCallback.assert_not_called()

        with mock.patch('xbmcgui.Window.removeControl') as xbmcgui_window_remove_control:
            self._window.removeControls((control, control2, control4))

            with self.subTest("Control removed"):
                xbmcgui_window_remove_control.assert_any_call(self._window, control)
                xbmcgui_window_remove_control.assert_any_call(self._window, control2)
                xbmcgui_window_remove_control.assert_any_call(self._window, control4)
                self.assertEqual(xbmcgui_window_remove_control.call_count, 3)

        with self.subTest("Removed callback called once on control that is removed (after removal)"):
            control._removedCallback.assert_called_once_with(self._window)

        with self.subTest("Removed callback called once on control that is removed (after removal)"):
            control4._removedCallback.assert_called_once_with(self._window)

        with self.subTest("Placed callback not called (control that is removed)"):
            control2._placedCallback.assert_not_called()

        with self.subTest("Placed callback not called (control that is not removed)"):
            control3._placedCallback.assert_not_called()

        with self.subTest("Removed callback not called (control that is not removed)"):
            control3._removedCallback.assert_not_called()

    def test_remove_control_without_callbacks(self):
        """
        Tests Window.removeControl. Ensures that controls can be removed from the window even if they don't have removed
        callbacks.
        """

        control = pyxbmct.Label(None, None, None, None, None, None)
        self._window.setGeometry(400, 500, 3, 3)
        self._window.placeControl(control, 1, 1)

        with mock.patch('xbmcgui.Window.removeControl') as xbmcgui_window_remove_control:
            self._window.removeControl(control)
            xbmcgui_window_remove_control.assert_called_once_with(self._window, control)

        self._window.removeControl(control)

    def test_place_control_coordinates_and_dimensions(self):
        """
        Tests pyxbmct.AddonFullWindow.placeControl. Ensures that controls are placed at the correct screen coordinates
        with the correct dimensions based on the dimensions of the Window, and the location of the Window
        """

        for window_width, window_height, rows, columns, window_x, window_y, window_padding in (
                (100, 50, 2, 4, 0, 0, 0), (121, 502, 3, 5, -10, 21, 5), (1000, 502, 8, 3, 205, 0, 20),
                (786, 82, 8, 3, 0, 91, 0)):
            with self.subTest("Window coordinates, dimensions and grid size", window_width=window_width,
                              window_height=window_height, rows=rows, columns=columns, window_x=window_x,
                              window_y=window_y):
                window = pyxbmct.AddonFullWindow()
                window.setGeometry(window_width, window_height, rows, columns, pos_x=window_x, pos_y=window_y,
                                   padding=window_padding)

                if not (window_x > 0 and window_y > 0):
                    window_x = 640 - window_width // 2
                    window_y = 360 - window_height // 2

                grid_x = window_x + skin.x_margin + window_padding
                grid_y = window_y + skin.y_margin + skin.title_back_y_shift + skin.header_height + window_padding
                grid_width = window_width - 2 * (skin.x_margin + window_padding)
                grid_height = window_height - (skin.header_height + skin.title_back_y_shift + 2 * (
                        skin.y_margin + window_padding))
                cell_width = (grid_width // columns)
                cell_height = (grid_height // rows)

                for row, column, pad_x, pad_y, column_span, row_span, with_placed_callback in itertools.product(
                        range(rows), range(columns), range(-2, 2), range(-2, 2), range(1, 3), range(1, 3),
                        (True, False)):
                    with self.subTest("Call parameters", row=row, column=column, pad_x=pad_x, pad_y=pad_y,
                                      column_span=column_span, row_span=row_span,
                                      with_placed_callback=with_placed_callback):
                        # complains about no. of args (I think because of Kodi stubs?)
                        control = pyxbmct.Label(None, None, None, None, None, None)

                        control.setPosition = mock.MagicMock()
                        control.setWidth = mock.MagicMock()
                        control.setHeight = mock.MagicMock()

                        if with_placed_callback:
                            control._placedCallback = mock.MagicMock()

                        with mock.patch('xbmcgui.Window.addControl') as xbmcgui_window_add_control:
                            window.placeControl(control, row, column, rowspan=row_span, columnspan=column_span,
                                                pad_x=pad_x, pad_y=pad_y)
                            with self.subTest("Control added to window"):
                                xbmcgui_window_add_control.assert_called_once_with(window, control)

                        with self.subTest("Test coordinates"):
                            expected_x = grid_x + pad_x + (cell_width * column)
                            expected_y = grid_y + pad_y + (cell_height * row)
                            control.setPosition.assert_called_with(expected_x, expected_y)

                        with self.subTest("Test width"):
                            expected_width = (cell_width * column_span) - (2 * pad_x)
                            control.setWidth.assert_called_with(expected_width)

                        with self.subTest("Test height"):
                            expected_height = (cell_height * row_span) - (2 * pad_y)
                            control.setHeight.assert_called_with(expected_height)

                        if with_placed_callback:
                            with self.subTest("Placed callback called"):
                                control._placedCallback.assert_called_once_with(window, row, column, row_span,
                                                                                column_span, pad_x, pad_y)


if __name__ == '__main__':
    unittest2.main()
