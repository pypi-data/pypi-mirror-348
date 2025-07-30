
from tomlify.lexer.lex_token import Token
from tomlify.lexer.token_type import TokenType


def build_token(type_: TokenType, lexeme: str, literal: str | None = None) -> Token:
    return Token(type_, lexeme, literal, line=0)

TestToken = {
    "BARE_KEY": build_token(TokenType.IDENTIFIER, "bare_key"),
    "BARE_KEY_2": build_token(TokenType.IDENTIFIER, "bare_key_2"),
    "STRING_KEY": build_token(TokenType.STRING, '"value"', literal="value"),
    "STRING_KEY_2": build_token(TokenType.STRING,'"value 2"',literal="value 2"),
    "KEY_SEP": build_token(TokenType.DOT, "."),
    "EQUAL": build_token(TokenType.EQUAL, "="),
    "COMMA": build_token(TokenType.COMMA, ","),
    "ARRAY_START": build_token(TokenType.LEFT_BRACKET, "["),
    "ARRAY_END": build_token(TokenType.RIGHT_BRACKET, "]"),
    "NEWLINE": build_token(TokenType.NEWLINE, "\n"),
    "ARRAY_TABLE_START": build_token(TokenType.DOUBLE_LEFT_BRACKET, "[["),
    "ARRAY_TABLE_END": build_token(TokenType.DOUBLE_RIGHT_BRACKET, "]]"),
    "TABLE_START": build_token(TokenType.LEFT_BRACKET, "{"),
    "TABLE_END": build_token(TokenType.RIGHT_BRACKET, "}"),
    "INLINE_TABLE_START": build_token(TokenType.LEFT_BRACE, "{"),
    "INLINE_TABLE_END": build_token(TokenType.RIGHT_BRACE, "}"),
}
