#!/usr/bin/env python

import sys
from setuptools import setup

try:
    import fontTools
except:
    print "*** Warning: extractor requires FontTools, see:"
    print "    https://github.com/behdad/fonttools"

try:
    import robofab
except:
    print "*** Warning: extractor requires RoboFab, see:"
    print "    https://github.com/robofab-developers/robofab.git"


setup(name="extractor",
    version="0.1",
    description="A package that extracts data from font binaries into an object with the same basic API as defcon.",
    author="Tal Leming",
    author_email="tal@typesupply.com",
    url="https://github.com/typesupply/extractor",
    license="MIT",
    packages=[
        "extractor",
        "extractor.formats"
    ],
    package_dir={"":"Lib"}
)
