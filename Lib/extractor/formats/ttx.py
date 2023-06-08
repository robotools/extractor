from extractor.formats.opentype import (
    extractOpenTypeInfo,
    extractOpenTypeGlyphs,
    extractOpenTypeKerning,
    extractOpenTypeFeatures,
)


def isTTX(pathOrFile):
    from fontTools.ttLib import TTFont

    try:
        font = TTFont()
        font.importXML(pathOrFile)
        del font
    except Exception:
        return False
    return True


def extractFontFromTTX(
    pathOrFile,
    destination,
    doGlyphs=True,
    doInfo=True,
    doKerning=True,
    doFeatures=True,
    customFunctions=[],
):
    from fontTools.ttLib import TTFont, TTLibError

    source = TTFont()
    source.importXML(pathOrFile)
    if doInfo:
        extractOpenTypeInfo(source, destination)
    if doGlyphs:
        extractOpenTypeGlyphs(source, destination)
    if doKerning:
        kerning, groups = extractOpenTypeKerning(source, destination)
        destination.groups.update(groups)
        destination.kerning.clear()
        destination.kerning.update(kerning)
    if doFeatures:
        features = extractOpenTypeFeatures(source)
        destination.features.text = features
    for function in customFunctions:
        function(source, destination)
    source.close()
