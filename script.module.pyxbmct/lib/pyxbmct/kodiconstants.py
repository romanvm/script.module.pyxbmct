# -*- coding: utf-8 -*-
# PyXBMCt framework module
#
# PyXBMCt is a mini-framework for creating Kodi (XBMC) Python addons
# with arbitrary UI made of Controls - decendants of xbmcgui.Control class.
# The framework uses image textures from Kodi Confluence skin.
#
# Licence: GPL v.3 <http://www.gnu.org/licenses/gpl.html>

# Text alignment constants. Mixed variants are obtained by bit OR (|)
ALIGN_LEFT = 0
"""Align left"""
ALIGN_RIGHT = 1
"""Align right"""
ALIGN_CENTER_X = 2
"""Align center horizontally"""
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