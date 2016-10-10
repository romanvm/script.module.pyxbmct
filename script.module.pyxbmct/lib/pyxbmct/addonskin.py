# coding: utf-8
# Module: skin
# Created on: 04.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>

import os
import xbmc
from xbmcaddon import Addon


class Skin(object):
    """
    Skin class

    Defines parameters that control
    the appearance of PyXBMCt windows and controls.
    """
    def __init__(self):
        kodi_version = xbmc.getInfoLabel('System.BuildVersion')[:2]
        # Kodistubs return an empty string
        if kodi_version and int(kodi_version) >= 17:
            self._estuary = True
        else:
            self._estuary = False
        self._texture_dir = os.path.join(Addon('script.module.pyxbmct').getAddonInfo('path'),
                                         'lib', 'pyxbmct', 'textures')

    @property
    def estuary(self):
        """
        Get or set a boolean property that defines the look of PyXBMCt elements:

        - ``True`` -- use Estuary skin appearance
        - ``False`` -- use Confluence skin appearance.

        :rtype: bool
        """
        return self._estuary

    @estuary.setter
    def estuary(self, value):
        if not isinstance(value, bool):
            raise TypeError('estuary property value must be bool!')
        self._estuary = value

    @property
    def images(self):
        """Get the base directory for image files"""
        if self.estuary:
            return os.path.join(self._texture_dir, 'estuary')
        else:
            return os.path.join(self._texture_dir, 'confluence')

    @property
    def x_margin(self):
        """
        Get horisontal adjustment for the header background
        if the main background has transparent edges.
        """
        if self.estuary:
            return 0
        else:
            return 5

    @property
    def y_margin(self):
        """
        Get vertical adjustment for the header background
        if the main background has transparent edges.
        """
        if self.estuary:
            return 0
        else:
            return 5

    @property
    def title_bar_x_shift(self):
        """Get horisontal adjustment for title bar texture"""
        if self.estuary:
            return 20
        else:
            return 0

    @property
    def title_bar_y_shift(self):
        """Get vertical adjustment for title bar texture"""
        if self.estuary:
            return 8
        else:
            return 4

    @property
    def title_back_y_shift(self):
        """
        Get header position adjustment
        if the main backround has visible borders.
        """
        if self.estuary:
            return 0
        else:
            return 4

    @property
    def header_height(self):
        """
        Get the height of a window header
        (for the title background and the title label).
        """
        if self.estuary:
            return 45
        else:
            return 35

    @property
    def close_btn_width(self):
        """Get the width of the top-right close button"""
        if self.estuary:
            return 35
        else:
            return 60

    @property
    def close_btn_height(self):
        """Get the height of the top-right close button"""
        if self.estuary:
            return 30
        else:
            return 30

    @property
    def close_btn_x_offset(self):
        """Get close button horisontal adjustment"""
        if self.estuary:
            return 50
        else:
            return 70

    @property
    def close_btn_y_offset(self):
        """Get close button vertical adjustment"""
        if self.estuary:
            return 7
        else:
            return 4

    @property
    def header_align(self):
        """
        Get a numeric value for header text alignment

        For example:

        - ``0``: left
        - ``6``: center
        """
        if self.estuary:
            return 0
        else:
            return 6

    @property
    def header_text_color(self):
        """Get the color of the header text"""
        if self.estuary:
            return ''
        else:
            return '0xFFFFA500'

    @property
    def background_img(self):
        """Get dialog background texture"""
        return os.path.join(self.images, 'AddonWindow', 'ContentPanel.png')

    @property
    def title_background_img(self):
        """Get title bar background texture"""
        return os.path.join(self.images, 'AddonWindow', 'dialogheader.png')

    @property
    def close_button_focus(self):
        """Get close button focused texture"""
        return os.path.join(self.images, 'AddonWindow', 'DialogCloseButton-focus.png')

    @property
    def close_button_no_focus(self):
        """Get close button unfocused texture"""
        return os.path.join(self.images, 'AddonWindow', 'DialogCloseButton.png')

    @property
    def main_bg_img(self):
        """
        Get fullscreen background for
        :class:`AddonFullWindow<pyxbmct.addonwindow.AddonFullWindow>` class
        """
        return os.path.join(self.images, 'AddonWindow', 'SKINDEFAULT.jpg')
