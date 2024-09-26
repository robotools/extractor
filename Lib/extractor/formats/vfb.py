import os
import shutil
import tempfile

from fontTools.ufoLib import UFOReader

try:
    from vfbLib.vfb.vfb import Vfb
    from vfbLib.ufo.builder import VfbToUfoBuilder

    haveVfbLib = True
except ImportError:
    haveVfbLib = False


def haveVfb2ufo():
    return haveVfbLib


# ----------------
# Public Functions
# ----------------


def isVFB(pathOrFile):
    if not isinstance(pathOrFile, str):
        return False
    if os.path.splitext(pathOrFile)[-1].lower() != ".vfb":
        return False
    return True


def extractFontFromVFB(
    pathOrFile,
    destination,
    doGlyphs=True,
    doInfo=True,
    doKerning=True,
    doGroups=True,
    doFeatures=True,
    doLib=True,
    customFunctions=[],
):
    extract_minimal = True
    vfb = Vfb(
        pathOrFile,
        minimal=extract_minimal,
        drop_keys=("Encoding", "Encoding Mac"),
        unicode_strings=True,
    )
    vfb.decompile()
    builder = VfbToUfoBuilder(
        vfb,
        minimal=extract_minimal,
        base64=True,
        pshints=False,
        add_kerning_groups=False,
    )
    masters = builder.get_ufo_masters(silent=True)
    ufoLib_source = masters[0]
    ufoPath = tempfile.mkdtemp(suffix=".ufo")
    ufoLib_source.save(ufoPath, overwrite=True)
    try:
        # We now use vfbLib instead of vfb2ufo, which wrote ufo2, and had no update
        # since 2015, so the extracted UFOs were pretty basic.
        # More data could be extracted now with vfbLib if needed.
        source = UFOReader(ufoPath, validate=True)
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
                glyphSet.readGlyph(
                    glyphName=glyphName, glyphObject=glyph, pointPen=pointPen
                )
        for function in customFunctions:
            function(source, destination)
    finally:
        shutil.rmtree(ufoPath)
