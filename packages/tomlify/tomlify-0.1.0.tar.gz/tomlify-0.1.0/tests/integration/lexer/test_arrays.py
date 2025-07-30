# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_arrays_toml() -> None:
    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='integers', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=1)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=1)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='3', literal=3, line=1)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='colors', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"red"', literal='red', line=2)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"yellow"', literal='yellow', line=2)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"green"', literal='green', line=2)""",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='nested_arrays_of_ints', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=3)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=3)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=3)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=3)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=3)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='3', literal=3, line=3)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='4', literal=4, line=3)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='5', literal=5, line=3)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=3)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='nested_mixed_array', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=4)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=4)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=4)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=4)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=4)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"a"', literal='a', line=4)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"b"', literal='b', line=4)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"c"', literal='c', line=4)""",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=4)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='string_array', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"all"', literal='all', line=5)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'strings'", literal='strings', line=5)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=5)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""are the same"""', literal='are the same', line=5)''',
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'''type'''", literal='type', line=5)""",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=6)",
    ]

    test_path = Path(RESOURCE_PATH) / "arrays" / "arrays.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_mixed_arrays_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# Mixed-type arrays are allowed', literal=' Mixed-type arrays are allowed', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='numbers', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0.1', literal=0.1, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0.2', literal=0.2, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0.5', literal=0.5, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='5', literal=5, line=2)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='contributors', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Foo Bar <foo@example.com>"', literal='Foo Bar <foo@example.com>', line=4)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.LEFT_BRACE: 'LEFT_BRACE'>, lexeme='{', literal=None, line=5)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Baz Qux"', literal='Baz Qux', line=5)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=5)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='email', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"bazqux@example.com"', literal='bazqux@example.com', line=5)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=5)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='url', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"https://example.com/bazqux"', literal='https://example.com/bazqux', line=5)""",
        "Token(type_=<TokenType.RIGHT_BRACE: 'RIGHT_BRACE'>, lexeme='}', literal=None, line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=6)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=7)",
    ]

    test_path = Path(RESOURCE_PATH) / "arrays" / "mixed_arrays.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_multiline_arrays_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='integers2', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='3', literal=3, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='integers3', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=6)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=6)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=7)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=7)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# this is ok', literal=' this is ok', line=7)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=9)",
    ]

    test_path = Path(RESOURCE_PATH) / "arrays" / "multiline_arrays.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
