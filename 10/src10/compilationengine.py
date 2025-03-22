from src10.jacktokenizer import JackTokenizer


class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.jacktokenizer = JackTokenizer(input_file)
        self.jacktokenizer.get_tokens()
        self.jacktokenizer.advance()
        self.jacktokenizer.tokenType()
        self.f = open(output_file, "w")
        self.indent = 0

    def run(self) -> None:
        self.compileClass()
        self.f.close()

    def _write_markup(self, token_type: str, token: str, indent: int) -> None:
        self.f.write(f"{'  ' * indent}<{token_type}> {token} </{token_type}>\n")

    def _write_markup_no_token(self, token_type: str, indent: int) -> None:
        self.f.write(f"{'  ' * indent}<{token_type}>\n")

    def compileClass(self) -> None:
        """classをコンパイルする"""
        self._write_markup_no_token("class", self.indent)
        self.indent += 1
        self.compileKeyword("class")
        self.compileIdentifier()
        self.compileSymbol("{")
        while self.jacktokenizer.current_token in ["static", "field"]:
            self.compileClassVarDec()
        while self.jacktokenizer.current_token in ["constructor", "function", "method"]:
            self.compileSubroutine()
        self.compileSymbol("}")
        self.indent -= 1
        self._write_markup_no_token("class", self.indent)

    def compileClassVarDec(self) -> None:
        """classVarDecをコンパイルする"""
        self._write_markup_no_token("classVarDec", self.indent)
        self.indent += 1
        self.compileKeyword(["static", "field"])
        self.compileKeyword(["int", "char", "boolean"])
        self.compileIdentifier()
        while self.jacktokenizer.current_token == ",":
            self.compileSymbol(",")
            self.compileIdentifier()
        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("classVarDec", self.indent)

    def compileSubroutine(self) -> None:
        """subroutineをコンパイルする"""
        self._write_markup_no_token("subroutineDec", self.indent)
        self.indent += 1
        self.compileKeyword(["constructor", "function", "method"])
        self.compileKeyword(["void", "int", "char", "boolean"])
        self.compileIdentifier()
        self.compileSymbol("(")
        self.compileParameterList()
        self.compileSymbol(")")
        self.compileSubroutineBody()
        self.indent -= 1

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

    def compileVarDec(self):
        pass

    def compileStatements(self):
        pass

    def compileDo(self):
        pass

    def compileLet(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass

    def compileKeyword(self, correct_token: list[str] | str):
        """keywordをコンパイルする"""
        if isinstance(correct_token, list):
            if self.jacktokenizer.current_token in correct_token & self.jacktokenizer.token_type == "keyword":
                self._write_markup("keyword", self.jacktokenizer.current_token, self.indent)
                self.jacktokenizer.advance()
            else:
                raise ValueError(f"expected {correct_token} but got {self.jacktokenizer.current_token}")
        else:
            if self.jacktokenizer.current_token == correct_token & self.jacktokenizer.token_type == "keyword":
                self._write_markup("keyword", correct_token, self.indent)
                self.jacktokenizer.advance()
            else:
                raise ValueError(f"expected {correct_token} but got {self.jacktokenizer.current_token}")

    def compileIdentifier(self):
        """identifierをコンパイルする

        Raises:
            ValueError: _description_
        """
        if self.jacktokenizer.token_type == "identifier":
            self._write_markup("identifier", self.jacktokenizer.current_token, self.indent)
            self.jacktokenizer.advance()
        else:
            raise ValueError(f"expected identifier but got {self.jacktokenizer.current_token}")

    def compileSymbol(self, correct_token: str):
        """symbolをコンパイルする"""
        if self.jacktokenizer.current_token == correct_token & self.jacktokenizer.token_type == "symbol":
            self._write_markup("symbol", correct_token, self.indent)
            self.jacktokenizer.advance()
        else:
            raise ValueError(f"expected {correct_token} but got {self.jacktokenizer.current_token}")
