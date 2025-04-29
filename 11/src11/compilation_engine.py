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
        # 制御構造ごとに独立したカウンター
        self.label_counter = 0
        self.class_name = ""

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
        subroutine_type = self.jacktokenizer.current_token
        self.compileKeyword(["constructor", "function", "method"])
        self.compileType(["void", "int", "char", "boolean"])

        subroutine_name = self.jacktokenizer.current_token
        self.compileIdentifier(category="subroutine", usage=False)
        self.compileSymbol("(")
        self.compileParameterList(subroutine_type)
        self.compileSymbol(")")
        self.compileSubroutineBody(subroutine_type, subroutine_name)
        self.indent -= 1
        self._write_markup_no_token("subroutineDec", self.indent, closed=True)

    def compileParameterList(self, subroutine_type):
        """parameterListをコンパイルする"""
        self._write_markup_no_token("parameterList", self.indent, closed=False)
        self.indent += 1
        # メソッドの場合、this参照を暗黙の第0引数として追加
        if subroutine_type == "method":
            self.subroutine_table.define("this", self.class_name, "ARG")

        arg_counter = 0
        while self.jacktokenizer.current_token != ")":
            _keyword = self.jacktokenizer.current_token
            self.compileType(["int", "char", "boolean"])
            self.subroutine_table.define(self.jacktokenizer.current_token, _keyword, "ARG")
            index = self.subroutine_table.indexOf(self.jacktokenizer.current_token)
            self.compileIdentifier(category="ARG", usage=False, index=index)
            if self.jacktokenizer.current_token == ",":
                self.compileSymbol(",")
            arg_counter += 1
        self.indent -= 1
        self._write_markup_no_token("parameterList", self.indent, closed=True)

        return arg_counter

    def compileSubroutineBody(self, subroutine_type, subroutine_name):
        """subroutineBodyをコンパイルする"""
        self._write_markup_no_token("subroutineBody", self.indent, closed=False)
        self.indent += 1
        self.compileSymbol("{")
        var_counter = 0
        while self.jacktokenizer.current_token == "var":
            self.compileVarDec()
            var_counter += 1

        self.vm_writer.write_function(self.class_name + "." + self.jacktokenizer.current_token, var_counter)

        # サブルーチン種別に応じた特殊処理
        if subroutine_type == "method":
            # メソッド: thisポインタを設定（第0引数）
            self.vm_writer.write_push("ARGUMENT", 0)
            self.vm_writer.write_pop("POINTER", 0)
        elif subroutine_type == "constructor":
            # コンストラクタ: メモリ確保してthisポインタを設定
            field_count = self.class_table.varCount("FIELD")
            self.vm_writer.write_push("CONSTANT", field_count)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)

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

        # サブルーチン名を取得
        subroutine_name = self.jacktokenizer.current_token

        self.compileIdentifier(category="subroutine", usage=False)
        self.compileSubroutineCall(subroutine_name)

        self.vm_writer.write_pop("TEMP", 0)

        self.compileSymbol(";")
        self.indent -= 1
        self._write_markup_no_token("doStatement", self.indent, closed=True)

    def compileSubroutineCall(self, subroutine_name=None):
        """subroutineCallをコンパイルする"""
        nArgs = 0

        # メソッド呼び出しの場合 (例: point.distance())
        if self.jacktokenizer.current_token == ".":
            self.compileSymbol(".")
            method_name = self.jacktokenizer.current_token
            self.compileIdentifier(category="subroutine", usage=False)

            # オブジェクト名を取得してシンボルテーブルから探索
            obj_type = None
            if subroutine_name is not None:
                # サブルーチンテーブルで探索
                kind = self.subroutine_table.kindOf(subroutine_name)
                if kind is not None:
                    obj_type = self.subroutine_table.typeOf(subroutine_name)
                    index = self.subroutine_table.indexOf(subroutine_name)
                    segment = self._kind_to_segment(kind)
                    self.vm_writer.write_push(segment, index)
                    nArgs = 1  # thisポインタが第1引数
                else:
                    # クラステーブルで探索
                    kind = self.class_table.kindOf(subroutine_name)
                    if kind is not None:
                        obj_type = self.class_table.typeOf(subroutine_name)
                        index = self.class_table.indexOf(subroutine_name)
                        segment = self._kind_to_segment(kind)
                        self.vm_writer.write_push(segment, index)
                        nArgs = 1  # thisポインタが第1引数
            function_name = f"{obj_type}.{method_name}" if obj_type else f"{subroutine_name}.{method_name}"
        else:
            # クラス内メソッド呼び出し (例: this.doSomething())
            function_name = f"{self.class_name}.{subroutine_name}"
            # thisポインタをプッシュ
            self.vm_writer.write_push("POINTER", 0)
            nArgs = 1  # thisポインタが第1引数
        self.compileSymbol("(")
        nArgs += self.compileExpressionList()
        self.compileSymbol(")")
        self.vm_writer.write_call(function_name, nArgs)

    def compileLet(self):
        """letをコンパイルする"""
        self._write_markup_no_token("letStatement", self.indent, closed=False)
        self.indent += 1

        # 最初のトークンは "let" なので、これを処理
        self.compileKeyword("let")

        # 変数名の取得と情報の取得
        var_name = self.jacktokenizer.current_token

        # シンボルテーブルから変数情報を取得
        kind = self.subroutine_table.kindOf(var_name) or self.class_table.kindOf(var_name)
        index = self.subroutine_table.indexOf(var_name) or self.class_table.indexOf(var_name)
        segment = self._kind_to_segment(kind)

        # 識別子の処理（XML出力のみ）
        self.compileIdentifier(category=kind, usage=False, index=index)

        # 配列への代入かどうかを判断
        is_array = False
        if self.jacktokenizer.current_token == "[":
            is_array = True
            # 配列のベースアドレスをプッシュ
            self.vm_writer.write_push(segment, index)

            self.compileSymbol("[")
            self.compileExpression()  # インデックス値をスタックに積む
            self.compileSymbol("]")

            # ベースアドレス + インデックスを計算
            self.vm_writer.write_arithmetic("ADD")

        self.compileSymbol("=")
        self.compileExpression()  # 代入する値をスタックに積む
        self.compileSymbol(";")  # ここにセミコロンを追加

        # 代入処理（ここがポイント）
        if is_array:
            # スタックの状態: [... arr_elem_addr, value]

            # valueを一時的に保存
            self.vm_writer.write_pop("TEMP", 0)

            # arr_elem_addrをTHATポインタに設定
            self.vm_writer.write_pop("POINTER", 1)  # POINTER 1 は THAT ポインタを指す

            # valueを再度スタックに戻す
            self.vm_writer.write_push("TEMP", 0)

            # 値を THAT[0] に書き込む
            self.vm_writer.write_pop("THAT", 0)
        else:
            # 通常変数への代入の場合
            self.vm_writer.write_pop(segment, index)

        self.indent -= 1
        self._write_markup_no_token("letStatement", self.indent, closed=True)

    def compileWhile(self):
        """whileをコンパイルする"""
        label_start = f"WHILE_START_{self.label_counter}"
        label_end = f"WHILE_END_{self.label_counter}"
        self.label_counter += 1
        self._write_markup_no_token("whileStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("while")

        self.vm_writer.write_label(label_start)

        self.compileSymbol("(")
        self.compileExpression()
        self.compileSymbol(")")

        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(label_end)

        self.compileSymbol("{")
        self.compileStatements()
        self.compileSymbol("}")

        self.vm_writer.write_goto(label_start)
        self.vm_writer.write_label(label_end)

        self.indent -= 1
        self._write_markup_no_token("whileStatement", self.indent, closed=True)

    def compileReturn(self):
        """returnをコンパイルする"""
        self._write_markup_no_token("returnStatement", self.indent, closed=False)
        self.indent += 1
        self.compileKeyword("return")
        if self.jacktokenizer.current_token != ";":
            self.compileExpression()
        else:
            # 式がない場合は、0をスタックにプッシュ（void関数の場合）
            self.vm_writer.write_push("CONSTANT", 0)
        self.compileSymbol(";")

        # returnコマンドを発行
        self.vm_writer.write_return()

        self.indent -= 1
        self._write_markup_no_token("returnStatement", self.indent, closed=True)

    def compileIf(self):
        """ifをコンパイルする"""
        self._write_markup_no_token("ifStatement", self.indent, closed=False)
        self.indent += 1

        # ラベルの生成
        label_else = f"IF_ELSE_{self.label_counter}"
        label_end = f"IF_END_{self.label_counter}"
        self.label_counter += 1

        self.compileKeyword("if")
        self.compileSymbol("(")
        self.compileExpression()  # 条件式をスタックに積む
        self.compileSymbol(")")

        # 条件が偽ならelseまたは終了へジャンプ
        self.vm_writer.write_arithmetic("NOT")  # 条件を反転
        self.vm_writer.write_if(label_else)

        self.compileSymbol("{")
        self.compileStatements()  # if本体
        self.compileSymbol("}")

        # if文の処理が終わったら終了ラベルに飛ぶ
        self.vm_writer.write_goto(label_end)

        # else部分の開始ラベル
        self.vm_writer.write_label(label_else)

        if self.jacktokenizer.current_token == "else":
            self.compileKeyword("else")
            self.compileSymbol("{")
            self.compileStatements()
            self.compileSymbol("}")

        # 終了ラベル
        self.vm_writer.write_label(label_end)

        self.indent -= 1
        self._write_markup_no_token("ifStatement", self.indent, closed=True)

    def compileExpression(self):
        """expressionをコンパイルする"""
        self._write_markup_no_token("expression", self.indent, closed=False)
        self.indent += 1
        self.compileTerm()  # 最初の項をコンパイル（a）
        while self.jacktokenizer.current_token in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            # 演算子を保存
            op = self.jacktokenizer.current_token

            # 演算子をXMLに出力
            self.compileSymbol(op)

            # 次の項をコンパイル（b）
            self.compileTerm()

            # 演算子に対応するVM命令を生成
            if op == "+":
                self.vm_writer.write_arithmetic("ADD")
            elif op == "-":
                self.vm_writer.write_arithmetic("SUB")
            elif op == "*":
                self.vm_writer.write_call("Math.multiply", 2)
            elif op == "/":
                self.vm_writer.write_call("Math.divide", 2)
            elif op == "&":
                self.vm_writer.write_arithmetic("AND")
            elif op == "|":
                self.vm_writer.write_arithmetic("OR")
            elif op == "<":
                self.vm_writer.write_arithmetic("LT")
            elif op == ">":
                self.vm_writer.write_arithmetic("GT")
            elif op == "=":
                self.vm_writer.write_arithmetic("EQ")

        self.indent -= 1
        self._write_markup_no_token("expression", self.indent, closed=True)

    def compileTerm(self):
        """termをコンパイルする"""
        self._write_markup_no_token("term", self.indent, closed=False)
        self.indent += 1
        if self.jacktokenizer.tokenType() == "int_const":
            self.vm_writer.write_push("CONSTANT", int(self.jacktokenizer.current_token))
            self.jacktokenizer.advance()
        elif self.jacktokenizer.tokenType() == "string_const":
            string_content = self.jacktokenizer.current_token[1:-1]
            self.vm_writer.write_push("CONSTANT", len(string_content))
            self.vm_writer.write_call("String.new", 1)
            for char in string_content:
                self.vm_writer.write_char(char)
            self._write_markup("stringConstant", self.jacktokenizer.current_token[1:-1], self.indent)
            self.jacktokenizer.advance()
        elif self.jacktokenizer.tokenType() == "keyword":
            keyword = self.jacktokenizer.current_token
            if keyword == "true":
                self.vm_writer.write_push("CONSTANT", 0)
                self.vm_writer.write_arithmetic("NOT")  # 0を反転して-1（すべてのビットが1）にする
            elif keyword == "false":
                self.vm_writer.write_push("CONSTANT", 0)
            elif keyword == "null":
                self.vm_writer.write_push("CONSTANT", 0)
            elif keyword == "this":
                self.vm_writer.write_push("POINTER", 0)
            self.jacktokenizer.advance()

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
        nArgs = 0  # 引数の数をカウント
        while self.jacktokenizer.current_token != ")":
            self.compileExpression()
            nArgs += 1
            if self.jacktokenizer.current_token == ",":
                self.compileSymbol(",")
        self.indent -= 1
        self._write_markup_no_token("expressionList", self.indent, closed=True)

        return nArgs

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

        Args:
            category: 変数のカテゴリ（"class", "subroutine", "STATIC", "FIELD", "ARG", "VAR"など）
            usage: 値の使用（True）か宣言（False）か
            index: 既知の場合は変数のインデックス
        """
        if self.jacktokenizer.tokenType() == "identifier":
            var_name = self.jacktokenizer.current_token

            # 変数の場合（クラスやサブルーチン名ではない場合）
            if category not in ["class", "subroutine"]:
                # 変数が使用される場合（値を取得する場合）
                if usage:
                    # indexが指定されていない場合は、シンボルテーブルから取得
                    if index is None:
                        # まずサブルーチンのシンボルテーブルを確認
                        kind = self.subroutine_table.kindOf(var_name)
                        if kind is not None:
                            index = self.subroutine_table.indexOf(var_name)
                        else:
                            # サブルーチンテーブルになければクラステーブルを確認
                            kind = self.class_table.kindOf(var_name)
                            index = self.class_table.indexOf(var_name)
                            if kind is None:
                                raise ValueError(f"変数 {var_name} がシンボルテーブルに見つかりません")
                    else:
                        # indexが指定されている場合はcategoryを使用
                        kind = category

                    # 変数の種類からVMセグメントを取得してpushコマンドを生成
                    segment = self._kind_to_segment(kind)
                    self.vm_writer.write_push(segment, index)

            # # シンボルテーブル情報を含めたXML出力
            # kind_info = self.subroutine_table.kindOf(var_name) or self.class_table.kindOf(var_name) or category
            # index_info = (
            #     index
            #     if index is not None
            #     else (self.subroutine_table.indexOf(var_name) or self.class_table.indexOf(var_name))
            # )

            # self._write_markup(
            #     "identifier",
            #     f"{var_name} category:{kind_info} usage:{usage} index:{index_info}",
            #     self.indent,
            # )
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

    def _kind_to_segment(self, kind: str) -> str:
        """変数の種類をVMセグメントにマッピングする"""
        if kind == "STATIC":
            return "STATIC"
        elif kind == "FIELD":
            return "THIS"
        elif kind == "ARG":
            return "ARGUMENT"
        elif kind == "VAR":
            return "LOCAL"
        else:
            return "CONSTANT"  # デフォルト値
