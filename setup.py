#!/usr/bin/env python

import sys
from setuptools import setup, find_packages


needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_wheel = {'bdist_wheel'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

with open('README.rst', 'r') as f:
    long_description = f.read()

setup_params = dict(
    name="ufo_extractor",
    description="Tools for extracting data from font binaries into UFO objects.",
    long_description=long_description,
    author="Tal Leming",
    author_email="tal@typesupply.com",
    maintainer="Just van Rossum, Frederik Berlaen, Ben Kiel",
    maintainer_email="justvanrossum@gmail.com",
    url="https://github.com/robotools/extractor",
    license="MIT",
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    include_package_data=True,
    use_scm_version={
          "write_to": 'Lib/extractor/_version.py',
          "write_to_template": '__version__ = "{version}"',
     },
    setup_requires=pytest_runner + wheel + ['setuptools_scm'],
    tests_require=[
        'pytest>=3.0.3',
    ],
    install_requires=[
        "fonttools[ufo,lxml,woff,unicode,type1]>=4.17.0",
        "fontFeatures",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Fonts",
    ],
    python_requires='>=3.7',
    zip_safe=True,
)

if __name__ == "__main__":
    setup(**setup_params)
