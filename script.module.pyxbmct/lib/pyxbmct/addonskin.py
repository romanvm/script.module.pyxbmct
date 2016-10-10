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

    ``estuary`` bool property defines the look of PyXBMCt elements:
    ``True`` -- use Estuary skin appearance, ``False`` -- use Confluence skin appearance.
    """
    def __init__(self):
        kodi_version = xbmc.getInfoLabel('System.BuildVersion')[:2]
        # Kodistubs return an empty string
        if kodi_version and int(kodi_version) >= 17:
            self.estuary = True
        else:
            self.estuary = False
        self._texture_dir = os.path.join(Addon('script.module.pyxbmct').getAddonInfo('path'),
                                         'lib', 'pyxbmct', 'textures')

    @property
    def images(self):
        """Base directory for image files"""
        if self.estuary:
            return os.path.join(self._texture_dir, 'estuary')
        else:
            return os.path.join(self._texture_dir, 'confluence')

    @property
    def x_margin(self):
        """
        Horisontal adjustment for the header background if the main background has transparent edges.
        """
        if self.estuary:
            return 0
        else:
            return 5

    @property
    def y_margin(self):
        """
        Vertical adjustment for the header background if the main background has transparent edges.
        """
        if self.estuary:
            return 0
        else:
            return 5

    @property
    def title_bar_x_shift(self):
        """Horisontal adjustment for title bar texture"""
        if self.estuary:
            return 20
        else:
            return 0

    @property
    def title_bar_y_shift(self):
        """Vertical adjustment for title bar texture"""
        if self.estuary:
            return 8
        else:
            return 4

    @property
    def title_back_y_shift(self):
        """
        Header position adjustment if the main backround has visible borders.
        """
        if self.estuary:
            return 0
        else:
            return 4

    @property
    def header_height(self):
        """
        The height of a window header (for the title background and the title label).
        """
        if self.estuary:
            return 45
        else:
            return 35

    @property
    def close_btn_width(self):
        if self.estuary:
            return 35
        else:
            return 60

    @property
    def close_btn_height(self):
        """The height of the top-right close button"""
        if self.estuary:
            return 30
        else:
            return 30

    @property
    def close_btn_x_offset(self):
        """Close button horisontal adjustment"""
        if self.estuary:
            return 50
        else:
            return 70

    @property
    def close_btn_y_offset(self):
        """Close button vertical adjustment"""
        if self.estuary:
            return 7
        else:
            return 4

    @property
    def header_align(self):
        """
        Header text alignment

        0 -- left
        6 -- center
        """
        if self.estuary:
            return 0
        else:
            return 6

    @property
    def header_text_color(self):
        """The color of the header text"""
        if self.estuary:
            return ''
        else:
            return '0xFFFFA500'

    @property
    def background_img(self):
        """Dialog background texture"""
        return os.path.join(self.images, 'AddonWindow', 'ContentPanel.png')

    @property
    def title_background_img(self):
        """Title bar background texture"""
        return os.path.join(self.images, 'AddonWindow', 'dialogheader.png')

    @property
    def close_button_focus(self):
        """Close button focused texture"""
        return os.path.join(self.images, 'AddonWindow', 'DialogCloseButton-focus.png')

    @property
    def close_button_no_focus(self):
        """Close button unfocused texture"""
        return os.path.join(self.images, 'AddonWindow', 'DialogCloseButton.png')

    @property
    def main_bg_img(self):
        """Fullscreen background for AddonFullWindow class"""
        return os.path.join(self.images, 'AddonWindow', 'SKINDEFAULT.jpg')
