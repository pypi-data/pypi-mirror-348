from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from tomlify.lexer.exceptions import LexerEOFError
from tomlify.lexer.lex_token import Token

if TYPE_CHECKING:
    from tomlify.lexer.lex_token import Literal
    from tomlify.lexer.token_type import TokenType

ParseInfo = tuple[int, int]

class BaseLexer(ABC):

    def __init__(self, source: str, start_line: int = 1) -> None:
        self._source: str = source
        self._tokens: list[Token] = []
        self._start: int = 0
        self._current: int = 0
        self._start_line: int = start_line
        self._current_line: int = start_line


    def call_sublexer(self, s_lexer: type[BaseLexer], delimiter: str = "") -> ParseInfo:
        lexer = s_lexer(self._source[self._current:], self._current_line)

        if delimiter != "":
            n_chars, n_lines = lexer.lex(delimiter)  # type: ignore[call-arg]
        else:
            n_chars, n_lines = lexer.lex()

        self._current += n_chars
        self._tokens.extend(lexer.get_tokens())
        self._current_line += n_lines

        return (n_chars, self._current_line - self._start_line)

    @abstractmethod
    def lex(self) -> ParseInfo:
        pass

    def get_tokens(self) -> list[Token]:
        return self._tokens

    def _match(self, expected: str) -> bool:
        if self._isAtEOF():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def _isAtEOF(self, num: int = 0) -> bool: # noqa: N802
        return self._current + num >= len(self._source)

    def _isAtEOL(self, num: int = 0) -> bool: # noqa: N802
        return self._source[self._current + num] == "\n"

    def _advance(self, num: int = 1) -> None:
        if self._isAtEOF():
            msg = "Attempting to advance past end of file."
            raise LexerEOFError(msg)
        self._current += num

    def _peek(self, num: int = 0) -> str:
        if  self._current + num < 0:
            return "\0"
        if self._isAtEOF() or self._current + num >= len(self._source):
            return "\0"
        return self._source[self._current + num]

    def _add_token(
            self,
            type_: TokenType,
            literal: Literal | None = None,
            line: int | None = None,
        ) -> None:
        if line is None:
            line = self._start_line
        text = self._source[self._start:self._current]
        self._tokens.append(Token(type_, text, literal, line))

# TODO: Add distinct string lexers for the literal string types
# TODO: Allow peek to return list of characters
