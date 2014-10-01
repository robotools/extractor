from exceptions import ExtractorError
from formats.opentype import isOpenType, extractFontFromOpenType
from formats.woff import isWOFF, extractFontFromWOFF
from formats.type1 import isType1, extractFontFromType1
from formats.ttx import isTTX, extractFontFromTTX
from formats.ufo import isUFO, extractFontFromUFO
from formats.vfb import isVFB, extractFontFromVFB, haveVfb2ufo, _setVfb2ufoLocation

supportedFormats = [".otf", ".ttf", ".pfa", ".pfb", ".ttx", ".ufo"]

def extractUFO(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True, doGroups=True, doFeatures=True, doLib=True, customFunctions={}):
    if isUFO(pathOrFile):
        func = extractFontFromUFO
        format = "UFO"
    elif isOpenType(pathOrFile):
        func = extractFontFromOpenType
        format = "OTF"
    elif isType1(pathOrFile):
        func = extractFontFromType1
        format = "Type1"
    elif isWOFF(pathOrFile):
        func = extractFontFromWOFF
        format = "WOFF"
    elif isTTX(pathOrFile):
        func = extractFontFromTTX
        format = "ttx"
    elif isVFB(pathOrFile) and ".vfb" in supportedFormats:
        func = extractFontFromVFB
        format = "VFB"
    else:
        raise ExtractorError("Unknown file format.")
    # wrap the extraction in a try: except: so that
    # callers don't need to worry about lower level
    # (fontTools, woffTools, etc.) errors. if an error
    # occurs, print the traceback for debugging and
    # raise an ExtractorError.
    try:
        func(pathOrFile, destination,
            doGlyphs=doGlyphs, doInfo=doInfo,
            doKerning=doKerning, doGroups=doGroups,
            doFeatures=doFeatures, doLib=doLib,
            customFunctions=customFunctions.get(format, [])
        )
    except:
        import sys
        import traceback
        traceback.print_exc(file=sys.stdout)
        raise ExtractorError("There was an error reading the %s file." % format)

# ---------------------
# Specific Format Tools
# ---------------------

if haveVfb2ufo():
    supportedFormats.append(".vfb")

def registerVfb2ufo(location):
    if ".vfb" in supportedFormats:
        supportedFormats.remove(".vfb")
    _setVfb2ufoLocation(location)
    if haveVfb2ufo():
        supportedFormats.append(".vfb")
