import pytest
from src06.symboltable import SymbolTable


@pytest.fixture
def symbol_table():
    return SymbolTable()


def test_addEntry(symbol_table):
    symbol_table.addEntry("LOOP", 1)
    if not symbol_table.contains("LOOP"):
        raise AssertionError("LOOP not found in symbol_table")


def test_contains(symbol_table):
    symbol_table.table = {"LOOP": 1}
    if not symbol_table.contains("LOOP"):
        raise AssertionError("LOOP not found in symbol_table")


def test_getAddress(symbol_table):
    symbol_table.table = {"LOOP": 1}
    assert symbol_table.getAddress("LOOP") == 1
