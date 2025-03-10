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
        self.count_cl = 1

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

        def writeFunction(self, function_name: str, nVars: int) -> None:
            self.f_stream.write(f"({function_name})\n")
            for _ in range(nVars):
                self.f_stream.write(f"@0\nD=A\n{self.push_stack}")

        def writeCall(self, function_name: str, nArgs: int) -> None:
            return_address = f"{function_name}{self.count_cl}"
            self.count_cl += 1
            # return_addressを先に生成して、pushhしても6章のassemblerにおけるfirst_passで
            # シンボルテーブルに登録されるため、問題ない
            # 各種のアドレスをpushする。pushすることで、呼び出し先から触れない
            self.f_stream.write(f"@{return_address}\nD=A\n{self.push_stack}\n")
            self.f_stream.write(f"@LCL\nD=M\n{self.push_stack}\n")
            self.f_stream.write(f"@ARG\nD=M\n{self.push_stack}\n")
            self.f_stream.write(f"@THIS\nD=M\n{self.push_stack}\n")
            self.f_stream.write(f"@THAT\nD=M\n{self.push_stack}\n")
            # ARG/LCLは呼び出し先の関数ように設定する
            self.f_stream.write(f"@SP\nD=M\n@5\nD=D-A\n@{nArgs}\nD=D-A\n@ARG\nM=D\n")
            self.f_stream.write("@SP\nD=M\n@LCL\nM=D\n")
            # 関数にジャンプ
            self.f_stream.write(f"@{function_name}\n0;JMP\n")
            # return_addressを追加
            self.f_stream.write(f"({return_address})\n")

        def writeReturn(self) -> None:
            # LCLをR13に一時保存する
            self.f_stream.write("@LCL\nD=M\n@R13\nM=D\n")
            # returnAddressをR14に一時保存
            self.f_stream.write("@13\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n")
            # *ARG = pop()
            self.f_stream.write(f"{self.pop_stack}@ARG\nA=M\nM=D\n")
            # SP = ARG + 1
            self.f_stream.write("@ARG\nD=M+1\n@SP\nM=D\n")
            # THAT = *(endFrame - 1)
            self.f_stream.write("@R13\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n")
            # THIS = *(endFrame - 2)
            self.f_stream.write("@R13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n")
            # ARG = *(endFrame - 3)
            self.f_stream.write("@R13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n")
            # LCL = *(endFrame - 4)
            self.f_stream.write("@R13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n")
            # goto returnAddress
            self.f_stream.write("@R14\nA=M\n0;JMP\n")

    def debug(self, current_line: str) -> None:
        self.f_stream.write(f"// {current_line}\n")

    def close(self) -> None:
        self.f_stream.close()
