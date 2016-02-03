#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='kicadsearch',
      version='0.3.1',
      author='Arvid Juskaitis',
      author_email='arvydas.juskaitis@gmail.com',
      url='https://github.com/arvjus/kicad-search',
      packages=['kicadsearch', ],
      license='LICENSE.txt',
      description='Freetext searching in KiCad EDA component libraries',
      keywords=['kicad', 'search'],
      scripts=['bin/kicadsearch', 'bin/kicadsearch-index'],
      install_requires=[
          'Whoosh >=2.7.0'
      ], )
