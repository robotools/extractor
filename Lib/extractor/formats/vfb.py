import os
import shutil
import tempfile
import subprocess

from fontTools.ufoLib import UFOReader

_ufo2vfbLocation = "/usr/local/bin/vfb2ufo"

def haveVfb2ufo():
    return os.path.exists(_ufo2vfbLocation)

# ----------------
# Public Functions
# ----------------

def isVFB(pathOrFile):
    if not isinstance(pathOrFile, str):
        return False
    if os.path.splitext(pathOrFile)[-1].lower() != ".vfb":
        return False
    return True

def extractFontFromVFB(pathOrFile, destination, doGlyphs=True, doInfo=True, doKerning=True, doGroups=True, doFeatures=True, doLib=True, customFunctions=[]):
    ufoPath = tempfile.mkdtemp(suffix=".ufo")
    cmds = [_ufo2vfbLocation, "-64", pathOrFile, ufoPath]
    cmds = subprocess.list2cmdline(cmds)
    popen = subprocess.Popen(cmds, shell=True)
    popen.wait()
    try:
        # vfb2ufo writes ufo2, and has no update since 2015...so dont get to crazy here...
        source = UFOReader(ufoPath)
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
    finally:
        shutil.rmtree(ufoPath)
