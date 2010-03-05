from exceptions import ExtractorError
from formats.opentype import isOpenType, extractFontFromOpenType
from formats.woff import isWOFF, extractFontFromWOFF

def extractUFO(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True):
    if isOpenType(pathOrFile):
        func = extractFontFromOpenType
    elif isWOFF(pathOrFile):
        func = extractFontFromWOFF
    else:
        raise ExtractorError("Unknown file format.")
    func(pathOrFile, destination, doGlyphs=doGlyphs, doInfo=doInfo, doKerning=doKerning)