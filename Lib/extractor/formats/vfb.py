import os
import shutil
import tempfile
import subprocess
from ufo import extractFontFromUFO

_ufo2vfbLocation = "/usr/local/bin/vfb2ufo"

def _setVfb2ufoLocation(location):
    global _ufo2vfbLocation
    _ufo2vfbLocation = location

def haveVfb2ufo():
    return os.path.exists(_ufo2vfbLocation)

# ----------------
# Public Functions
# ----------------

def isVFB(pathOrFile):
    if not isinstance(pathOrFile, basestring):
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
        extractFontFromUFO(ufoPath, destination,
            doGlyphs=doGlyphs, doInfo=doInfo,
            doKerning=doKerning, doGroups=doGroups,
            doFeatures=doFeatures, doLib=doLib,
            customFunctions=customFunctions
        )
    finally:
        shutil.rmtree(ufoPath)