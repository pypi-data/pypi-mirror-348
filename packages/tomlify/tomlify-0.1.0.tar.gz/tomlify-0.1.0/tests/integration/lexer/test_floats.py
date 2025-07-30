# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_floats_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# fractional', literal=' fractional', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt1', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='+1.0', literal=1.0, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt2', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='3.1415', literal=3.1415, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt3', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='-0.01', literal=-0.01, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# exponent', literal=' exponent', line=6)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt4', literal=None, line=7)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=7)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='5e+22', literal=5e+22, line=7)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt5', literal=None, line=8)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=8)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1e06', literal=1000000.0, line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt6', literal=None, line=9)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=9)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='-2E-2', literal=-0.02, line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=10)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# both', literal=' both', line=11)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=11)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt7', literal=None, line=12)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=12)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='6.626e-34', literal=6.626e-34, line=12)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=12)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=13)",

    ]

    test_path = Path(RESOURCE_PATH) / "floats" / "floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens


# TODO: Manage better error management in lexer

def test_invalid_floats_toml() -> None:

    test_path = Path(RESOURCE_PATH) / "floats" / "invalid_floats.toml"
    _, err, return_code = run_test(SCRIPT_PATH, test_path)

    err = err.splitlines()[0]

    assert return_code == 1
    assert err == "InvalidCharacterError: Invalid floating point input"


def test_special_floats_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# infinity', literal=' infinity', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='sf1', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='inf', literal=inf, line=2)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# positive infinity', literal=' positive infinity', line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='sf2', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='+inf', literal=inf, line=3)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# positive infinity', literal=' positive infinity', line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='sf3', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='-inf', literal=-inf, line=4)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# negative infinity', literal=' negative infinity', line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# not a number', literal=' not a number', line=6)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='sf4', literal=None, line=7)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=7)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='nan', literal=nan, line=7)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# actual sNaN/qNaN encoding is implementation-specific', literal=' actual sNaN/qNaN encoding is implementation-specific', line=7)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='sf5', literal=None, line=8)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=8)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='+nan', literal=nan, line=8)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# same as `nan`', literal=' same as `nan`', line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='sf6', literal=None, line=9)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=9)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='-nan', literal=nan, line=9)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# valid, actual encoding is implementation-specific', literal=' valid, actual encoding is implementation-specific', line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=10)",
]

    test_path = Path(RESOURCE_PATH) / "floats" / "special_floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_underscore_floats_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flt8', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='224_617.445_991_228', literal=224617.445991228, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=2)",
    ]

    test_path = Path(RESOURCE_PATH) / "floats" / "underscore_floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
