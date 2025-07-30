from tomlify.lexer.base_lexer import BaseLexer
from tomlify.lexer.token_type import TokenType


class CommentLexer(BaseLexer):
    def lex(self) -> tuple[int, int]:
        # A comment goes until the end of the line.
        while (self._peek() != "\n") and not self._isAtEOF():
            self._advance()
        value = self._source[self._start + 1: self._current]
        self._add_token(TokenType.COMMENT, value)
        return (self._current, self._current_line - self._start_line)
