import pytest
from src11.symboltable import SymbolTable


@pytest.fixture()
def symboltable():
    class MockSymbolTable(SymbolTable):
        def __init__(self):
            self.symbol_table = {}

    return MockSymbolTable


class TestReset:
    def test_normal_case(self, symboltable):
        symboltable.reset()

        assert symboltable.symbol_table == {}

    def test_empty_table(self, symboltable):
        symboltable.symbol_table = {}
        symboltable.reset()

        assert symboltable.symbol_table == {}


class Testdefine:
    def test_normal_case(self, symboltable):
        symboltable.define("x", "int", "STATIC")
        symboltable.define("y", "int", "FIELD")

        assert symboltable.symbol_table == {
            "x": {"type": "int", "kind": "STATIC", "index": 0},
            "y": {"type": "int", "kind": "FIELD", "index": 0},
        }

    def test_index_over1(self, symboltable):
        symboltable.define("x", "int", "STATIC")
        symboltable.define("y", "int", "FIELD")
        symboltable.define("xx", "int", "STATIC")
        symboltable.define("yy", "int", "FIELD")

        assert symboltable.symbol_table == {
            "x": {"type": "int", "kind": "STATIC", "index": 0},
            "y": {"type": "int", "kind": "FIELD", "index": 0},
            "xx": {"type": "int", "kind": "STATIC", "index": 1},
            "yy": {"type": "int", "kind": "FIELD", "index": 1},
        }


class TestvarCount:
    def test_normal_case(self, symboltable):
        symboltable.define("x", "int", "STATIC")
        symboltable.define("y", "int", "FIELD")
        symboltable.define("xx", "int", "ARG")
        symboltable.define("yy", "int", "VAR")
        symboltable.define("zz", "int", "VAR")
        assert symboltable.varCount("STATIC") == 1
        assert symboltable.varCount("FIELD") == 1
        assert symboltable.varCount("ARG") == 1
        assert symboltable.varCount("VAR") == 2

    def test_empty_case(self, symboltable):
        symboltable = SymbolTable()
        assert symboltable.varCount("STATIC") == 0
        assert symboltable.varCount("FIELD") == 0
        assert symboltable.varCount("ARG") == 0
        assert symboltable.varCount("VAR") == 0


class TestkindOf:
    def test_normal_case(self, symboltable):
        symboltable.define("x", "int", "STATIC")
        symboltable.define("y", "int", "FIELD")
        symboltable.define("xx", "int", "ARG")
        symboltable.define("yy", "int", "VAR")

        assert symboltable.kindOf("x") == "STATIC"
        assert symboltable.kindOf("y") == "FIELD"
        assert symboltable.kindOf("xx") == "ARG"
        assert symboltable.kindOf("yy") == "VAR"
        assert symboltable.kindOf("zz") is None


class TesttypeOf:
    def test_normal_case(self, symboltable):
        symboltable.define("x", "int", "STATIC")
        symboltable.define("y", "int", "FIELD")
        symboltable.define("xx", "int", "ARG")
        symboltable.define("yy", "int", "VAR")

        assert symboltable.typeOf("x") == "int"
        assert symboltable.typeOf("y") == "int"
        assert symboltable.typeOf("xx") == "int"
        assert symboltable.typeOf("yy") == "int"


class TestindexOf:
    def test_normal_case(self, symboltable):
        symboltable.define("x", "int", "STATIC")
        symboltable.define("y", "int", "FIELD")
        symboltable.define("xx", "int", "ARG")
        symboltable.define("yy", "int", "VAR")

        assert symboltable.indexOf("x") == 0
        assert symboltable.indexOf("y") == 0
        assert symboltable.indexOf("xx") == 0
        assert symboltable.indexOf("yy") == 0
