"""
This is a dirty hack that I needed to use because script.module.pyxbmct is an invalid package name.
This is not good practice but I have yet to find a solution that doesn't involve putting the tests in
script.module.pyxbmct which I want to avoid as they are not a part of the Kodi addon.
"""
import os, sys
old_path = sys.path
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(parent_directory, "script.module.pyxbmct", "lib"))
import pyxbmct
sys.path = old_path