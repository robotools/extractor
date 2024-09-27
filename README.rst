|CI Build Status| |PyPI Version| |Python Versions|


UFO Extractor
=============

Tools for extracting data from font binaries into UFO objects.

Supported input formats
-----------------------

The following font formats are supported:

-  CFF or TrueType-flavored OpenType fonts (``*.otf``, ``*.ttf``)
-  `FontTools <https://github.com/fonttools/fonttools>`__ TTX files
   (``*.ttx``)
-  WOFF 1.0/2.0 (``*.woff``, ``*.woff2``)
-  PostScript Type1 fonts (``*.pfa``, ``*.pfb``, etc.)
-  FontLab files (``*.vfb``, when installed with optional dependency "vfb")

Note however, that what data will (or even could) be exported will depend on
input file format and the file itself.

Python module
-------------

The example below demonstrates how one can import data into
a `ufoLib2 <https://github.com/fonttools/ufoLib2/>`__
or `Defcon <https://github.com/typesupply/defcon>`__ ``Font`` instance:

.. code:: python

   >>> import extractor
   >>> from ufoLib2 import Font    # alternatively: from defcon import Font
   >>> ufo = Font()
   >>> extractor.extractUFO("/path/to/MyFont.ttf", ufo)
   >>> ufo.save("/path/to/MyFont.ufo")

Console script
--------------

A console script for one-off conversion is also provided
(note: see Installation below):

.. code::

   $ extractufo -h
   usage: extractufo [-h] [-m {ufoLib2,defcon}] [-z] FONT_FILE [FONT_FILE ...]

   Extract data from font binaries and build UFO objects from them.

   positional arguments:
     FONT_FILE             Input font path

   options:
     -h, --help            show this help message and exit
     -m {ufoLib2,defcon}, --ufo-module {ufoLib2,defcon}
                           Select the default library for writing UFOs (default: autodetect, prefer ufoLib2)
     -z, --zip             Output UFO ZIP

   Each resulting UFO will be saved as FONT_FILE.ufo(z) in the same directory as the original FONT_FILE.
   If destination file or directory already exists, conversion for that source file will be skipped and the application exit code will indicate an error.

Installation
------------

You can install ``extractor`` with ``pip``:

.. code::

   $ pip install ufo-extractor

To install with support for extracting from vfb files:

.. code::

   $ pip install ufo-extractor[vfb]

If you want to use the console script and have neither `ufoLib2` nor `defcon`
installed (or aren't sure), running the following will install `ufoLib2` as well
to ensure that the script works:

.. code::

   $ pip install ufo-extractor[script]

The options may also be combined:

.. code::

   $ pip install ufo-extractor[vfb][script]

Note that, for historical reasons, the package is listed on the
`Python Package Index <https://travis-ci.org/typesupply/extractor>`__ under the name
``ufo-extractor``, to disambiguate it from another package also called "extractor".
However, the import name for the package remains ``extractor``, without prefix.


.. |CI Build Status| image:: https://github.com/robotools/extractor/workflows/Tests/badge.svg
   :target: https://github.com/robotools/extractor/actions?query=workflow%3ATests
.. |PyPI Version| image:: https://img.shields.io/pypi/v/ufo-extractor.svg
   :target: https://pypi.org/project/ufo-extractor/
.. |Python Versions| image:: https://img.shields.io/badge/python-3.8%2C%203.9%2C%203.10%2C%203.11%2C%203.12-blue.svg
