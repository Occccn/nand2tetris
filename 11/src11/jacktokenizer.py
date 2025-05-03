from collections import deque

from src11.tokens import Token


class JackTokenizer:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines = self._skip_comment(f.readlines())
        self.TOKEN = Token()
        self.previous_token = None

    def _skip_comment(self, lines: list[str]) -> deque:
        """コメントをスキップする"""
        outputs = []
        comment_start = False
        for line in lines:
            if line.startswith("//") or line == "\n" or line == "":
                pass
            elif ("/*" in line or "/**" in line) and "*/" not in line:
                comment_start = True
            elif "*/" in line:
                comment_start = False
                lines.append(line.split("*/")[1])
            elif comment_start:
                pass
            elif "//" in line:
                outputs.append(line.split("//")[0])
            else:
                outputs.append(line)
        return deque(outputs)

    def next_token(self) -> str:
        """次のトークンを取得するだけで、現在のトークンは変更しない。また次のトークンは削除しない"""
        return self.tokens[0]

    def get_tokens(self) -> None:
        """tokkenのリストを作成する

        Returns:
            _type_: _description_
        """
        self.tokens = []
        for line in self.lines:
            line = line.strip()
            current_point = 0
            while current_point < len(line):
                if line[current_point] in self.TOKEN.symbols:
                    self.tokens.append(line[current_point])
                    current_point += 1
                elif line[current_point] == '"':
                    start_point = current_point
                    current_point += 1
                    while line[current_point] != '"':
                        current_point += 1
                    current_point += 1
                    self.tokens.append(line[start_point:current_point])
                elif line[current_point].isalpha() or line[current_point] == "_":
                    start_point = current_point
                    while line[current_point] != " " and line[current_point] not in self.TOKEN.symbols:
                        current_point += 1
                    self.tokens.append(line[start_point:current_point])
                elif line[current_point].isdigit():
                    start_point = current_point
                    while line[current_point].isdigit():
                        current_point += 1
                    self.tokens.append(f"{int(line[start_point:current_point])}")
                else:
                    current_point += 1

    def HasmoreTokens(self) -> bool:
        if len(self.tokens) == 0:
            return False
        else:
            return True

    def advance(self) -> None:
        if self.HasmoreTokens():
            if hasattr(self, "current_token") and self.current_token is not None:
                self.previous_token = self.current_token
            self.current_token = self.tokens.pop(0)

    def tokenType(self) -> str:
        if self.current_token in self.TOKEN.keywords:
            return "keyword"
        elif self.current_token in self.TOKEN.symbols:
            return "symbol"
        elif (
            self.current_token.startswith('"')
            and self.current_token.endswith('"')
            and '"' not in self.current_token[1:-1]
            and "\n" not in self.current_token[1:-1]
        ):
            return "string_const"
        elif self.current_token[0].isalpha() or self.current_token[0] == "_":
            return "identifier"
        else:
            return "int_const"

    def keyWord(self) -> str:
        if self.current_token == "class":
            return "CLASS"
        elif self.current_token == "constructor":
            return "CONSTRUCTOR"
        elif self.current_token == "function":
            return "FUNCTION"
        elif self.current_token == "method":
            return "METHOD"
        elif self.current_token == "field":
            return "FIELD"
        elif self.current_token == "static":
            return "STATIC"
        elif self.current_token == "var":
            return "VAR"
        elif self.current_token == "int":
            return "INT"
        elif self.current_token == "char":
            return "CHAR"
        elif self.current_token == "boolean":
            return "BOOLEAN"
        elif self.current_token == "void":
            return "VOID"
        elif self.current_token == "true":
            return "TRUE"
        elif self.current_token == "false":
            return "FALSE"
        elif self.current_token == "null":
            return "NULL"
        elif self.current_token == "this":
            return "THIS"
        elif self.current_token == "let":
            return "LET"
        elif self.current_token == "do":
            return "DO"
        elif self.current_token == "if":
            return "IF"
        elif self.current_token == "else":
            return "ELSE"
        elif self.current_token == "while":
            return "WHILE"
        elif self.current_token == "return":
            return "RETURN"
        raise ValueError(f"Invalid token: {self.current_token}")

    def symbol(self) -> str:
        return self.current_token

    def identifier(self) -> str:
        return "identifier"

    def intVal(self) -> int:
        return int(self.current_token)

    def stringVal(self) -> str:
        return self.current_token[1:-1]
