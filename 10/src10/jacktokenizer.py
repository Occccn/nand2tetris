from collections import deque

from src10.token import Token


class JackAnalyzer:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines = deque(f.readlines())
            self.TOKEN = Token()

    def get_tokens(self):
        self.tokens = []
        for line in self.lines:
            line = line.strip()
            if line.startswith("//") or line == "\n" or line == "" or (line.startswith("/*") and line.endswith("*/")):
                continue
            else:
                line = line.strip()
        return self.tokens

    def HasmoreTokens(self):
        if len(self.tokens) == 0:
            return False
        else:
            return True

    def advance(self):
        pass

    def tokenType(self):
        if self.token in self.TOKEN.keywords:
            return "KEYWORD"
        elif self.token in self.TOKEN.symbols:
            return "SYMBOL"
        elif isinstance(self.token, int):
            return "INT_CONST"
        elif (
            self.token.startswith('"')
            and self.token.endswith('"')
            and '"' not in self.token[1:-1]
            and "\n" not in self.token[1:-1]
        ):
            return "STRING_CONST"
        elif self.token[0].isalpha() or self.token[0] == "_":
            return "IDENTIFIER"

    def keyWord(self):
        if self.token == "class":
            return "CLASS"
        elif self.token == "constructor":
            return "CONSTRUCTOR"
        elif self.token == "function":
            return "FUNCTION"
        elif self.token == "method":
            return "METHOD"
        elif self.token == "field":
            return "FIELD"
        elif self.token == "static":
            return "STATIC"
        elif self.token == "var":
            return "VAR"
        elif self.token == "int":
            return "INT"
        elif self.token == "char":
            return "CHAR"
        elif self.token == "boolean":
            return "BOOLEAN"
        elif self.token == "void":
            return "VOID"
        elif self.token == "true":
            return "TRUE"
        elif self.token == "false":
            return "FALSE"
        elif self.token == "null":
            return "NULL"
        elif self.token == "this":
            return "THIS"
        elif self.token == "let":
            return "LET"
        elif self.token == "do":
            return "DO"
        elif self.token == "if":
            return "IF"
        elif self.token == "else":
            return "ELSE"
        elif self.token == "while":
            return "WHILE"
        elif self.token == "return":
            return "RETURN"

    def symbol(self):
        pass

    def identifier(self):
        pass

    def intVal(self):
        pass

    def stringVal(self):
        pass
