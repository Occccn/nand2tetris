from code import Code
from collections import deque
from pathlib import Path

from parser import Parser

BASE_DIR = Path(__file__).parents[1]


class Assembler:
    def __init__(self, filename):
        self.p = Parser(BASE_DIR / "asm" / filename)
        self.binary_instructions = deque([])

    def compile_assembler(self):
        while self.p.HasMoreLines():
            self.p.advance()
            if self.p.InstructionType() == "A_INSTRUCTION":
                symbol = self.p.symbol()
                # シンボルが数値の場合のみに対応
                self.binary_instructions.append(f"0{int(symbol):015b}")
            elif self.p.InstructionType() == "C_INSTRUCTION":
                dest = self.p.dest()
                comp = self.p.comp()
                jump = self.p.jump()
                self.binary_instructions.append(f"111{Code.comp(comp)}{Code.dest(dest)}{Code.jump(jump)}")
            else:
                continue

    def write_binary(self):
        with open("output.hack", "w") as f:
            for instruction in self.binary_instructions:
                f.write(instruction + "\n")


if __name__ == "__main__":
    assembler = Assembler("add/Add.asm")
    assembler.compile_assembler()
    assembler.write_binary()
