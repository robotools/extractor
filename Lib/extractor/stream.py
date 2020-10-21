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

    def __init__(self, instruction_processor=None, program_bytes=b""):
        self.io = BytesIO(program_bytes)

    def rewind(self):
        """
        Rewind the instruction pointer to the beginning of the stream.
        """
        self.io.seek(0)

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

    def __repr__(self):
        """
        Print the instructions from the bytecode in the current stream starting
        at the beginning.
        """
        self.rewind()

        asm = ""
        indent = 0

        more = True
        while more:
            opcode = self.io.read(1)
            if opcode:
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
                        args.append(str(num_args))
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
                    arg_bitstring = " "
                else:
                    arg_bitstring = num2binary(opcode - base_opcode, arg_bits)

                if cmd_name in ("NPUSHB", "NPUSHW", "PUSHB", "PUSHW"):
                    num_args = len(args)
                    val = "value" if num_args == 1 else "values"
                    asm += f"\n{'  ' * indent}{cmd_name}[{arg_bitstring}]\t/* {num_args} {val} pushed */"
                else:
                    asm += f"\n{'  ' * indent}{cmd_name}[{arg_bitstring}]\t/* {name} */"

                if args:
                    asm += f"\n{'  ' * indent}{' '.join(args)}"

                if cmd_name in ("ELSE", "FDEF", "IF"):
                    indent += 1
            else:
                more = False
        return asm.strip()
