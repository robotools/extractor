from extractor.exceptions import ExtractorError
from extractor.formats.opentype import isOpenType, extractFontFromOpenType
from extractor.formats.woff import isWOFF, extractFontFromWOFF
from extractor.formats.type1 import isType1, extractFontFromType1
from extractor.formats.ttx import isTTX, extractFontFromTTX

def extractUFO(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True, customFunctions={}):
    if isOpenType(pathOrFile):
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
    else:
        raise ExtractorError("Unknown file format.")
    # wrap the extraction in a try: except: so that
    # callers don't need to worry about lower level
    # (fontTools, woffTools, etc.) errors. if an error
    # occurs, print the traceback for debugging and
    # raise an ExtractorError.
    try:
        func(pathOrFile, destination, doGlyphs=doGlyphs, doInfo=doInfo, doKerning=doKerning, customFunctions=customFunctions.get(format, []))
    except:
        import sys
        import traceback
        traceback.print_exc(file=sys.stdout)
        raise ExtractorError("There was an error reading the %s file." % format)
