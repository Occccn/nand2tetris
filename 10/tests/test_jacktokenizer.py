from collections import deque

import pytest
from src10.jacktokenizer import JackTokenizer
from src10.tokens import Token

correct_tokens = [
    "class",
    "Main",
    "{",
    "function",
    "void",
    "main",
    "(",
    ")",
    "{",
    "var",
    "int",
    "x",
    ";",
    "let",
    "x",
    "=",
    "1",
    ";",
    "let",
    "x",
    "=",
    '"a"',
    ";",
    "do",
    "Output",
    ".",
    "printInt",
    "(",
    "x",
    ")",
    ";",
    "return",
    ";",
    "}",
    "}",
]

# create a list of correct token types
correct_tokenTypes = [
    "keyword",
    "identifier",
    "symbol",
    "keyword",
    "keyword",
    "identifier",
    "symbol",
    "symbol",
    "symbol",
    "keyword",
    "keyword",
    "identifier",
    "symbol",
    "keyword",
    "identifier",
    "symbol",
    "int_const",
    "symbol",
    "keyword",
    "identifier",
    "symbol",
    "string_const",
    "symbol",
    "keyword",
    "identifier",
    "symbol",
    "identifier",
    "symbol",
    "identifier",
    "symbol",
    "symbol",
    "keyword",
    "symbol",
    "symbol",
    "symbol",
]


@pytest.fixture
def jacktokenizer():
    class MockJackTokenizer(JackTokenizer):
        def __init__(self, path: str):
            self.lines = [
                "class Main {",
                "// test",
                "/* test */",
                "/** test",
                "* test",
                "dddd",
                "*/",
                "    function void main() { // test",
                "        var int x;",
                "        let x = 1;",
                '        let x = "a";',
                "        do Output.printInt(x);",
                "        return;",
                "    }",
                "}",
            ]
            self.TOKEN = Token()

    return MockJackTokenizer("")


def test_skip_comments(jacktokenizer):
    lines = [
        "class Main {",
        "// test",
        "/* test */",
        "/** test",
        "* test",
        "dddd",
        "*/",
        "    function void main() { // test",
        "        var int x;",
        "        let x = 1;",
        '        let x = "a";',
        "        do Output.printInt(x);",
        "        return;",
        "    }",
        "}",
    ]
    lines = jacktokenizer._skip_comment(lines)
    assert lines == deque(
        [
            "class Main {",
            "    function void main() { ",
            "        var int x;",
            "        let x = 1;",
            '        let x = "a";',
            "        do Output.printInt(x);",
            "        return;",
            "    }",
            "}",
        ]
    )


def test_get_tokens(jacktokenizer):
    lines = [
        "class Main {",
        "// test",
        "/* test */",
        "/** test",
        "/** test */",
        "* test",
        "dddd",
        "*/",
        "    function void main() { // test",
        "        var int x;",
        "        let x = 1;",
        '        let x = "a";',
        "        do Output.printInt(x);",
        "        return;",
        "    }",
        "}",
    ]
    jacktokenizer.lines = jacktokenizer._skip_comment(lines)
    jacktokenizer.get_tokens()
    assert jacktokenizer.tokens == correct_tokens


def test_tokenType(jacktokenizer):
    tokens = []
    print(len(correct_tokens))
    jacktokenizer.tokens = correct_tokens
    length = len(jacktokenizer.tokens)
    for _ in range(length):
        jacktokenizer.advance()
        tokens.append(jacktokenizer.tokenType())
    print(len(correct_tokenTypes))
    print(len(correct_tokens))
    assert tokens == correct_tokenTypes
