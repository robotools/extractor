from opentype import extractOpenTypeInfo, extractOpenTypeGlyphs, extractOpenTypeKerning
from extractor.tools import defaultLeftKerningGroupPrefix, defaultRightKerningGroupPrefix

# ----------------
# Public Functions
# ----------------

def isWOFF(pathOrFile):
    from woffTools import WOFFFont, WOFFLibError
    try:
        font = WOFFFont(pathOrFile)
        del font
    except WOFFLibError:
        return False
    return True

def extractFontFromWOFF(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True, doGroups=True, doFeatures=True, doLib=True, customFunctions=[]):
    from woffTools import WOFFFont
    source = WOFFFont(pathOrFile)
    if doInfo:
        extractOpenTypeInfo(source, destination)
    if doGlyphs:
        extractOpenTypeGlyphs(source, destination)
    if doKerning:
        kerning, groups = extractOpenTypeKerning(source, destination)
        destination.groups.update(groups)
        destination.kerning.clear()
        destination.kerning.update(kerning)
    for function in customFunctions:
        function(source, destination)
    source.close()

# ----------------
# Specific Imports
# ----------------

def extractWOFFInfo(source, destination):
    return extractOpenTypeInfo(source, destination)

def extractWOFFGlyphs(source, destination):
    return extractOpenTypeGlyphs(source, destination)

def extractWOFFKerning(source, destination, leftGroupPrefix=defaultLeftKerningGroupPrefix, rightGroupPrefix=defaultRightKerningGroupPrefix):
    return extractOpenTypeKerning(source, destination, leftGroupPrefix=leftGroupPrefix, rightGroupPrefix=rightGroupPrefix)
