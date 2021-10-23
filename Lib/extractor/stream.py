# -*- coding: utf-8 -*-
from fontTools.misc.textTools import num2binary
from fontTools.ttLib.tables.ttProgram import streamOpcodeDict, opcodeDict
from io import BytesIO


class InstructionStream(object):
    """
    :param program_bytes: The program bytecode.
    :type program_bytes:  bytes

    The instruction stream.
    """

    def __init__(self, instruction_processor=None, program_bytes=b"") -> None:
        self.ip = instruction_processor
        self.io = BytesIO(program_bytes)
        self._num_bytes = len(program_bytes)

    def __len__(self):
        return self._num_bytes

    def __repr__(self) -> str:
        """
        Return the instructions from the bytecode in the current stream
        starting at the beginning.
        """
        return self.get_assembly()

    def __str__(self) -> str:
        """
        Return the instructions from the bytecode in the current stream
        starting at the beginning.
        """
        return self.get_assembly()

    def move_instruction_pointer(self, bytes_offset: int) -> None:
        """
        :param bytes_offset: The offset in bytes. May be positive or negative.
        :type bytes_offset:  int

        Move the instruction pointer inside the current stream, relative to the
        current pointer position.
        """
        self.io.seek(bytes_offset, 1)  # 1 = relative to current position

    def read_byte(self):
        """
        Read a byte from the instruction stream and advance the instruction
        pointer. Returns the value as a tuple of (byte, int).
        """
        b = self.io.read(1)
        if not b:
            return False
        return b, int.from_bytes(b, byteorder="big", signed=False)

    def read_word(self):
        """
        Read a word from the instruction stream and advance the instruction
        pointer. Returns the value as a tuple of (word, int).
        """
        w = self.io.read(2)
        if not w:
            return False
        return w, int.from_bytes(w, byteorder="big", signed=True)

    def rewind(self) -> None:
        """
        Rewind the instruction pointer to the beginning of the stream.
        """
        self.io.seek(0)

    # Getting the assembly code

    @property
    def vtt_assembly(self) -> str:
        """
        Return the instructions from the bytecode in the current stream as VTT
        assembly code.
        """
        return self.get_assembly(dialect="vtt", end="\n")

    def get_assembly(self, dialect="ttx", end="\n") -> str:
        """
        Return the instructions from the bytecode in the current stream as
        assembly code in the specified dialect, "ttx" or "vtt".
        """
        vtt = dialect == "vtt"
        ttx = dialect == "ttx"
        self.rewind()

        asm = ""
        indent = 0

        while True:
            opcode = self.io.read(1)
            if not opcode:
                asm = asm.strip()
                if ttx:
                    return asm
                elif vtt:
                    if asm:
                        return f"#PUSHOFF{end}" + asm.strip() + f"{end}#PUSHON"
                    return ""
                else:
                    # Unknown dialect
                    raise NotImplementedError

            opcode = int.from_bytes(opcode, byteorder="big", signed=False)
            cmd_info = streamOpcodeDict.get(opcode, None)
            if cmd_info is None:
                cmd_info = opcodeDict.get(opcode, None)
            if cmd_info is None:
                print(
                    asm + "\n"
                    "Illegal opcode 0x%02x at offset 0x%04x."
                    % (int(opcode), self.io.tell(),)
                )
                raise KeyError
            cmd_name, arg_bits, base_opcode, name = cmd_info

            args = []
            if cmd_name in ("EIF", "ELSE", "ENDF"):
                indent -= 1

            if cmd_name in ("NPUSHB", "NPUSHW", "PUSHB", "PUSHW"):
                # PUSH instructions read their arguments from the stream
                if cmd_name.startswith("PUSH"):
                    # Take number of arguments from the opcode
                    num_args = opcode - base_opcode + 1
                else:
                    # Take number of arguments from the stream
                    _, num_args = self.read_byte()
                if cmd_name.endswith("B"):
                    for n in range(num_args):
                        _, i = self.read_byte()
                        args.append(str(i))
                else:
                    for n in range(num_args):
                        _, i = self.read_word()
                        args.append(str(i))
                arg_bits = 0  # Don't output bits for push instructions

            if arg_bits == 0:
                if ttx:
                    arg_bitstring = " "
                else:
                    arg_bitstring = ""
            else:
                if ttx:
                    arg_bitstring = num2binary(opcode - base_opcode, arg_bits)
                elif vtt:
                    arg_bitstring = self.bitstring_to_mnemonic(
                        cmd_name, num2binary(opcode - base_opcode, arg_bits)
                    )
                else:
                    # Unknown dialect
                    raise NotImplementedError

            if ttx:
                if cmd_name in ("NPUSHB", "NPUSHW", "PUSHB", "PUSHW"):
                    num_args = len(args)
                    val = "value" if num_args == 1 else "values"
                    asm += (
                        f"\n{'  ' * indent}{cmd_name}[{arg_bitstring}]"
                        f"\t/* {num_args} {val} pushed */"
                    )
                else:
                    asm += (
                        f"\n{'  ' * indent}{cmd_name}[{arg_bitstring}]"
                        f"\t/* {name} */"
                    )

                if args:
                    asm += f"\n{'  ' * indent}{' '.join(args)}"

            elif vtt:
                if cmd_name in ("NPUSHB", "NPUSHW", "PUSHB", "PUSHW"):
                    # Format as generic #PUSH for VTT assembly output
                    cmd_name = "#PUSH"
                    asm += f"{end}{'  ' * indent}{cmd_name}, {', '.join(args)}"
                elif cmd_name in ("JMPR", "JROF"):
                    # Special formatting for jump instructions
                    if cmd_name == "JPMR":
                        args = ("*",)
                    elif cmd_name == "JROF":
                        args = ("*", "*")
                    asm += f"{end}#PUSHON"
                    asm += f"{end}{'  ' * indent}{cmd_name}, {', '.join(args)}"
                    asm += f"{end}#PUSHOFF"
                else:
                    asm += (
                        f"{end}{'  ' * indent}{cmd_name}[{arg_bitstring}]"
                        f"\t/* {name} */"
                    )

            else:
                # Unknown dialect
                raise NotImplementedError

            if cmd_name in ("ELSE", "FDEF", "IF"):
                indent += 1

    def bitstring_to_mnemonic(self, cmd_name: str, bitstring: str) -> str:
        """
        Return VTT mnemonics for a bit string
        """
        if cmd_name in ("SVTCA", "SPVTCA", "SFVTCA", "IUP"):
            # Direction
            if bitstring == "0":
                return "Y"  # Y axis
            return "X"  # X axis

        elif cmd_name in ("SPVTL", "SFVTL", "SDPVTL"):
            # Line relation
            if bitstring == "0":
                return "r"  # parallel to line
            return "R"  # perpendicular to line

        elif cmd_name in ("MDAP", "MIAP"):
            # Rounding
            if bitstring == "0":
                return "r"  # do not round distance
            return "R"  # round distance

        elif cmd_name in ("SHP", "SHC", "SHZ"):
            # Reference Point Usage
            if bitstring == "0":
                return "2"  # Use rp2
            return "1"  # Use rp1

        elif cmd_name in ("MSIRP",):
            # Reference Point Autoset
            if bitstring == "0":
                return "m"  # Do not set rp0
            return "M"  # Set rp0 to point number on the stack

        elif cmd_name in ("GC", "MD"):
            # Outline
            if bitstring == "0":
                return "N"  # Use gridfitted outline
            return "O"  # Use original outline

        elif cmd_name in ("ROUND", "NROUND"):
            # Color
            return self.bitstring_to_color_mnemonic(bitstring)

        elif cmd_name in ("MDRP", "MIRP"):
            flags = ""

            # Reference Point Autoset
            if bitstring[0] == "0":
                flags += "m"
            else:
                flags += "M"

            # Minimum Distance
            if bitstring[1] == "0":
                flags += "<"
            else:
                flags += ">"

            # Rounding
            if bitstring[2] == "0":
                flags += "r"  # do not round distance
            else:
                flags += "R"  # round distance

            # Color
            return flags + self.bitstring_to_color_mnemonic(bitstring[3:])

        # Unknown command
        raise KeyError

    def bitstring_to_color_mnemonic(self, bitstring: str) -> str:
        """
        Return VTT distance color mnemonics for a bit string
        """
        if bitstring == "00":
            return "Gr"  # Gray
        elif bitstring == "01":
            return "Bl"  # Black
        elif bitstring == "10":
            return "Wh"  # White
        # "11" is not defined
        raise KeyError
