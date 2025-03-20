from collections import deque

from src10.token import Token


class JackTokenizer:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines = deque(f.readlines())
            self.TOKEN = Token()

    def get_tokens(self):
        """tokkenのリストを作成する

        Returns:
            _type_: _description_
        """
        self.tokens = []
        for line in self.lines:
            line = line.strip()
            if line.startswith("//") or line == "\n" or line == "" or (line.startswith("/*") and line.endswith("*/")):
                continue
            else:
                line = line.strip()
                current_point = 0
                while current_point < len(line):
                    if line[current_point] in self.TOKEN.symbols:
                        self.tokens.append(line[current_point])
                        current_point += 1
                    elif line[current_point] == '"':
                        current_point += 1
                        start_point = current_point
                        while line[current_point] != '"':
                            current_point += 1
                        self.tokens.append(line[start_point : current_point - 1])
                        current_point += 1
                    elif line[current_point].isalpha() or line[current_point] == "_":
                        start_point = current_point
                        while line[current_point] != " " and line[current_point] not in self.TOKEN.symbols:
                            current_point += 1
                        self.tokens.append(line[start_point:current_point])
                    elif line[current_point].isdigit():
                        start_point = current_point
                        while line[current_point].isdigit():
                            current_point += 1
                        self.tokens.append(int(line[start_point:current_point]))
                    else:
                        current_point += 1
        return self.tokens

    def HasmoreTokens(self):
        if len(self.tokens) == 0:
            return False
        else:
            return True

    def advance(self):
        self.current_token = self.tokens.pop(0)

    def tokenType(self):
        if self.current_token in self.TOKEN.keywords:
            return "KEYWORD"
        elif self.current_token in self.TOKEN.symbols:
            return "SYMBOL"
        elif isinstance(self.token, int):
            return "INT_CONST"
        elif (
            self.current_token.startswith('"')
            and self.current_token.endswith('"')
            and '"' not in self.current_token[1:-1]
            and "\n" not in self.current_token[1:-1]
        ):
            return "STRING_CONST"
        elif self.current_token[0].isalpha() or self.current_token[0] == "_":
            return "IDENTIFIER"

    def keyWord(self):
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

    def symbol(self) -> str:
        return self.current_token

    def identifier(self):
        return "identifier"

    def intVal(self) -> int:
        return self.current_token

    def stringVal(self) -> str:
        return self.current_token
