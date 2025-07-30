#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'chibi>=0.16.0', 'chibi_requests>=1.3.1', 'selenium>=4.29.0' ]

setup(
    author="dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="libreria para hacer scrappers de sitios web",
    install_requires=requirements,
    license="WTFPL",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chibi_site',
    name='chibi_site',
    packages=find_packages(include=['chibi_site', 'chibi_site.*']),
    url='https://github.com/dem4ply/chibi_site',
    version='0.1.0',
    zip_safe=False,
)
