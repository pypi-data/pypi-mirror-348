from tomlify.lexer.base_lexer import BaseLexer
from tomlify.lexer.exceptions import UnterminatedStringError
from tomlify.lexer.token_type import TokenType


class StringLexer(BaseLexer):

    def lex(self, delimiter: str = '"') -> tuple[int, int]:
        self._advance()
        while True:

            # Check we haven't gotten to the end of the file or line
            if self._isAtEOF() or self._isAtEOL():
                msg = "Unterminated string."
                raise UnterminatedStringError(msg)

            # Check for escaped character
            if self._peek() == "\\" and delimiter == '"':
                self._advance(2)
                continue

            if self._peek() == delimiter:
                break

            self._advance()

        self._advance()
        value = self._source[self._start+1: self._current-1]
        self._add_token(TokenType.STRING, value)
        return (self._current, self._current_line - self._start_line)


class MultilineStringLexer(BaseLexer):

    def lex(self, delimiter: str = '"') -> tuple[int, int]:

        self._advance(3)
        while True:

            # Check we haven't gotten to the end of the file or line
            if self._isAtEOF():
                msg = "Unterminated string."
                raise UnterminatedStringError(msg)

            # Check for escaped character
            if self._peek() == "\\" and delimiter == '"':
                self._advance(2)
                continue

            next_three = self._peek() + self._peek(1) + self._peek(2)
            if next_three == delimiter * 3:
                break

            if self._peek() == "\n":
                self._current_line += 1

            self._advance()

        self._advance(3)
        value = self._source[self._start + 3: self._current - 3]
        self._add_token(TokenType.STRING, value)
        return (self._current, self._current_line - self._start_line)

