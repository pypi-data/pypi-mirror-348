# ruff: noqa: N802

from tomlify.lexer.lex_token import Literal, Token
from tomlify.lexer.token_type import TokenType


def EQUAL_TOKEN(line: int) -> Token:
    return Token(TokenType.EQUAL, "=", None, line)

def NEWLINE_TOKEN(line: int) -> Token:
    return Token(TokenType.NEWLINE, "\n", None, line)

def EOF_TOKEN(line: int) -> Token:
    return Token(TokenType.EOF, "", None, line)

def STRING_TOKEN(value: str, literal: Literal, line: int) -> Token:
    return Token(TokenType.STRING, value, literal, line)

def IDENTIFIER_TOKEN(value: str, line: int) -> Token:
    return Token(TokenType.IDENTIFIER, value, None, line)

def COMMENT_TOKEN(value: str, literal: Literal, line: int) -> Token:
    return Token(TokenType.COMMENT, value, literal, line)

def DOT_TOKEN(line: int) -> Token:
    return Token(TokenType.DOT, ".", None, line)

def PLUS_TOKEN(line: int) -> Token:
    return Token(TokenType.PLUS, "+", None, line)

def MINUS_TOKEN(line: int) -> Token:
    return Token(TokenType.MINUS, "-", None, line)

def LEFT_BRACKET_TOKEN(line: int) -> Token:
    return Token(TokenType.LEFT_BRACKET, "[", None, line)

def RIGHT_BRACKET_TOKEN(line: int) -> Token:
    return Token(TokenType.RIGHT_BRACKET, "]", None, line)

def DOUBLE_LEFT_BRACKET_TOKEN(line: int) -> Token:
    return Token(TokenType.DOUBLE_LEFT_BRACKET, "[[", None, line)

def DOUBLE_RIGHT_BRACKET_TOKEN(line: int) -> Token:
    return Token(TokenType.DOUBLE_RIGHT_BRACKET, "]]", None, line)

def FLOAT_TOKEN(value: str, literal: Literal) -> Token:
    return Token(TokenType.NUMBER, value, literal, 1)
