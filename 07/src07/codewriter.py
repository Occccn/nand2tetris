from typing import Literal


class CodeWriter:
    def __init__(self, path: str) -> None:
        self.f_stream = open(path, "w")

    def writeAtithmetic(self, command: str) -> None:
        pass

    def writePushPop(self, command: Literal["C_PUSH", "C_POP"], segment: str, index: int) -> None:
        # if command == "C_PUSH":
        #     if segment == "constant":
                
        # pass

    def close(self) -> None:
        self.f_stream.close()
