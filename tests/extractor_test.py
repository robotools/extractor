import extractor
import os
import pytest


def getpath(filename):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, "data", filename)


class ExtractUfoTest:

    def test_extract_cmap_with_UVS(self, FontClass):
        ufo = FontClass()
        extractor.extractUFO(getpath("UVSTest.ttf"), ufo)

        assert {glyph.name: set(glyph.unicodes) for glyph in ufo if glyph.unicodes} == {
            "zero": {0x030},
            "Anegativesquared": {0x1F170},
        }

        assert ufo.lib.get("public.unicodeVariationSequences") == {
            "FE00": {"0030": "zero.slash"},
            "FE0E": {"1F170": "Anegativesquared.text"},
            "FE0F": {"1F170": "Anegativesquared"},
        }


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(sys.argv))
