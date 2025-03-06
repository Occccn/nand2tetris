from typing import Literal


class CodeWriter:
    def __init__(self, path: str) -> None:
        self.f_stream = open(path, "w")
        self.push_stack = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # pushするためのアドレスが指定されているため、popする際は-1が必要
        # self.pop_stack = "@SP\nA=M-1\nD=M\n@SP\nM=M-1\n"
        self.pop_stack = "@SP\nM=M-1\n@SP\nA=M\nD=M\n"
        self.count_eq = 1
        self.count_gt = 1
        self.count_lt = 1

    def writeAtithmetic(self, command: str) -> None:
        if command == "add":
            self.f_stream.write(f"{self.pop_stack}@SP\nM=M-1\n@SP\nA=M\nM=D+M\n@SP\nM=M+1\n")
        elif command == "sub":
            self.f_stream.write(f"{self.pop_stack}@SP\nM=M-1\n@SP\nA=M\nM=M-D\n@SP\nM=M+1\n")
        elif command == "neg":
            self.f_stream.write("@SP\nA=M-1\nM=-M\n")
        elif command == "eq":
            self.f_stream.write(
                f"{self.pop_stack}A=A-1\nD=M-D\n@EQ_TRUE{self.count_eq}\nD;JEQ\n@SP\nA=M-1\nM=0\n@EQ_END{self.count_eq}\n0;JMP\n(EQ_TRUE{self.count_eq})\n@SP\nA=M-1\nM=-1\n(EQ_END{self.count_eq})\n"
            )
            self.count_eq += 1
        elif command == "gt":
            self.f_stream.write(
                f"{self.pop_stack}A=A-1\nD=M-D\n@GT_TRUE{self.count_gt}\nD;JGT\n@SP\nA=M-1\nM=0\n@GT_END{self.count_gt}\n0;JMP\n(GT_TRUE{self.count_gt})\n@SP\nA=M-1\nM=-1\n(GT_END{self.count_gt})\n"
            )
            self.count_gt += 1
        elif command == "lt":
            self.f_stream.write(
                f"{self.pop_stack}A=A-1\nD=M-D\n@LT_TRUE{self.count_lt}\nD;JLT\n@SP\nA=M-1\nM=0\n@LT_END{self.count_lt}\n0;JMP\n(LT_TRUE{self.count_lt})\n@SP\nA=M-1\nM=-1\n(LT_END{self.count_lt})\n"
            )
            self.count_lt += 1
        elif command == "and":
            self.f_stream.write(f"{self.pop_stack}A=A-1\nM=D&M\n")
        elif command == "or":
            self.f_stream.write(f"{self.pop_stack}A=A-1\nM=D|M\n")
        elif command == "not":
            self.f_stream.write("@SP\nA=M-1\nM=!M\n")

    def writePushPop(self, command: Literal["C_PUSH", "C_POP"], segment: str, index: int) -> None:
        if command == "C_PUSH":
            if segment == "constant":
                self.f_stream.write(f"@{index}\nD=A\n{self.push_stack}")
            elif segment == "temp":
                self.f_stream.write(f"@{5 + index}\nD=M\n{self.push_stack}")
            elif segment == "pointer":
                self.f_stream.write(f"@{3 + index}\nD=M\n{self.push_stack}")
            elif segment == "static":
                self.f_stream.write(f"@{index + 16}\nD=M\n{self.push_stack}")
            elif segment == "local":
                self.f_stream.write(f"@{index}\nD=A\n@LCL\nA=D+M\nD=M\n{self.push_stack}")
            elif segment == "argument":
                self.f_stream.write(f"@{index}\nD=A\n@ARG\nA=D+M\nD=M\n{self.push_stack}")
            elif segment == "this":
                self.f_stream.write(f"@{index}\nD=A\n@THIS\nA=D+M\nD=M\n{self.push_stack}")
            elif segment == "that":
                self.f_stream.write(f"@{index}\nD=A\n@THAT\nA=D+M\nD=M\n{self.push_stack}")
        elif command == "C_POP":
            if segment == "temp":
                self.f_stream.write(f"{self.pop_stack}@{5 + index}\nM=D\n")
            elif segment == "pointer":
                self.f_stream.write(f"{self.pop_stack}@{3 + index}\nM=D\n")
            elif segment == "static":
                self.f_stream.write(f"{self.pop_stack}@{index + 16}\nM=D\n")
            elif segment == "local":
                self.f_stream.write(f"@{index}\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")
            elif segment == "argument":
                self.f_stream.write(f"@{index}\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")
            elif segment == "this":
                self.f_stream.write(f"@{index}\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")
            elif segment == "that":
                self.f_stream.write(f"@{index}\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n{self.pop_stack}@R13\nA=M\nM=D\n")

        pass

        def writeLabel(self, label: str) -> None:
            self.f_stream.write(f"({label})\n")

        def writeGoto(self, label: str) -> None:
            self.f_stream.write(f"@{label}\n0;JMP\n")

        def writeIf(self, label: str) -> None:
            self.f_stream.write(f"{self.pop_stack}@{label}\nD;JNE\n")

    def debug(self, current_line: str) -> None:
        self.f_stream.write(f"// {current_line}\n")

    def close(self) -> None:
        self.f_stream.close()
