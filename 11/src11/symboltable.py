from typing import Literal


class SymbolTable:
    def __init__(self):
        self.symbol_table = {}

    def reset(self):
        pass

    def define(self, name: str, type: str, kind: Literal["STATIC", "FIELD", "ARG", "VAR"]):
        pass

    def varCount(self, kind: Literal["STATIC", "FIELD", "ARG", "VAR"]):
        pass

    def kindOf(self, name: str):
        pass

    def typeOf(self, name: str):
        pass

    def indexOf(self, name: str):
        pass
