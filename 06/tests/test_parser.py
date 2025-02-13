from collections import deque
from pathlib import Path

from src06.parser import Parser

BASE_DIR = Path(__file__).parents[1]


def test_HasMoreLines():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.lines = deque(["@2", "D=A", "@3", "D=D+A"])
    assert p.HasMoreLines() == True
    p.lines = []
    assert p.HasMoreLines() == False


def test_advance():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.lines = deque(["@2", "//D=A", "@3", "\n", "D=D+A"])
    p.advance()
    assert p.current_line == "@2"
    p.advance()
    assert p.current_line == "@3"
    p.advance()
    assert p.current_line == "D=D+A"


def test_InstructionType():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.current_line = "@2"
    assert p.InstructionType() == "A_INSTRUCTION"
    p.current_line = "(LOOP)"
    assert p.InstructionType() == "L_INSTRUCTION"
    p.current_line = "D=D+A"
    assert p.InstructionType() == "C_INSTRUCTION"
    p.current_line = "D;JGT"
    assert p.InstructionType() == "C_INSTRUCTION"
    p.current_line = "D"
    assert p.InstructionType() == "C_INSTRUCTION"


def test_symbol():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.current_line = "@2"
    assert p.symbol() == "2"
    p.current_line = "(LOOP)"
    assert p.symbol() == "LOOP"
    p.current_line = "D=D+A"
    assert p.symbol() == ""
    p.current_line = "D;JGT"
    assert p.symbol() == ""


def test_dest():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.current_line = "D=D+A"
    assert p.dest() == "D"
    p.current_line = "D;JGT"
    assert p.dest() == ""


def test_comp():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.current_line = "D=D+A"
    assert p.comp() == "D+A"
    p.current_line = "D;JGT"
    assert p.comp() == "D"


def test_jump():
    p = Parser(BASE_DIR / "asm/add/Add.asm")
    p.current_line = "D;JGT"
    assert p.jump() == "JGT"
    p.current_line = "D=D+A"
    assert p.jump() == ""
