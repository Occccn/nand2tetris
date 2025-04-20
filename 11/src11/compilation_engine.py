from src11.jacktokenizer import JackTokenizer
from src11.symboltable import SymbolTable
from src11.vmwriter import VMWriter


class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.jacktokenizer = JackTokenizer(input_file)
        self.jacktokenizer.get_tokens()
        self.jacktokenizer.advance()
        self.jacktokenizer.tokenType()
        self.f = open(output_file, "w")
        self.indent = 0
        self.class_table = SymbolTable()
        self.vm_writer = VMWriter(output_file.with_suffix(".vm"))

    def run(self) -> None:
        self.compileClass()
        self.f.close()

    def _write_markup(self, token_type: str, token: str, indent: int) -> None:
        self.f.write(f"{'  ' * indent}<{token_type}> {token} </{token_type}>\n")

    def _write_markup_no_token(self, token_type: str, indent: int, closed: bool) -> None:
        if closed:
            self.f.write(f"{'  ' * indent}</{token_type}>\n")
        else:
            self.f.write(f"{'  ' * indent}<{token_type}>\n")

    def compileClass(self) -> None:
        """classをコンパイルする"""
        self._write_markup_no_token("class", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("class")
        self.compileIdentifier(category="class", usage=False)
        self.compileSymbol("{")
        while self.jacktokenizer.current_token in ["static", "field"]:
            self.compileClassVarDec()
        while self.jacktokenizer.current_token in ["constructor", "function", "method"]:
            self.compileSubroutine()
        self.compileSymbol("}")
        self.indent -= 1
        self._write_markup_no_token("class", self.indent, closed=True)

    def compileClassVarDec(self) -> None:
        """classVarDecをコンパイルする"""
        self._write_markup_no_token("classVarDec", self.indent, closed=False)
        self.indent += 1
        _keyword = self.jacktokenizer.keyWord()
        self.compileKeyword(["static", "field"])
        _type = self.jacktokenizer.current_token
        self.compileType(["int", "char", "boolean"])
        self.class_table.define(self.jacktokenizer.current_token, _type, _keyword)
        index = self.class_table.indexOf(self.jacktokenizer.current_token)
        self.compileIdentifier(category=_keyword, usage=True, index=index)
        while self.jacktokenizer.current_token == ",":
            self.compileSymbol(",")
            self.class_table.define(self.jacktokenizer.current_token, _type, _keyword)
            index = self.class_table.indexOf(self.jacktokenizer.current_token)
            self.compileIdentifier(category=_keyword, usage=True, index=index)
        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("classVarDec", self.indent, closed=True)

    def compileSubroutine(self) -> None:
        """subroutineをコンパイルする"""
        self.subroutine_table = SymbolTable()
        self._write_markup_no_token("subroutineDec", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword(["constructor", "function", "method"])
        self.compileType(["void", "int", "char", "boolean"])
        self.compileIdentifier(category="subroutine", usage=False)
        self.compileSymbol("(")
        self.compileParameterList()
        self.compileSymbol(")")
        self.compileSubroutineBody()
        self.indent -= 1
        self._write_markup_no_token("subroutineDec", self.indent, closed=True)

    def compileParameterList(self):
        """parameterListをコンパイルする"""
        self._write_markup_no_token("parameterList", self.indent, closed=False)
        self.indent += 1
        while self.jacktokenizer.current_token != ")":
            _keyword = self.jacktokenizer.current_token
            self.compileType(["int", "char", "boolean"])
            self.subroutine_table.define(self.jacktokenizer.current_token, _keyword, "ARG")
            index = self.subroutine_table.indexOf(self.jacktokenizer.current_token)
            self.vm_writer.write_push("ARGUMENT", index)
            self.compileIdentifier(category="ARG", usage=False, index=index)
            if self.jacktokenizer.current_token == ",":
                self.compileSymbol(",")
        self.indent -= 1
        self._write_markup_no_token("parameterList", self.indent, closed=True)
        pass

    def compileSubroutineBody(self):
        """subroutineBodyをコンパイルする"""
        self._write_markup_no_token("subroutineBody", self.indent, closed=False)
        self.indent += 1
        self.compileSymbol("{")
        while self.jacktokenizer.current_token == "var":
            self.compileVarDec()
        self.compileStatements()
        self.compileSymbol("}")
        self.indent -= 1
        self._write_markup_no_token("subroutineBody", self.indent, closed=True)

    def compileVarDec(self):
        """varDecをコンパイルする"""
        self._write_markup_no_token("varDec", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("var")
        _type = self.jacktokenizer.current_token
        self.compileType(["int", "char", "boolean"])
        self.subroutine_table.define(self.jacktokenizer.current_token, _type, "VAR")
        index = self.subroutine_table.indexOf(self.jacktokenizer.current_token)
        self.compileIdentifier(category="VAR", usage=True, index=index)
        while self.jacktokenizer.current_token == ",":
            self.compileSymbol(",")
            self.subroutine_table.define(self.jacktokenizer.current_token, _type, "VAR")
            index = self.subroutine_table.indexOf(self.jacktokenizer.current_token)
            self.compileIdentifier(category="VAR", usage=True, index=index)
        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("varDec", self.indent, closed=True)

    def compileStatements(self):
        """statementsをコンパイルする"""
        self._write_markup_no_token("statements", self.indent, closed=False)
        self.indent += 1
        while self.jacktokenizer.current_token in ["let", "if", "while", "do", "return"]:
            if self.jacktokenizer.current_token == "let":
                self.compileLet()
            elif self.jacktokenizer.current_token == "if":
                self.compileIf()
            elif self.jacktokenizer.current_token == "while":
                self.compileWhile()
            elif self.jacktokenizer.current_token == "do":
                self.compileDo()
            elif self.jacktokenizer.current_token == "return":
                self.compileReturn()
        self.indent -= 1
        self._write_markup_no_token("statements", self.indent, closed=True)

    def compileDo(self):
        """doをコンパイルする"""
        self._write_markup_no_token("doStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("do")
        self.compileIdentifier(category="subroutine", usage=False)
        self.compileSubroutineCall()
        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("doStatement", self.indent, closed=True)

    def compileSubroutineCall(self):
        """subroutineCallをコンパイルする"""
        # self.compileIdentifier()
        if self.jacktokenizer.current_token == ".":
            self.compileSymbol(".")
            self.compileIdentifier(category="subroutine", usage=False)
        self.compileSymbol("(")
        self.compileExpressionList()
        self.compileSymbol(")")

    def compileLet(self):
        """letをコンパイルする"""
        self._write_markup_no_token("letStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("let")
        self.compileIdentifier(category="VAR", usage=False)
        if self.jacktokenizer.current_token == "[":
            self.compileSymbol("[")
            self.compileExpression()
            self.compileSymbol("]")
        self.compileSymbol("=")
        self.compileExpression()
        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("letStatement", self.indent, closed=True)

    def compileWhile(self):
        """whileをコンパイルする"""
        self._write_markup_no_token("whileStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("while")
        self.compileSymbol("(")
        self.compileExpression()
        self.compileSymbol(")")
        self.compileSymbol("{")
        self.compileStatements()
        self.compileSymbol("}")
        self.indent -= 1
        self._write_markup_no_token("whileStatement", self.indent, closed=True)

    def compileReturn(self):
        """returnをコンパイルする"""
        self._write_markup_no_token("returnStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("return")
        if self.jacktokenizer.current_token != ";":
            self.compileExpression()
        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("returnStatement", self.indent, closed=True)

    def compileIf(self):
        """ifをコンパイルする"""
        self._write_markup_no_token("ifStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("if")
        self.compileSymbol("(")
        self.compileExpression()
        self.compileSymbol(")")
        self.compileSymbol("{")
        self.compileStatements()
        self.compileSymbol("}")
        if self.jacktokenizer.current_token == "else":
            self.compileKeyword("else")
            self.compileSymbol("{")
            self.compileStatements()
            self.compileSymbol("}")
        self.indent -= 1
        self._write_markup_no_token("ifStatement", self.indent, closed=True)

    def compileExpression(self):
        """expressionをコンパイルする"""
        self._write_markup_no_token("expression", self.indent, closed=False)
        self.indent += 1
        self.compileTerm()
        while self.jacktokenizer.current_token in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.compileSymbol(self.jacktokenizer.current_token)
            self.compileTerm()
        self.indent -= 1
        self._write_markup_no_token("expression", self.indent, closed=True)

    def compileTerm(self):
        """termをコンパイルする"""
        self._write_markup_no_token("term", self.indent, closed=False)
        self.indent += 1
        if self.jacktokenizer.tokenType() == "int_const":
            self._write_markup("integerConstant", self.jacktokenizer.current_token, self.indent)
            self.vm_writer.write_push("CONSTANT", int(self.jacktokenizer.current_token))
            self.jacktokenizer.advance()
        elif self.jacktokenizer.tokenType() == "string_const":
            self._write_markup("stringConstant", self.jacktokenizer.current_token[1:-1], self.indent)
            self.jacktokenizer.advance()
        elif self.jacktokenizer.tokenType() == "keyword":
            self.compileKeyword(["true", "false", "null", "this"])
        elif self.jacktokenizer.tokenType() == "identifier":
            self.compileIdentifier(category="VAR", usage=False)
            if self.jacktokenizer.current_token == "[":
                self.compileSymbol("[")
                self.compileExpression()
                self.compileSymbol("]")
            elif self.jacktokenizer.current_token in ["(", "."]:
                self.compileSubroutineCall()
        elif self.jacktokenizer.current_token in ["-", "~"]:
            self.compileSymbol(self.jacktokenizer.current_token)
            self.compileTerm()
        elif self.jacktokenizer.current_token == "(":
            self.compileSymbol("(")
            self.compileExpression()
            self.compileSymbol(")")
        else:
            raise ValueError(f"expected term but got {self.jacktokenizer.current_token}")
        self.indent -= 1
        self._write_markup_no_token("term", self.indent, closed=True)

    def compileExpressionList(self):
        """expressionListをコンパイルする"""
        self._write_markup_no_token("expressionList", self.indent, closed=False)
        self.indent += 1
        while self.jacktokenizer.current_token != ")":
            self.compileExpression()
            if self.jacktokenizer.current_token == ",":
                self.compileSymbol(",")
        self.indent -= 1
        self._write_markup_no_token("expressionList", self.indent, closed=True)

    def compileKeyword(self, correct_token: list[str] | str):
        """keywordをコンパイルする"""
        if isinstance(correct_token, list):
            if (self.jacktokenizer.current_token in correct_token) & (self.jacktokenizer.tokenType() == "keyword"):
                self._write_markup(self.jacktokenizer.tokenType(), self.jacktokenizer.current_token, self.indent)
                self.jacktokenizer.advance()
            else:
                raise ValueError(f"expected {correct_token} but got {self.jacktokenizer.current_token}")
        else:
            if (self.jacktokenizer.current_token == correct_token) & (self.jacktokenizer.tokenType() == "keyword"):
                self._write_markup("keyword", correct_token, self.indent)
                self.jacktokenizer.advance()
            else:
                raise ValueError(f"expected {correct_token} but got {self.jacktokenizer.current_token}")

    def compileIdentifier(self, category: str, usage: bool, index: int | None = None):
        """identifierをコンパイルする

        Raises:
            ValueError: _description_
        """
        if self.jacktokenizer.tokenType() == "identifier":
            self._write_markup(
                "identifier",
                f"{self.jacktokenizer.current_token} category:{category} usage:{usage} index:{index}",
                self.indent,
            )
            self.jacktokenizer.advance()
        else:
            raise ValueError(f"expected identifier but got {self.jacktokenizer.current_token}")

    def compileSymbol(self, correct_token: str):
        """symbolをコンパイルする"""
        if (self.jacktokenizer.current_token == correct_token) & (self.jacktokenizer.tokenType() == "symbol"):
            if correct_token == "<":
                correct_token = "&lt;"
            elif correct_token == ">":
                correct_token = "&gt;"
            elif correct_token == "&":
                correct_token = "&amp;"
            elif correct_token == '"':
                correct_token = "&quot;"
            self._write_markup("symbol", correct_token, self.indent)
            if self.jacktokenizer.HasmoreTokens():
                self.jacktokenizer.advance()
        else:
            raise ValueError(f"expected {correct_token} but got {self.jacktokenizer.current_token}")

    def compileType(self, correct_token: list[str]):
        """typeをコンパイルする"""
        if self.jacktokenizer.current_token in correct_token:
            self.compileKeyword(correct_token)
        else:
            self.compileIdentifier(category="class", usage=False)
