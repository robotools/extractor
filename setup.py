#!/usr/bin/env python

import sys
from setuptools import setup, find_packages


needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_wheel = {'bdist_wheel'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name="ufo_extractor",
    version="0.2.0",
    description="Tools for extracting data from font binaries into UFO objects.",
    long_description=long_description,
    author="Tal Leming",
    author_email="tal@typesupply.com",
    url="https://github.com/typesupply/extractor",
    license="MIT",
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    setup_requires=pytest_runner + wheel,
    tests_require=[
        'pytest>=2.8',
    ],
    install_requires=[
        "fonttools>=3.3.1",
        "ufoLib>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Fonts",
    ],
)
