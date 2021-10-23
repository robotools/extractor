import os
import pytest
import unittest

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.ttProgram import Program

from extractor.stream import InstructionStream


sample = """PUSHB[ ]	/* 4 values pushed */
1 2 3 4
PUSHW[ ]	/* 2 values pushed */
1 -1
PUSHW[ ]	/* 2 values pushed */
5 512
SPVTCA[0]	/* SetPVectorToAxis */
SPVTCA[1]	/* SetPVectorToAxis */
SFVTL[0]	/* SetFVectorToLine */
SFVTL[1]	/* SetFVectorToLine */
MDAP[0]	/* MoveDirectAbsPt */
MDAP[1]	/* MoveDirectAbsPt */
IF[ ]	/* If */
  SHP[0]	/* ShiftPointByLastPoint */
  SHC[1]	/* ShiftContourByLastPt */
EIF[ ]	/* EndIf */
MSIRP[1]	/* MoveStackIndirRelPt */
MD[0]	/* MeasureDistance */
GC[1]	/* GetCoordOnPVector */
ROUND[01]	/* Round */
MDRP[00110]	/* MoveDirectRelPt */"""

expected_vtt = """#PUSHOFF
#PUSH, 1, 2, 3, 4
#PUSH, 1, -1
#PUSH, 5, 512
SPVTCA[Y]	/* SetPVectorToAxis */
SPVTCA[X]	/* SetPVectorToAxis */
SFVTL[r]	/* SetFVectorToLine */
SFVTL[R]	/* SetFVectorToLine */
MDAP[r]	/* MoveDirectAbsPt */
MDAP[R]	/* MoveDirectAbsPt */
IF[]	/* If */
  SHP[2]	/* ShiftPointByLastPoint */
  SHC[1]	/* ShiftContourByLastPt */
EIF[]	/* EndIf */
MSIRP[M]	/* MoveStackIndirRelPt */
MD[N]	/* MeasureDistance */
GC[O]	/* GetCoordOnPVector */
ROUND[Bl]	/* Round */
MDRP[m<RWh]	/* MoveDirectRelPt */
#PUSHON"""

sample_keyerror = "MDRP[00111]	/* MoveDirectRelPt */"


def data_path(file_name):
    return os.path.join(
        os.path.dirname(__file__),
        "data",
        "ibm_plex",
        file_name,
    )


class InstructionStreamTests(unittest.TestCase):
    def _compile(self, ttassembly: str) -> bytes:
        pgm = Program()
        pgm.fromAssembly(ttassembly)
        return pgm.getBytecode()

    def test_extract_ttx(self):
        font = TTFont(data_path("IBM Plex Serif-Text-FL.ttf"))
        with open(data_path("IBM Plex Serif-Text-FL.fpgm.ttxasm")) as f:
            expected_fpgm = f.read()
        fpgm = font["fpgm"]
        stream = InstructionStream(program_bytes=fpgm.program.getBytecode())
        print(stream)
        expected_lines = expected_fpgm.splitlines()
        for i, line in enumerate(str(stream).splitlines()):
            assert line == expected_lines[i]

    def test_extract_vtt(self):
        font = TTFont(data_path("IBM Plex Serif-Text-FL.ttf"))
        with open(data_path("IBM Plex Serif-Text-FL.fpgm.vttasm")) as f:
            expected_fpgm = f.read()
        fpgm = font["fpgm"]
        stream = InstructionStream(program_bytes=fpgm.program.getBytecode())
        expected_lines = expected_fpgm.splitlines()
        for i, line in enumerate(stream.vtt_assembly.splitlines()):
            assert line == expected_lines[i]

    def test_complex_ttx(self):
        stream = InstructionStream(program_bytes=self._compile(sample))
        # Roundtripped sample should be identical
        expected_lines = sample.splitlines()
        for i, line in enumerate(str(stream).splitlines()):
            assert line == expected_lines[i]

    def test_complex_vtt(self):
        stream = InstructionStream(program_bytes=self._compile(sample))
        expected_lines = expected_vtt.splitlines()
        for i, line in enumerate(stream.vtt_assembly.splitlines()):
            assert line == expected_lines[i]

    def test_illegal_ttx(self):
        # Sample contains illegal flags, ttx does ignore this
        stream = InstructionStream(
            program_bytes=self._compile(sample_keyerror)
        )
        # Roundtripped sample should be identical
        assert str(stream) == sample_keyerror

    def test_illegal_vtt(self):
        # Sample contains illegal flags, vtt should raise an error
        stream = InstructionStream(
            program_bytes=self._compile(sample_keyerror)
        )
        with pytest.raises(KeyError):
            assert stream.vtt_assembly == sample
