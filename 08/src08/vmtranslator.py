import argparse
from pathlib import Path

from src08.codewriter import CodeWriter
from src08.parser import Parser

BASE_DIR = Path(__file__).parents[1]


class VMTranslator:
    def __init__(self, dirname, filename):
        self.dir = dirname
        dir_path = BASE_DIR / "vm" / self.dir / filename
        self.input_paths = list(dir_path.glob("*.vm"))
        self.outputpath = BASE_DIR / "vm" / self.dir / filename / f"{filename}.asm"
        self.parsers = [Parser(path) for path in self.input_paths]
        self.code_writer = CodeWriter(self.outputpath)

    def bootstrap(self):
        self.code_writer.writeInit()

    def translate(self, parser: Parser):
        while parser.HasMoreLines():
            parser.advance()
            command_type = parser.commandType()
            self.code_writer.debug(parser.current_line)
            arg = parser.arg1()
            if command_type == "C_ARITHMETIC":
                self.code_writer.writeAtithmetic(arg)
            if command_type in ["C_PUSH", "C_POP"]:
                index = parser.arg2()
                self.code_writer.writePushPop(command_type, arg, index)
            if command_type == "C_LABEL":
                self.code_writer.writeLabel(arg)
            if command_type == "C_GOTO":
                self.code_writer.writeGoto(arg)
            if command_type == "C_IF":
                self.code_writer.writeIf(arg)
            if command_type == "C_FUNCTION":
                self.code_writer.writeFunction(arg, parser.arg2())
            if command_type == "C_RETURN":
                self.code_writer.writeReturn()
            if command_type == "C_CALL":
                self.code_writer.writeCall(arg, parser.arg2())

    def run(self):
        self.bootstrap()
        for parser in self.parsers:
            self.code_writer.setFileName(parser.filename)
            self.translate(parser)
        self.code_writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vmtranslator for nand2tetris")

    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument("-f", "--file", help="file name to vm", required=True)
    parser.add_argument("-d", "--dir", help="dir name to vm", required=True)
    args = parser.parse_args()  # 4. 引数を解析

    vmtranslator = VMTranslator(filename=args.file, dirname=args.dir)
    vmtranslator.run()
