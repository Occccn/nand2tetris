from typing import Literal


class SymbolTable:
    def __init__(self):
        self.symbol_table = {}
        self._counters = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}

    def reset(self):
        self.symbol_table = {}
        self._counters = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}

    def define(self, name: str, type: str, kind: Literal["STATIC", "FIELD", "ARG", "VAR"]):
        index = self._counters[kind]
        self.symbol_table[name] = {"type": type, "kind": kind, "index": index}
        self._counters[kind] += 1

    def varCount(self, kind: Literal["STATIC", "FIELD", "ARG", "VAR"]) -> int:
        return self._counters[kind]

    def kindOf(self, name: str) -> str | None:
        if name in self.symbol_table:
            return self.symbol_table[name]["kind"]
        return None

    def typeOf(self, name: str) -> str | None:
        if name in self.symbol_table:
            return self.symbol_table[name]["type"]
        return None

    def indexOf(self, name: str) -> int | None:
        if name in self.symbol_table:
            return self.symbol_table[name]["index"]
        return None
