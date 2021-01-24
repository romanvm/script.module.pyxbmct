# coding: utf-8
# (c) 2020, Roman Miroshnychenko <roman1972@gmail.com>
# License: GPL v.3

import os
from xml.dom.minidom import parse
from setuptools import setup, find_packages

this_dir = os.path.dirname(os.path.abspath(__file__))


def get_version():
    doc = parse(os.path.join(this_dir, 'script.module.pyxbmct', 'addon.xml'))
    return doc.firstChild.getAttribute('version')


setup(
    name='PyXBMCt',
    author='Roman Miroshnychenko',
    version=get_version(),
    package_dir={'': 'script.module.pyxbmct/lib'},
    packages=find_packages('./script.module.pyxbmct/lib'),
    install_requires=[
        'Kodistubs',
        'six',
        'kodi_six @ git+https://github.com/romanvm/kodi.six'
    ],
    extras_require={
        'dev': [
            'unittest2',
            'mock',
            'pytype',
            'Sphinx'
        ]
    },
    zip_safe=False
)
