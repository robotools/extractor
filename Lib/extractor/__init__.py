from exceptions import ExtractorError
from formats.opentype import isOpenType, extractFontFromOpenType
from formats.woff import isWOFF, extractFontFromWOFF

def extractUFO(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True, customFunctions={}):
    if isOpenType(pathOrFile):
        func = extractFontFromOpenType
        format = "OTF"
    elif isWOFF(pathOrFile):
        func = extractFontFromWOFF
        format = "WOFF"
    else:
        raise ExtractorError("Unknown file format.")
    func(pathOrFile, destination, doGlyphs=doGlyphs, doInfo=doInfo, doKerning=doKerning, customFunctions=customFunctions.get(format, []))
