from typing import Literal


class CodeWriter:
    def __init__(self, path: str) -> None:
        self.f_stream = open(path, "w")
        self.push_stack = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # pushするためのアドレスが指定されているため、popする際は-1が必要
        self.pop_stack = "@SP\nA=M-1\nD=M\n@SP\nM=M-1\n"

    def writeAtithmetic(self, command: str) -> None:
        if command == "add":
            self.f_stream.write(f"{self.pop_stack}A=A-1\nM=M+D\n")
        elif command == "sub":
            self.f_stream.write(f"{self.pop_stack}A=A-1\nM=M-D\n")
        elif command == "neg":
            self.f_stream.write("@SP\nA=M-1\nM=-M\n")
        elif command == "eq":
            pass
        elif command == "gt":
            pass
        elif command == "lt":
            pass
        elif command == "and":
            pass
        elif command == "or":
            pass
        elif command == "not":
            pass
        pass

    def writePushPop(self, command: Literal["C_PUSH", "C_POP"], segment: str, index: int) -> None:
        if command == "C_PUSH":
            if segment == "constant":
                self.f_stream.write(f"@{index}\nD=A\n{self.push_stack}")
            elif segment == "temp":
                self.f_stream.write(f"@{5 + index}\\D=M\n{self.push_stack}")
            elif segment == "pointer":
                self.f_stream.write(f"@{3 + index}\\D=M\n{self.push_stack}")
            elif segment == "static":
                self.f_stream.write(f"@{index + 16}\\D=M\n{self.push_stack}")
            elif segment == "local":
                self.f_stream.write(f"@{index}\\D=A\n@LCL\nA=M+D\nD=M\n{self.push_stack}")
            elif segment == "argument":
                self.f_stream.write(f"@{index}\\D=A\n@ARG\nA=M+D\nD=M\n{self.push_stack}")
            elif segment == "this":
                self.f_stream.write(f"@{index}\\D=A\n@THIS\nA=M+D\nD=M\n{self.push_stack}")
            elif segment == "that":
                self.f_stream.write(f"@{index}\\D=A\n@THAT\nA=M+D\nD=M\n{self.push_stack}")
        elif command == "C_POP":
            if segment == "temp":
                self.f_stream.write(f"{self.pop_stack}@{5 + index}\nM=D\n")
            elif segment == "pointer":
                self.f_stream.write(f"{self.pop_stack}@{3 + index}\nM=D\n")
            elif segment == "static":
                self.f_stream.write(f"{self.pop_stack}@{index + 16}\nM=D\n")
            elif segment == "local":
                self.f_stream.write(f"@{index}\\D=A\n@LCL\nD=M+D\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")
            elif segment == "argument":
                self.f_stream.write(f"@{index}\\D=A\n@ARG\nD=M+D\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")
            elif segment == "this":
                self.f_stream.write(f"@{index}\\D=A\n@THIS\nD=M+D\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")
            elif segment == "that":
                self.f_stream.write(f"@{index}\\D=A\n@THAT\nD=M+D\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")

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
