# ruff: noqa: PLR0912

import re
from typing import TYPE_CHECKING

from tomlify.lexer.base_lexer import BaseLexer
from tomlify.lexer.date_lexer import DateLexer
from tomlify.lexer.exceptions import InvalidCharacterError
from tomlify.lexer.token_type import TokenType

if TYPE_CHECKING:
    from tomlify.lexer.lex_token import Literal


class BinaryLexer(BaseLexer):

    def lex(self) -> tuple[int, int]:
        self._advance(2)

        while True:
            c = self._peek()

            if self._isAtEOF() or self._peek().isspace():
                break

            if c in "01_":
                self._advance()
                continue
            msg = f"Invalid character '{c}' in binary literal."
            raise InvalidCharacterError(msg)

        literal = int(self._source[self._start:self._current], 2)
        self._add_token(TokenType.NUMBER, literal)
        return (self._current, self._current_line - self._start_line)


class OctalLexer(BaseLexer):
    def lex(self) -> tuple[int, int]:
        self._advance(2)

        while True:
            c = self._peek()

            if self._isAtEOF() or self._peek().isspace():
                break

            if c in "01234567_":
                self._advance()
                continue
            msg = f"Invalid character '{c}' in octal literal."
            raise InvalidCharacterError(msg)

        literal = int(self._source[self._start:self._current], 8)
        self._add_token(TokenType.NUMBER, literal)
        return (self._current, self._current_line - self._start_line)

class HexLexer(BaseLexer):
    def lex(self) -> tuple[int, int]:
        self._advance(2)

        while True:
            c = self._peek()

            if self._isAtEOF() or self._peek().isspace():
                break

            if c in "abcdefABCDEF0123456789_":
                self._advance()
                continue
            msg = f"Invalid character '{c}' in hexadecimal literal."
            raise InvalidCharacterError(msg)

        literal = int(self._source[self._start:self._current], 16)
        self._add_token(TokenType.NUMBER, literal)
        return (self._current, self._current_line - self._start_line)


class DecimalLexer(BaseLexer):
    def lex(self) -> tuple[int, int]:  # noqa: C901

        #TODO: Refactor to reduce line length
        if re.findall(r"[0-9]{4,}-[0-9]{2}-[0-9]{2}", self._source) or re.findall(r"[0-9]{2}:[0-9]{2}:[0-9]{2}", self._source):  # noqa: E501
            return self.call_sublexer(DateLexer)

        is_integer = True
        is_start = -1

        while True:
            is_start += 1

            c = self._peek()

            if self._isAtEOF() or self._peek().isspace() or self._peek() == ",":
                break

            if c in {",", "]"}:
                break

            if c == ".":
                is_integer = False
                if not (self._has_leading_digit() and self._has_trailing_digit()):
                    msg = "Invalid floating point input"
                    raise InvalidCharacterError(msg)
                self._advance()
                continue

            if c == "i" and self._peek(1) == "n" and self._peek(2) == "f":
                is_integer = False
                self._advance(3)
                continue

            if c == "n" and self._peek(1) == "a" and self._peek(2) == "n":
                is_integer = False
                self._advance(3)
                continue

            if c in "0123456789_":
                self._advance()
                continue

            if c.lower() == "e":
                is_integer = False
                self._advance()
                continue

            if c in "+-":
                if not is_start:
                    self._advance()
                    continue
                if is_integer:
                    break
                self._advance()
                continue

            msg = f"Invalid character '{c}' in decimal literal."
            raise InvalidCharacterError(msg)

        number_literal = self._source[self._start:self._current]
        literal: Literal = int(number_literal) if is_integer else float(number_literal)
        self._add_token(TokenType.NUMBER, literal)
        return (self._current, self._current_line - self._start_line)

    def _has_leading_digit(self) -> bool:
        return self._peek(1).isdigit()

    def _has_trailing_digit(self) -> bool:
        return self._peek(-1).isdigit()

class NumberLexer(BaseLexer):
    def lex(self) -> tuple[int, int]:

        prefix = self._peek() + self._peek(1)

        match prefix:
            case "0x":
                return self.call_sublexer(HexLexer)
            case "0o":
                return self.call_sublexer(OctalLexer)
            case "0b":
                return self.call_sublexer(BinaryLexer)
            case _:
               return self.call_sublexer(DecimalLexer)

# TODO: Implement time and date types as tokens
