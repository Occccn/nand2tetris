from typing import Literal


class CodeWriter:
    def __init__(self, path: str) -> None:
        self.f_stream = open(path, "w")

    def writeAtithmetic(self, command: str) -> None:
        pass

    def writePushPop(self, command: Literal["C_PUSH", "C_POP"], segment: str, index: int) -> None:
        # RAM[0]の位置にstaclの最上位のアドレスがある
        # local/argument/this/thatの最上位アドレスはRAM[1]~RAM[4]に格納されている
        # constantはその値をスタックに格納する
        # temp iはRAM[5+i]に格納されている
        # pointer 0はthis, 1はthatにアクセス

        # if command == "C_PUSH":
        #     if segment == "constant":

        pass

    def close(self) -> None:
        self.f_stream.close()
