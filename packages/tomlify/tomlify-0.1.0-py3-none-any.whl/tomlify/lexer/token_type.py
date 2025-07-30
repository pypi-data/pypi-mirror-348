from enum import Enum


class TokenType(Enum):

    # Single-character tokens
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SLASH = "SLASH"
    EQUAL = "EQUAL"
    COLON = "COLON"

    # Double character tokens
    DOUBLE_LEFT_BRACKET = "DOUBLE_LEFT_BRACKET"
    DOUBLE_RIGHT_BRACKET = "DOUBLE_RIGHT_BRACKET"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    COMMENT = "COMMENT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"

    # Control Characters
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"

    # Terminal Character
    EOF = "EOF"
