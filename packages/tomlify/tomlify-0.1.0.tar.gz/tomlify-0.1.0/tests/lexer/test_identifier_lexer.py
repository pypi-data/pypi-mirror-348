# ruff: noqa: S101

from tomlify.lexer.identifier_lexer import IdentifierLexer
from tomlify.lexer.lex_token import Token
from tomlify.lexer.token_type import TokenType


def test_identifier() -> None:
    input_string = "test"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_identifier_capital() -> None:
    input_string = "Test"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_identifier_number() -> None:
    input_string = "test1"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_identifier_underscore() -> None:
    input_string = "test_1"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_identifier_hyphen() -> None:
    input_string = "test-1"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_identifier_ended_period() -> None:
    input_string = "test"
    lexer = IdentifierLexer(input_string+".test2")
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_boolen_true() -> None:
    input_string = "true"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    expected_token = Token(TokenType.BOOLEAN, input_string, literal=True, line=1)
    assert lexer.get_tokens() == [expected_token]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_boolen_false() -> None:
    input_string = "false"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    expected_token = Token(TokenType.BOOLEAN, input_string, literal=False, line=1)
    assert lexer.get_tokens() == [expected_token]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_boolen_true_prefix() -> None:
    input_string = "true_identifier"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_boolen_false_prefix() -> None:
    input_string = "false_identifier"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_boolen_true_suffix() -> None:
    input_string = "identifier_true"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0

def test_boolen_false_suffix() -> None:
    input_string = "identifier_false"
    lexer = IdentifierLexer(input_string)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.IDENTIFIER, input_string, None, 1)]
    assert n_chars == len(input_string)
    assert n_lines == 0
