from collections import deque
from typing import Literal

from src08.arithmetic import Arithmetic


class Parser:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines = deque(f.readlines())

        ## read the file
        self.current_line_number: int = 0
        self.arithmetic: Arithmetic = Arithmetic()

    def HasMoreLines(self) -> bool:
        if len(self.lines) == 0:
            return False
        else:
            return True

    def advance(self) -> None:
        while self.HasMoreLines():
            self.current_line = self.lines.popleft()
            self.current_line = self.current_line.strip()
            if self.current_line.startswith("//") or self.current_line == "\n" or self.current_line == "":
                continue
            else:
                self.current_line = self.current_line.strip()
                break

    def commandType(
        self,
    ) -> (
        Literal["C_ARITHMETIC", "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION", "C_RETURN", "C_CALL"]
        | None
    ):
        # C_ARITHMETIC
        if (
            self.current_line.split()[0]
            in self.arithmetic.arithmetic + self.arithmetic.comparison + self.arithmetic.logical
        ):
            return "C_ARITHMETIC"
        # C_PUSH
        if self.current_line.startswith("push"):
            return "C_PUSH"
        # C_POP
        elif self.current_line.startswith("pop"):
            return "C_POP"
        elif self.current_line.startswith("label"):
            return "C_LABEL"
        elif self.current_line.startswith("goto"):
            return "C_GOTO"
        elif self.current_line.startswith("if"):
            return "C_IF"
        elif self.current_line.startswith("function"):
            return "C_FUNCTION"
        elif self.current_line.startswith("return"):
            return "C_RETURN"
        elif self.current_line.startswith("call"):
            return "C_CALL"
        return None

    def arg1(self) -> str:
        if self.commandType() == "C_ARITHMETIC":
            return self.current_line
        else:
            return self.current_line.split()[1]

    def arg2(self) -> int | None:
        # if self.commandType() in ["C_POP", "C_FUNCTION", "C_CALL", "C_PUSH"]:
        return int(self.current_line.split()[2])
