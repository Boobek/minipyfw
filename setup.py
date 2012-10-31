#!/usr/bin/env python
'''
Usage:    python -OO setup.py install
'''
from distutils.core import setup

version = "1.0"
name = "PyQutie framework"
description = "Language teacher application"
author = 'Balazs KANYO'
author_email = 'bkanyo@gmail.com'
url = 'http://boobekdev.fw.hu/'

setup(
	version=version,
	description=description,
	author=author,
	author_email=author_email,
	url=url,
	name=name,
	packages = ['minipyfw'],
	package_dir={"minipyfw": "minipyfw"},
)
