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
    ``True``: use Estuary skin design, ``False``: use Confluence skin design.
    """
    def __init__(self):
        if int(xbmc.getInfoLabel('System.BuildVersion')[:2]) >= 17:
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
        if self.estuary:
            return 20
        else:
            return 0

    @property
    def title_bar_y_shift(self):
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
        if self.estuary:
            return 30
        else:
            return 30

    @property
    def close_btn_x_offset(self):
        if self.estuary:
            return 50
        else:
            return 70

    @property
    def close_btn_y_offset(self):
        if self.estuary:
            return 7
        else:
            return 4

    @property
    def heder_align(self):
        if self.estuary:
            return 0
        else:
            return 6

    @property
    def header_text_color(self):
        if self.estuary:
            return ''
        else:
            return '0xFFFFA500'

    @property
    def background_img(self):
        return os.path.join(self.images, 'AddonWindow', 'ContentPanel.png')

    @property
    def title_background_img(self):
        return os.path.join(self.images, 'AddonWindow', 'dialogheader.png')

    @property
    def close_button_focus(self):
        return os.path.join(self.images, 'AddonWindow', 'DialogCloseButton-focus.png')

    @property
    def close_button_no_focus(self):
        return os.path.join(self.images, 'AddonWindow', 'DialogCloseButton.png')

    @property
    def main_bg_img(self):
        return os.path.join(self.images, 'AddonWindow', 'SKINDEFAULT.jpg')
