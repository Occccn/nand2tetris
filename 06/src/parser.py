from collections import deque
from typing import Literal

import ipdb


class Parser:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines = deque(f.readlines())

        ## read the file

    def HasMoreLines(self) -> bool:
        if len(self.lines) == 0:
            return False
        else:
            return True

    def advance(self) -> None:
        while self.HasMoreLines():
            self.current_line = self.lines.popleft()
            if self.current_line.startswith("//") or self.current_line == "\n":
                continue
            else:
                self.current_line = self.current_line.strip()
                break

    def InstructionType(self) -> Literal["A_INSTRUCTION", "C_INSTRUCTION", "L_INSTRUCTION"]:
        if self.current_line.startswith("@"):
            return "A_INSTRUCTION"
        elif self.current_line.startswith("("):
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"

    def symbol(self) -> str:
        if self.InstructionType() == "A_INSTRUCTION":
            return self.current_line[1:].strip()
        elif self.InstructionType() == "L_INSTRUCTION":
            return self.current_line[1:-1].strip()
        else:
            return ""

    def dest(self) -> str:
        if "=" in self.current_line:
            return self.current_line.split("=")[0]
        else:
            return ""

    def comp(self) -> str:
        if "=" in self.current_line:
            part1 = self.current_line.split("=")[1]
            if ";" in part1:
                return part1.split(";")[0]
            else:
                return part1
        else:
            if ";" in self.current_line:
                return self.current_line.split(";")[0]
            else:
                return self.current_line

    def jump(self) -> str:
        if ";" in self.current_line:
            return self.current_line.split(";")[1]
        else:
            return ""


if __name__ == "__main__":
    p = Parser("asm/add/Add.asm")
    print(p.lines)
    p.advance()
    ipdb.set_trace()
    # while p.HasMoreLines():
    #     p.advance()
    #     print(p.InstructionType(), p.symbol(), p.dest(), p.comp(), p.jump())
