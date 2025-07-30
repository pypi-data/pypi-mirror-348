# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_base_integers_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# hexadecimal with prefix `0x`', literal=' hexadecimal with prefix `0x`', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='hex1', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0xDEADBEEF', literal=3735928559, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='hex2', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0xdeadbeef', literal=3735928559, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='hex3', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0xdead_beef', literal=3735928559, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# octal with prefix `0o`', literal=' octal with prefix `0o`', line=6)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='oct1', literal=None, line=7)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=7)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0o01234567', literal=342391, line=7)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='oct2', literal=None, line=8)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=8)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0o755', literal=493, line=8)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# useful for Unix file permissions', literal=' useful for Unix file permissions', line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# binary with prefix `0b`', literal=' binary with prefix `0b`', line=10)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=10)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='bin1', literal=None, line=11)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=11)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0b11010110', literal=214, line=11)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=11)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=12)",

    ]

    test_path = Path(RESOURCE_PATH) / "integers" / "base_integers.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens


def test_integers_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int1', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='+99', literal=99, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int2', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='42', literal=42, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int3', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='0', literal=0, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int4', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='-17', literal=-17, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=5)",
    ]

    test_path = Path(RESOURCE_PATH) / "integers" / "integers.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens


def test_base_underscore_integers_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int5', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1_000', literal=1000, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int6', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='5_349_221', literal=5349221, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int7', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='53_49_221', literal=5349221, line=3)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# Indian number system grouping', literal=' Indian number system grouping', line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='int8', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1_2_3_4_5', literal=12345, line=4)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# VALID but discouraged', literal=' VALID but discouraged', line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=5)",
    ]

    test_path = Path(RESOURCE_PATH) / "integers" / "underscore_integers.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
