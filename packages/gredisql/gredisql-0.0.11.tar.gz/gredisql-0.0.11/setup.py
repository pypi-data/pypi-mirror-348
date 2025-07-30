# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 02 Sep 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import setuptools
from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='gredisql',
    version='0.0.11',
    author='Sabbir Amin',
    author_email='sabbiramin.cse11ruet@gmail.com',
    description='A GraphQL interface for Redis Database. ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sabbiramin113008/gredisql',
    packages=setuptools.find_packages(),
    install_requires=['redis==5.0.0',
                      'Flask==2.3.3',
                      'strawberry-graphql==0.205.0'],
    license='MIT',
    keywords=['python', 'Database', 'Redis', 'GraphQL'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    zip_safe=False
)
