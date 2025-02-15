from collections import deque
from pathlib import Path

from src06.code import Code
from src06.parser import Parser
from src06.symboltable import SymbolTable

BASE_DIR = Path(__file__).parents[1]


class Assembler:
    def __init__(self, filename):
        self.binary_instructions = deque([])
        self.symbol_table = SymbolTable()
        self.filename = filename

    def first_pass(self):
        self.p = Parser(BASE_DIR / "asm" / self.filename)
        while self.p.HasMoreLines():
            self.p.advance()
            if self.p.InstructionType() == "L_INSTRUCTION":
                symbol = self.p.symbol()
                if not self.symbol_table.contains(symbol):
                    symbol = self.p.symbol()
                    self.symbol_table.addEntry(symbol, self.p.current_line_number)
                else:
                    continue
            # elif self.p.InstructionType() == "A_INSTRUCTION":
            #     symbol = self.p.symbol()
            #     if not self.symbol_table.contains(symbol):
            #         symbol = self.p.symbol()
            #         address = 1
            #         self.symbol_table.addEntry(symbol, address)

    def compile_assembler(self):
        self.p = Parser(BASE_DIR / "asm" / self.filename)
        while self.p.HasMoreLines():
            self.p.advance()
            if self.p.InstructionType() == "A_INSTRUCTION":
                symbol = self.p.symbol()
                # シンボルが数値の場合のみに対応
                if symbol.isdigit():
                    self.binary_instructions.append(f"0{int(symbol):015b}")
                else:
                    if not self.symbol_table.contains(symbol):
                        self.symbol_table.addEntry(symbol, self.symbol_table.current_address)
                        self.symbol_table.current_address += 1
                    else:
                        pass
                    self.binary_instructions.append(f"0{self.symbol_table.getAddress(symbol):015b}")
            elif self.p.InstructionType() == "C_INSTRUCTION":
                dest = self.p.dest()
                comp = self.p.comp()
                jump = self.p.jump()
                self.binary_instructions.append(f"111{Code.comp(comp)}{Code.dest(dest)}{Code.jump(jump)}")
            else:
                continue

    def write_binary(self):
        with open("output.hack", "w") as f:
            for i in range(len(self.binary_instructions)):
                instruction = self.binary_instructions[i]
                if i == len(self.binary_instructions) - 1:
                    f.write(instruction)
                else:
                    f.write(instruction + "\n")


if __name__ == "__main__":
    assembler = Assembler("pong/Pong.asm")
    assembler.first_pass()
    assembler.compile_assembler()
    assembler.write_binary()
