import os
import pytest
import unittest

from fontTools.ttLib import TTFont
from extractor.stream import InstructionStream


def data_path(file_name):
    return os.path.join(
        os.path.dirname(__file__),
        "data",
        "ibm_plex",
        file_name,
    )


class InstructionStreamTests(unittest.TestCase):
    def test_extract_ttx(self):
        font = TTFont(data_path("IBM Plex Serif-Text-FL.ttf"))
        with open(data_path("IBM Plex Serif-Text-FL.fpgm.ttxasm")) as f:
            expected_fpgm = f.read()
        fpgm = font["fpgm"]
        stream = InstructionStream(program_bytes=fpgm.program.getBytecode())
        assert str(stream) == expected_fpgm

    def test_extract_vtt(self):
        font = TTFont(data_path("IBM Plex Serif-Text-FL.ttf"))
        with open(data_path("IBM Plex Serif-Text-FL.fpgm.vttasm")) as f:
            expected_fpgm = f.read()
        fpgm = font["fpgm"]
        stream = InstructionStream(program_bytes=fpgm.program.getBytecode())
        assert stream.vtt_assembly == expected_fpgm
