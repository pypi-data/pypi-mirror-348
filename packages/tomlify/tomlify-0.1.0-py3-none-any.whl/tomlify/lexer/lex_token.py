from dataclasses import dataclass
from datetime import date, datetime, time

from tomlify.lexer.token_type import TokenType

Literal = str | int | float | bool | date | datetime | time

@dataclass
class Token:
    type_: TokenType
    lexeme: str
    literal: Literal | None
    line: int
