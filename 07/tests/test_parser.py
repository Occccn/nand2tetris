from pathlib import Path

import pytest
from src07.parser import Parser

BASE_DIR = Path(__file__).parents[1]


@pytest.fixture
def parser():
    return Parser(BASE_DIR / "vm" / "SimpleAdd" / "SimpleAdd.vm")


def test_commandType(parser):
    parser.current_line = "push constant 7"
    assert parser.commandType() == "C_PUSH"
    parser.current_line = "pop constant 7"
    assert parser.commandType() == "C_POP"
    parser.current_line = "add"
    assert parser.commandType() == "C_ARITHMETIC"
    parser.current_line = "eq"
    assert parser.commandType() == "C_ARITHMETIC"
    parser.current_line = "gt"
    assert parser.commandType() == "C_ARITHMETIC"
    parser.current_line = "lt"
    assert parser.commandType() == "C_ARITHMETIC"
    parser.current_line = "and"
    assert parser.commandType() == "C_ARITHMETIC"
    parser.current_line = "or"
    assert parser.commandType() == "C_ARITHMETIC"
    parser.current_line = "not"
    assert parser.commandType() == "C_ARITHMETIC"
