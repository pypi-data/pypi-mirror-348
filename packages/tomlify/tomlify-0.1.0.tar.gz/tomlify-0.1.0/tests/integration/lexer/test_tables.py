# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_tables_toml() -> None:
    expected_tokens = [
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='table', literal=None, line=1)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='table-1', literal=None, line=3)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key1', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"some string"', literal='some string', line=4)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key2', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='123', literal=123, line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.LEFT_BRACKET: 'LEFT_BRACKET'>, lexeme='[', literal=None, line=7)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='table-2', literal=None, line=7)",
        "Token(type_=<TokenType.RIGHT_BRACKET: 'RIGHT_BRACKET'>, lexeme=']', literal=None, line=7)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key1', literal=None, line=8)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=8)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"another string"', literal='another string', line=8)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key2', literal=None, line=9)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=9)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='456', literal=456, line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=10)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_inline_tables_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        "Token(type_=<TokenType.LEFT_BRACE: 'LEFT_BRACE'>, lexeme='{', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='first', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Tom"', literal='Tom', line=1)""",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='last', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Preston-Werner"', literal='Preston-Werner', line=1)""",
        "Token(type_=<TokenType.RIGHT_BRACE: 'RIGHT_BRACE'>, lexeme='}', literal=None, line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='point', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.LEFT_BRACE: 'LEFT_BRACE'>, lexeme='{', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='x', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1', literal=1, line=2)",
        "Token(type_=<TokenType.COMMA: 'COMMA'>, lexeme=',', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='y', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='2', literal=2, line=2)",
        "Token(type_=<TokenType.RIGHT_BRACE: 'RIGHT_BRACE'>, lexeme='}', literal=None, line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='animal', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        "Token(type_=<TokenType.LEFT_BRACE: 'LEFT_BRACE'>, lexeme='{', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='type', literal=None, line=3)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"pug"', literal='pug', line=3)""",
        "Token(type_=<TokenType.RIGHT_BRACE: 'RIGHT_BRACE'>, lexeme='}', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=4)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "inline_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
