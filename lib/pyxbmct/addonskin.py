# coding: utf-8
# Module: skin
# Created on: 04.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import os
from xbmcaddon import Addon

estuary = True
texture_dir = os.path.join(Addon('script.module.pyxbmct').getAddonInfo('path'), 'lib', 'pyxbmct', 'textures')


class Skin(object):
    """
    Defines the appearance of PyXBMCt windows and controls
    """
    @property
    def images(self):
        if estuary:
            return os.path.join(texture_dir, 'estuary')
        else:
            return os.path.join(texture_dir, 'default')

    @property
    def x_margin(self):
        if estuary:
            return 0
        else:
            return 5

    @property
    def y_margin(self):
        if estuary:
            return 0
        else:
            return 5

    @property
    def y_shift(self):
        if estuary:
            return 0
        else:
            return 4

    @property
    def header_height(self):
        if estuary:
            return 45
        else:
            return 35

    @property
    def close_btn_width(self):
        if estuary:
            return 30
        else:
            return 60

    @property
    def close_btn_height(self):
        if estuary:
            return 30
        else:
            return 30

    @property
    def close_btn_x_offset(self):
        if estuary:
            return 50
        else:
            return 70

    @property
    def close_btn_y_offset(self):
        if estuary:
            return 7
        else:
            return 4

    @property
    def heder_align(self):
        if estuary:
            return 0
        else:
            return 6

    @property
    def header_text_color(self):
        if estuary:
            return ''
        else:
            return '0xFFFFA500'
