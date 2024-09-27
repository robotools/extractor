from extractor.exceptions import ExtractorError
from extractor.formats.opentype import isOpenType, extractFontFromOpenType
from extractor.formats.woff import isWOFF, extractFontFromWOFF
from extractor.formats.type1 import isType1, extractFontFromType1
from extractor.formats.ttx import isTTX, extractFontFromTTX
from extractor.formats.vfb import isVFB, extractFontFromVFB, haveVfb2ufo

try:
    from ._version import __version__
except ImportError:
    try:
        from setuptools_scm import get_version
        __version__ = get_version()
    except ImportError:
        __version__ = 'unknown'

_extractFunctions = dict(
    OTF=extractFontFromOpenType,
    Type1=extractFontFromType1,
    WOFF=extractFontFromWOFF,
    ttx=extractFontFromTTX,
    vfb=extractFontFromVFB,
)


def extractFormat(pathOrFile):
    if isType1(pathOrFile):
        return "Type1"
    elif isWOFF(pathOrFile):
        return "WOFF"
    elif isOpenType(pathOrFile):
        return "OTF"
    elif isTTX(pathOrFile):
        return "ttx"
    elif haveVfb2ufo() and isVFB(pathOrFile):
        return "vfb"
    return None


def extractUFO(
    pathOrFile,
    destination,
    doGlyphs=True,
    doInfo=True,
    doKerning=True,
    doFeatures=True,
    format=None,
    customFunctions={},
):
    if format is None:
        format = extractFormat(pathOrFile)
    if format not in _extractFunctions:
        raise ExtractorError("Unknown file format.")
    func = _extractFunctions[format]
    # wrap the extraction in a try: except: so that
    # callers don't need to worry about lower level
    # (fontTools, etc.) errors. if an error
    # occurs, print the traceback for debugging and
    # raise an ExtractorError.
    try:
        func(
            pathOrFile,
            destination,
            doGlyphs=doGlyphs,
            doInfo=doInfo,
            doKerning=doKerning,
            doFeatures=doFeatures,
            customFunctions=customFunctions.get(format, []),
        )
    except:
        import sys
        import traceback

        traceback.print_exc(file=sys.stdout)
        raise ExtractorError(
            "There was an error reading the %s file." % format
        )


def cmdline():
    """
    Extract one ore more fonts to UFO. Installed as command line script
    `extractufo`.

    Usage: extractufo font [font ...]
    """
    import os
    from sys import exit
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Extract data from font binaries and build UFO objects from them.",
        epilog="Each resulting UFO will be saved as FONT_FILE.ufo(z) in the same directory as the original FONT_FILE. "
               "If destination file or directory already exists, conversion for that source file will be skipped and the application exit code will indicate an error.",
    )
    parser.add_argument('FONT_FILE', help='Input font path', nargs="+")
    parser.add_argument('-m', '--ufo-module', choices=['ufoLib2', 'defcon'],
                        help='Select the default library for writing UFOs (default: autodetect, prefer ufoLib2)')
    parser.add_argument('-z', '--zip', action="store_true", help="Output UFO ZIP")

    args = parser.parse_args()
    if args.ufo_module is None:
        try:
            from ufoLib2 import Font
            print("Will use ufoLib2 for UFO output.")
        except ImportError:
            try:
                from defcon import Font
                print("Will use defcon for UFO output.")
            except ImportError:
                print("Either ufoLib2 or, alternatively, defcon library is required to run this command.\nPlease install one of them.")
                exit(1)
    elif args.ufo_module == 'ufoLib2':
        try:
            from ufoLib2 import Font
        except ImportError:
            print("Can't find ufoLib2 installed. Please install it or specify a different UFO library.")
            exit(1)
    else:
        try:
            from defcon import Font
        except ImportError:
            print("Can't find defcon installed. Please install it or specify a different UFO library.")
            exit(1)

    structure = "zip" if args.zip else "package"
    had_write_errors = False
    for font_path in args.FONT_FILE:
        ufo_path = f"{font_path}.ufo" if not args.zip else f"{font_path}.ufoz"
        print(f"Extracting {ufo_path}... ", end="")
        if os.path.exists(ufo_path):
            print("path already exists, skipping.")
            had_write_errors = True
            continue
        ufo = Font()
        extractUFO(font_path, ufo)
        ufo.save(ufo_path, structure=structure)
        print("done.")

    exit(had_write_errors)
