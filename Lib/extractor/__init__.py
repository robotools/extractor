from exceptions import ExtractorError
from formats.opentype import isOpenType, extractFontFromOpenType

def extractUFO(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True):
    if isOpenType(pathOrFile):
        extractFontFromOpenType(pathOrFile, destination, doGlyphs=doGlyphs, doInfo=doInfo, doKerning=doKerning)
    else:
        raise ExtractorError("Unknown file format.")
