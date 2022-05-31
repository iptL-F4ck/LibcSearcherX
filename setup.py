#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='LibcSearcherX',
    version='0.0.2',
    author='iptL',
    author_email='iptL_htb@163.com',
    url='',
    description='Online Libc Searcher',
    packages=['LibcSearcherX'],
    include_package_data=True,
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
        ]
    }
)
