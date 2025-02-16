from collections import deque
from pathlib import Path

import pytest
from src06.parser import Parser

BASE_DIR = Path(__file__).parents[1]


@pytest.fixture
def parser():
    return Parser(BASE_DIR / "asm/Add.asm")


def test_HasMoreLines(parser):
    parser.lines = deque(["@2", "D=A", "@3", "D=D+A"])
    if not parser.HasMoreLines():
        raise AssertionError("HasMoreLines() should return True")
    parser.lines = deque([])
    if parser.HasMoreLines():
        raise AssertionError("HasMoreLines() should return False")


def test_advance(parser):
    parser.lines = deque(["@2", "//D=A", "@3", "\n", "D=D+A"])
    parser.advance()
    assert parser.current_line == "@2"
    parser.advance()
    assert parser.current_line == "@3"
    parser.advance()
    assert parser.current_line == "D=D+A"


def test_InstructionType(parser):
    parser.current_line = "@2"
    assert parser.InstructionType() == "A_INSTRUCTION"
    parser.current_line = "(LOOP)"
    assert parser.InstructionType() == "L_INSTRUCTION"
    parser.current_line = "D=D+A"
    assert parser.InstructionType() == "C_INSTRUCTION"
    parser.current_line = "D;JGT"
    assert parser.InstructionType() == "C_INSTRUCTION"
    parser.current_line = "D"
    assert parser.InstructionType() == "C_INSTRUCTION"


def test_symbol(parser):
    parser.current_line = "@2"
    assert parser.symbol() == "2"
    parser.current_line = "(LOOP)"
    assert parser.symbol() == "LOOP"
    parser.current_line = "D=D+A"
    assert parser.symbol() == ""
    parser.current_line = "D;JGT"
    assert parser.symbol() == ""


def test_dest(parser):
    parser.current_line = "D=D+A"
    assert parser.dest() == "D"
    parser.current_line = "D;JGT"
    assert parser.dest() == ""


def test_comp(parser):
    parser.current_line = "D=D+A"
    assert parser.comp() == "D+A"
    parser.current_line = "D;JGT"
    assert parser.comp() == "D"


def test_jump(parser):
    parser.current_line = "D;JGT"
    assert parser.jump() == "JGT"
    parser.current_line = "D=D+A"
    assert parser.jump() == ""
