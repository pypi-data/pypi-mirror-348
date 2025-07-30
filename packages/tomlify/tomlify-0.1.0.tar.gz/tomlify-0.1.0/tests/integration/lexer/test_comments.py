# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_comments_toml() -> None:

    expected_tokens = [
    "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# This is a full-line comment', literal=' This is a full-line comment', line=1)",
    "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
    "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key', literal=None, line=2)",
    "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
    """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=2)""",
    "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# This is a comment at the end of a line', literal=' This is a comment at the end of a line', line=2)",
    "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
    "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='another', literal=None, line=3)",
    "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
    """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"# This is not a comment"', literal='# This is not a comment', line=3)""",
    "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
    "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=4)",
    ]

    test_path = Path(RESOURCE_PATH) / "comments" / "comments.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
