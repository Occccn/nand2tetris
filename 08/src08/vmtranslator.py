import argparse
from pathlib import Path

from src08.codewriter import CodeWriter
from src08.parser import Parser

BASE_DIR = Path(__file__).parents[1]


class VMTranslator:
    def __init__(self, dirname, filename):
        self.dir = dirname
        self.inputpath = BASE_DIR / "vm" / self.dir / filename / f"{filename}.vm"
        self.outputpath = BASE_DIR / "vm" / self.dir / filename / f"{filename}.asm"
        self.parser = Parser(self.inputpath)
        self.code_writer = CodeWriter(self.outputpath)

    def translate(self):
        while self.parser.HasMoreLines():
            self.parser.advance()
            command_type = self.parser.commandType()
            self.code_writer.debug(self.parser.current_line)
            arg = self.parser.arg1()
            if command_type == "C_ARITHMETIC":
                self.code_writer.writeAtithmetic(arg)
            if command_type in ["C_PUSH", "C_POP"]:
                index = self.parser.arg2()
                self.code_writer.writePushPop(command_type, arg, index)
        self.code_writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vmtranslator for nand2tetris")

    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument("-f", "--file", help="file name to vm", required=True)
    parser.add_argument("-d", "--dir", help="dir name to vm", required=True)
    args = parser.parse_args()  # 4. 引数を解析

    vmtranslator = VMTranslator(args.file, args.dir)
    vmtranslator.translate()
