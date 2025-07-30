from tomlify.lexer.base_lexer import BaseLexer
from tomlify.lexer.token_type import TokenType


class IdentifierLexer(BaseLexer):
    def lex(self) -> tuple[int, int]:

        true_check = "".join([self._peek(i) for i in range(5)])
        false_check = "".join([self._peek(i) for i in range(6)])

        if true_check[0:4] == "true" and not self._isidentifier(self._peek(4)):
            self._advance(4)
            self._add_token(TokenType.BOOLEAN, literal = True)
            return (self._current, self._current_line - self._start_line)

        if false_check[0:5] == "false" and not self._isidentifier(self._peek(5)):
            self._advance(5)
            self._add_token(TokenType.BOOLEAN, literal = False)
            return (self._current, self._current_line - self._start_line)

        while True:
            if not self._isidentifier(self._peek()):
                break

            self._advance()
            continue

        self._add_token(TokenType.IDENTIFIER)
        return (self._current, self._current_line - self._start_line)

    @staticmethod
    def _isidentifier(c: str) -> bool:
        return c.isalnum() or c in {"_", "-"}
