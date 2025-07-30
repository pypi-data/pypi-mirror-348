#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pyinstxtractorCN',
    version='1.0.0',
    description='Decompile the .exe program packaged by pyinstaller, Chinese version',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='JZM',
    author_email='pyinstxtractorcn@outlook.com',
    url='https://github.com/jzm3/pyinstxtractorCN',
    install_requires=[],
    license='Apache License 2.0',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries'
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/jzm3/pyinstxtractorCN',
        'Source': 'https://github.com/jzm3/pyinstxtractorCN',
    },
)