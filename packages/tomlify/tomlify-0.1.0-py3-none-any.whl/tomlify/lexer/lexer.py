from __future__ import annotations

from tomlify.lexer.base_lexer import BaseLexer
from tomlify.lexer.comment_lexer import CommentLexer
from tomlify.lexer.exceptions import InvalidCharacterError
from tomlify.lexer.identifier_lexer import IdentifierLexer
from tomlify.lexer.lex_token import Token
from tomlify.lexer.number_lexer import NumberLexer
from tomlify.lexer.string_lexer import MultilineStringLexer, StringLexer
from tomlify.lexer.token_type import TokenType

TOKEN_TYPE_MAP = {
    ".": TokenType.DOT,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    "[": TokenType.LEFT_BRACKET,
    "]": TokenType.RIGHT_BRACKET,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    "=": TokenType.EQUAL,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    "/": TokenType.SLASH,
    "[[": TokenType.DOUBLE_LEFT_BRACKET,
    "]]": TokenType.DOUBLE_RIGHT_BRACKET,
}

class Lexer(BaseLexer):

    def lex(self) -> tuple[int, int]:
        """Tokenizes the source text for relevent TOML lexemes.

        This method starts at the beginning of the next lexeme and
        continues until the end of the file is reached. Once all
        tokens have been scanned, an EOF token is appended to the
        tokens list.

        Returns:
            list[Token]: The list of tokens found in the source text.

        """
        while not self._isAtEOF():
            # We are at the beginning of the next lexeme.
            self._start = self._current
            self._lextoken()

        self._tokens.append(Token(TokenType.EOF, "", None, self._current_line))
        return self._current, self._current_line - self._start_line

    def _lextoken(self) -> None:  # noqa: C901,PLR0912
        c = self._peek()
        match c:
            case "#":
                self.call_sublexer(CommentLexer)
            case '"' | "'":
                if self._peek(1) == c and self._peek(2) == c:
                    self.call_sublexer(MultilineStringLexer, delimiter=c)
                else:
                    self.call_sublexer(StringLexer, delimiter=c)
            case "-"|"+":
                self.call_sublexer(NumberLexer)
            case "."|"{"|"}"|":"|"="|",":
                self._advance()
                token = TOKEN_TYPE_MAP[c]
                self._add_token(token, line=self._current_line)
            case "[" | "]":
                if self._peek(1) == c:
                    self._advance(2)
                    token = TOKEN_TYPE_MAP[2*c]
                    self._add_token(token, line=self._current_line)
                else:
                    self._advance()
                    token = TOKEN_TYPE_MAP[c]
                    self._add_token(token, line=self._current_line)
            case " ":
                self._advance()
            case "\n"|"\r":
                self._advance()
                self._add_token(TokenType.NEWLINE, line=self._current_line)
                self._current_line += 1
            case _:
                if c == "i" and self._peek(1) == "n" and self._peek(2) == "f":
                    self._advance(3)
                    line = self._current_line
                    self._add_token(TokenType.NUMBER, literal = float("inf"), line=line)
                elif c == "n" and self._peek(1) == "a" and self._peek(2) == "n":
                    self._advance(3)
                    line = self._current_line
                    self._add_token(TokenType.NUMBER, literal = float("nan"), line=line)
                elif c.isdigit():
                    self.call_sublexer(NumberLexer)
                elif c.isalpha():
                    self.call_sublexer(IdentifierLexer)
                else:
                    msg = f"Unexpected character '{c!r}' on line {self._current_line}"
                    raise InvalidCharacterError(msg)

# TODO: add support for line starting indent
# TODO: refactor symbols to use a sublexer to reduce complexity
