# ruff: noqa: S101

import pytest

from tomlify.lexer.exceptions import InvalidCharacterError
from tomlify.lexer.lex_token import Token
from tomlify.lexer.number_lexer import NumberLexer
from tomlify.lexer.token_type import TokenType


def test_number_int() -> None:
    input_num = "99"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 99, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_number_int_zero() -> None:
    input_num = "0"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 0, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_number_underscore() -> None:
    input_num = "1_000"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 1000, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_number_multiple_underscore() -> None:
    input_num = "1_2_3_4_5"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 12345, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_number_hex_uppercase() -> None:
    input_num = "0xDEADBEEF"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 3735928559, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_number_hex_lowercase() -> None:
    input_num = "0xdeadbeef"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 3735928559, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_number_hex_underscore() -> None:
    input_num = "0xdead_beef"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 3735928559, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_invalid_hex() -> None:
    input_num = "0xdeadmeat"
    lexer = NumberLexer(input_num)
    with pytest.raises(InvalidCharacterError):
        lexer.lex()

def test_number_octal() -> None:
    input_num = "0o377"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 255, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_invalid_octal() -> None:
    input_num = "0o408"
    lexer = NumberLexer(input_num)
    with pytest.raises(InvalidCharacterError):
        lexer.lex()

def test_number_binary() -> None:
    input_num = "0b10101010"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 170, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_invalid_binary() -> None:
    input_num = "0b102"
    lexer = NumberLexer(input_num)
    with pytest.raises(InvalidCharacterError):
        lexer.lex()

def test_number_float() -> None:
    input_num = "3.1415"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 3.1415, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def float_exponent() -> None:
    input_num = "5e+22"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 5e+22, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def float_negative_exponent() -> None:
    input_num = "1e-2"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 1e-2, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def float_positive_exponent() -> None:
    input_num = "1e+22"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 1e+2, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def float_positive_capital_e() -> None:
    input_num = "1E+22"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 1e+2, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def float_full_exponent() -> None:
    input_num = "6.626e-34"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 1e+2, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0

def test_invalid_floats_predecimal() -> None:
    input_num = ".7"
    lexer = NumberLexer(input_num)
    with pytest.raises(InvalidCharacterError):
        lexer.lex()

def test_invalid_floats_postdecimal() -> None:
    input_num = "7."
    lexer = NumberLexer(input_num)
    with pytest.raises(InvalidCharacterError):
        lexer.lex()

def test_invalid_floats_exponent() -> None:
    input_num = "3.e+20"
    lexer = NumberLexer(input_num)
    with pytest.raises(InvalidCharacterError):
        lexer.lex()

def test_float_underscore() -> None:
    input_num = "224_617.441_912"
    lexer = NumberLexer(input_num)
    n_chars, n_lines = lexer.lex()
    assert lexer.get_tokens() == [Token(TokenType.NUMBER, input_num, 224617.441912, 1)]
    assert n_chars == len(input_num)
    assert n_lines == 0
