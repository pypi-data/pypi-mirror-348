# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_key_value_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# INVALID', literal=' INVALID', line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='first', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Tom"', literal='Tom', line=5)""",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='last', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Preston-Werner"', literal='Preston-Werner', line=5)""",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# INVALID', literal=' INVALID', line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=6)",
    ]

    test_path = Path(RESOURCE_PATH) / "key_value.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
