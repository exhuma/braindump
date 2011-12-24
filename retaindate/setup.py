#!/usr/bin/env python

from distutils.core import setup

setup(name='retaindate',
        version='1.0',
        description='Awfully simple module to check a date for obsoletion',
        author='Michel Albert',
        url='https://github.com/exhuma/braindump',
        author_email='michel@albert.lu',
        packages=['retaindate'],
        license="BSD",
        long_description=open('README.rst').read(),
        )
