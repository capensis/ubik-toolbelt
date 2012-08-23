#!/usr/bin/env python
# coding: utf-8

import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

setup(
	name='ubik-toolbelt',
	version='0.1',
	description='Ubik toolbelt for management',
	long_description=open('README.md').read(), 
	license=open("LICENSE").read(),
	author="Geoffrey Lehée",
	author_email="geoffrey@lehee.name",
	url='https://github.com/socketubs/Ubik-toolbelt/',
	keywords="ubik package toolbelt linux",
	packages = ['ubik_toolbelt'],
	scripts=['bin/ubik-package'],
	install_requires=['docopt==0.5.0'],
	classifiers=(
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7')
)
