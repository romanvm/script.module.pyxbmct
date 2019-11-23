import unittest2
import mock
import sys

sys.path.append("../script.module.pyxbmct/lib")
import pyxbmct

WINDOW_ROWS = 4
WINDOW_COLUMNS = 4
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 100


class TestGroup(unittest2.TestCase):

    def setUp(self):
        self._window = pyxbmct.AddonFullWindow()
        self._window.setGeometry(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_ROWS, WINDOW_COLUMNS)

    def test_place_control(self):
        rows = 4
        columns = 3

        group = pyxbmct.Group(rows, columns)
        self._window.placeControl(group, 0, 0)
        window_x = 0
        window_y = 0

        self._window.width = 1280
        self._window.height = 720
        self._window.getWidth = mock.MagicMock(return_value=self._window.width)
        self._window.getHeight = mock.MagicMock(return_value=self._window.height)

        group_width = group.getWidth()
        group_height = group.getHeight()

        self._window.addControl = mock.MagicMock()

        for row in range(rows):
            for column in range(columns):
                with self.subTest("Coordinates", row=row, column=column):
                    for pad_x in range(-2, 2):
                        for pad_y in range(-2, 2):
                            with self.subTest("Padding", pad_x=pad_x, pad_y=pad_y):
                                for column_span in range(1, 3):
                                    for row_span in range(1, 3):
                                        with self.subTest("Column span", column_span=column_span):
                                            with self.subTest("Row span", row_span=row_span):
                                                # complains about no. of args (I think because of Kodi stubs?)
                                                control = pyxbmct.Label(None, None, None, None, None, None)

                                                control.setPosition = mock.MagicMock()
                                                control.setWidth = mock.MagicMock()
                                                control.setHeight = mock.MagicMock()

                                                group.placeControl(control, row, column, pad_x=pad_x, pad_y=pad_y)

                                                with self.subTest("Control added to window"):
                                                    self._window.addControl.assert_called_with(control)

                                                with self.subTest("Test coordinates"):
                                                    expected_x = window_x + pad_x + (
                                                            (group_width // columns) * (column + column_span - 1))
                                                    expected_y = window_y + pad_y + (
                                                            (group_height // rows) * (row + row_span - 1))
                                                    control.setPosition.assert_called_with(expected_x, expected_y)

                                                with self.subTest("Test width"):
                                                    expected_width = ((group_width // columns) * column_span) - (
                                                                2 * pad_x)
                                                    control.setWidth.assert_called_with(expected_width)

                                                with self.subTest("Test height"):
                                                    expected_height = ((group_height // rows) * row_span) - (2 * pad_y)
                                                    control.setHeight.assert_called_with(expected_height)


if __name__ == '__main__':
    unittest2.main()
