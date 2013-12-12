import os
from robofab.ufoLib import UFOReader

# ----------------
# Public Functions
# ----------------

def isUFO(pathOrFile):
    if not isinstance(pathOrFile, basestring):
        return False
    if os.path.splitext(pathOrFile)[-1].lower() != ".ufo":
        return False
    if not os.path.isdir(pathOrFile):
        return False
    try:
        reader = UFOReader(pathOrFile)
    except:
        return False
    return True

def extractFontFromUFO(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True, doGroups=True, doFeatures=True, doLib=True, customFunctions=[]):
    source = UFOReader(pathOrFile)
    if doInfo:
        source.readInfo(destination.info)
    if doKerning:
        kerning = source.readKerning()
        destination.kerning.update(kerning)
    if doGroups:
        groups = source.readGroups()
        destination.groups.update(groups)
    if doFeatures:
        features = source.readFeatures()
        destination.features.text = features
    if doLib:
        lib = source.readLib()
        destination.lib.update(lib)
    if doGlyphs:
        glyphSet = source.getGlyphSet()
        for glyphName in glyphSet.keys():
            destination.newGlyph(glyphName)
            glyph = destination[glyphName]
            pointPen = glyph.getPointPen()
            glyphSet.readGlyph(glyphName=glyphName, glyphObject=glyph, pointPen=pointPen)
    for function in customFunctions:
        function(source, destination)
