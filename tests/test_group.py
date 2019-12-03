import unittest2
import mock
import sys
import itertools

sys.path.append("../script.module.pyxbmct/lib")
import pyxbmct

WINDOW_ROWS = 4
WINDOW_COLUMNS = 4
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class TestGroup(unittest2.TestCase):

    def setUp(self):
        self._window = pyxbmct.AddonFullWindow()
        self._window.getWidth = mock.MagicMock(return_value=WINDOW_WIDTH)
        self._window.getHeight = mock.MagicMock(return_value=WINDOW_HEIGHT)
        self._window.removeControl = mock.Mock(wraps=self._window.removeControl)

        self._window.setGeometry(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_ROWS, WINDOW_COLUMNS)

    def test_place_control_grid_not_placed(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        placed_callback = mock.MagicMock()
        removed_callback = mock.MagicMock()
        control._placedCallback = placed_callback
        control._removedCallback = removed_callback

        with self.subTest("AddonWindowError thrown"):
            with self.assertRaises(pyxbmct.AddonWindowError):
                group.placeControl(control, 0, 0)

        with self.subTest("Placed callback not called"):
            placed_callback.assert_not_called()

        with self.subTest("Removed callback not called"):
            placed_callback.assert_not_called()

    def test_place_and_remove_control_callbacks(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control._placedCallback = mock.MagicMock()
        control._removedCallback = mock.MagicMock()

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)

        with self.subTest("Removed callback not called (before removal)"):
            control._removedCallback.assert_not_called()

        group.removeControl(control)

        # Exact values and the fact that is called on placement are tested elsewhere
        with self.subTest("Placed callback called"):
            control._placedCallback.assert_called_once()

        with self.subTest("Control removed"):
            self._window.removeControl.assert_called_once_with(control)

        with self.subTest("Removed callback called once (after removal)"):
            control._removedCallback.assert_called_once_with(self._window)

    def test_remove_all_children(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control._removedCallback = mock.MagicMock()

        control2 = pyxbmct.Label(None, None, None, None, None, None)

        control3 = pyxbmct.Label(None, None, None, None, None, None)
        control3._removedCallback = mock.MagicMock()

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)
        group.placeControl(control2, 1, 0)
        group.placeControl(control3, 1, 1)

        # Added later so it they be called when the control is placed
        control2._placedCallback = mock.MagicMock()
        control3._placedCallback = mock.MagicMock()

        with self.subTest("Removed callback not called (before removal)"):
            control._removedCallback.assert_not_called()

        group.removeAllChildren()

        with self.subTest("Control removed"):
            self._window.removeControl.assert_any_call(control)
            self._window.removeControl.assert_any_call(control2)
            self._window.removeControl.assert_any_call(control3)
            self.assertEqual(self._window.removeControl.call_count, 3)

        with self.subTest("Removed callback called once on control that is removed (after removal)"):
            control._removedCallback.assert_called_once_with(self._window)

        with self.subTest("Placed callback not called (control that is removed)"):
            control2._placedCallback.assert_not_called()

        with self.subTest("Placed callback not called (control that is not removed)"):
            control3._placedCallback.assert_not_called()

        with self.subTest("Removed callback called (control that is removed)"):
            control3._removedCallback.assert_called_once_with(self._window)

    def test_remove_group_removes_all_children(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control._removedCallback = mock.MagicMock()

        control2 = pyxbmct.Label(None, None, None, None, None, None)

        control3 = pyxbmct.Label(None, None, None, None, None, None)
        control3._removedCallback = mock.MagicMock()

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)
        group.placeControl(control2, 1, 0)
        group.placeControl(control3, 1, 1)

        # Added later so it they be called when the control is placed
        control2._placedCallback = mock.MagicMock()
        control3._placedCallback = mock.MagicMock()

        with self.subTest("Removed callback not called (before removal)"):
            control._removedCallback.assert_not_called()

        self._window.removeControl(group)

        with self.subTest("Control removed"):
            self._window.removeControl.assert_any_call(control)
            self._window.removeControl.assert_any_call(control2)
            self._window.removeControl.assert_any_call(control3)
            self._window.removeControl.assert_any_call(group)
            self.assertEqual(self._window.removeControl.call_count, 4)

        with self.subTest("Removed callback called once on control that is removed (after removal)"):
            control._removedCallback.assert_called_once_with(self._window)

        with self.subTest("Placed callback not called (control that is removed)"):
            control2._placedCallback.assert_not_called()

        with self.subTest("Placed callback not called (control that is not removed)"):
            control3._placedCallback.assert_not_called()

        with self.subTest("Removed callback called (control that is removed)"):
            control3._removedCallback.assert_called_once_with(self._window)

    def test_set_visible(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control.setVisible = mock.MagicMock()

        control2 = pyxbmct.Label(None, None, None, None, None, None)
        control2.setVisible = mock.MagicMock()

        control3 = pyxbmct.Label(None, None, None, None, None, None)
        control3.setVisible = mock.MagicMock()

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)
        group.placeControl(control2, 1, 0)
        group.placeControl(control3, 1, 1)

        group.setVisible(False)

        with self.subTest("control1 setVisible called with False"):
            control.setVisible.assert_called_once_with(False)

        with self.subTest("control2 setVisible called with False"):
            control2.setVisible.assert_called_once_with(False)

        with self.subTest("control3 setVisible called with False"):
            control3.setVisible.assert_called_once_with(False)

        group.setVisible(True)

        with self.subTest("control1 setVisible called with True"):
            control.setVisible.assert_called_with(True)

        with self.subTest("control2 setVisible called with True"):
            control2.setVisible.assert_called_with(True)

        with self.subTest("control3 setVisible called with True"):
            control3.setVisible.assert_called_with(True)

        with self.subTest("control1 setVisible called exactly twice"):
            self.assertEqual(control.setVisible.call_count, 2)

        with self.subTest("control2 setVisible called exactly twice"):
            self.assertEqual(control2.setVisible.call_count, 2)

        with self.subTest("control3 setVisible called exactly twice"):
            self.assertEqual(control3.setVisible.call_count, 2)

    def test_set_enabled(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control.setEnabled = mock.MagicMock()

        control2 = pyxbmct.Label(None, None, None, None, None, None)
        control2.setEnabled = mock.MagicMock()

        control3 = pyxbmct.Label(None, None, None, None, None, None)
        control3.setEnabled = mock.MagicMock()

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)
        group.placeControl(control2, 1, 0)
        group.placeControl(control3, 1, 1)

        group.setEnabled(False)

        with self.subTest("control1 setVisible called with False"):
            control.setEnabled.assert_called_once_with(False)

        with self.subTest("control2 setVisible called with False"):
            control2.setEnabled.assert_called_once_with(False)

        with self.subTest("control3 setVisible called with False"):
            control3.setEnabled.assert_called_once_with(False)

        group.setEnabled(True)

        with self.subTest("control1 setVisible called with True"):
            control.setEnabled.assert_called_with(True)

        with self.subTest("control2 setVisible called with True"):
            control2.setEnabled.assert_called_with(True)

        with self.subTest("control3 setVisible called with True"):
            control3.setEnabled.assert_called_with(True)

        with self.subTest("control1 setVisible called exactly twice"):
            self.assertEqual(control.setEnabled.call_count, 2)

        with self.subTest("control2 setVisible called exactly twice"):
            self.assertEqual(control2.setEnabled.call_count, 2)

        with self.subTest("control3 setVisible called exactly twice"):
            self.assertEqual(control3.setEnabled.call_count, 2)

    def test_remove_controls(self):
        group = pyxbmct.Group(2, 4)

        control = pyxbmct.Label(None, None, None, None, None, None)
        control._removedCallback = mock.MagicMock()

        control2 = pyxbmct.Label(None, None, None, None, None, None)

        control3 = pyxbmct.Label(None, None, None, None, None, None)
        control3._removedCallback = mock.MagicMock()

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)
        group.placeControl(control2, 1, 0)
        group.placeControl(control3, 1, 1)

        # Added later so it they be called when the control is placed
        control2._placedCallback = mock.MagicMock()
        control3._placedCallback = mock.MagicMock()

        with self.subTest("Removed callback not called (before removal)"):
            control._removedCallback.assert_not_called()

        group.removeControls((control, control2))

        with self.subTest("Control removed"):
            self._window.removeControl.assert_any_call(control)
            self._window.removeControl.assert_any_call(control2)
            self.assertEqual(self._window.removeControl.call_count, 2)

        with self.subTest("Removed callback called once on control that is removed (after removal)"):
            control._removedCallback.assert_called_once_with(self._window)

        with self.subTest("Placed callback not called (control that is removed)"):
            control2._placedCallback.assert_not_called()

        with self.subTest("Placed callback not called (control that is not removed)"):
            control3._placedCallback.assert_not_called()

        with self.subTest("Removed callback not called (control that is not removed)"):
            control3._removedCallback.assert_not_called()

    def test_remove_control_without_callbacks(self):
        rows = 2
        columns = 4
        group = pyxbmct.Group(rows, columns)

        control = pyxbmct.Label(None, None, None, None, None, None)

        self._window.placeControl(group, 0, 0)
        group.placeControl(control, 0, 0)

        self._window.removeControl = mock.MagicMock()
        group.removeControl(control)

        with self.subTest("Control removed"):
            self._window.removeControl.assert_called_once_with(control)

    def test_place_control_coordinates_and_dimensions(self):
        self._window.addControl = mock.MagicMock()

        for group_row, group_col, rows, columns in ((0, 0, 4, 3), (1, 2, 5, 5), (3, 2, 4, 10)):
            with self.subTest("Group coordinates and size", group_row=group_row, group_col=group_col, rows=rows,
                              columns=columns):
                group = pyxbmct.Group(rows, columns)

                group.getX = mock.MagicMock(return_value=4)
                group.getY = mock.MagicMock(return_value=4)
                group.getWidth = mock.MagicMock(return_value=100)
                group.getHeight = mock.MagicMock(return_value=300)

                group_x = group.getX()
                group_y = group.getY()

                group_width = group.getWidth()
                group_height = group.getHeight()

                self._window.placeControl(group, group_row, group_col)

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

                        group.placeControl(control, row, column, rowspan=row_span, columnspan=column_span, pad_x=pad_x,
                                           pad_y=pad_y)

                        with self.subTest("Control added to window"):
                            self._window.addControl.assert_called_with(control)

                        with self.subTest("Test coordinates"):
                            expected_x = group_x + pad_x + ((group_width // columns) * column)
                            expected_y = group_y + pad_y + ((group_height // rows) * row)
                            control.setPosition.assert_called_with(expected_x, expected_y)

                        with self.subTest("Test width"):
                            expected_width = ((group_width // columns) * column_span) - (2 * pad_x)
                            control.setWidth.assert_called_with(expected_width)

                        with self.subTest("Test height"):
                            expected_height = ((group_height // rows) * row_span) - (2 * pad_y)
                            control.setHeight.assert_called_with(expected_height)

                        if with_placed_callback:
                            with self.subTest("Placed callback called"):
                                control._placedCallback.assert_called_once_with(self._window, row, column, row_span,
                                                                        column_span, pad_x, pad_y)


if __name__ == '__main__':
    unittest2.main()
