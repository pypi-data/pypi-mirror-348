# ruff: noqa: DTZ007

import re
from datetime import datetime

from tomlify.lexer.base_lexer import BaseLexer, ParseInfo
from tomlify.lexer.exceptions import InvalidCharacterError
from tomlify.lexer.token_type import TokenType
from tomlify.utils.regex import RegexChecker

DATE_STR = r"([0-9]{4,})-([0-1][0-9])-([0-3][0-9])"
TIME_STR = r"([0-2][0-9]):([0-5][0-9]):([0-5][0-9])(\.)?([0-9]+)?"
SEPARATOR_STR = r"([Tt ])"
TZ_STR = r"([Z])?([+-])?([0-2][0-9])?:?([0-5][0-9])?"

DATETIME_STR = f"{DATE_STR}{SEPARATOR_STR}{TIME_STR}{TZ_STR}"

class DatePatterns:
    """Regex Patterns RFC 3339 compliant date time formats."""

    DATE_STR_PATTERN = re.compile(DATE_STR)
    TIME_STR_PATTERN = re.compile(TIME_STR)
    DATETIME_STR_PATTERN = re.compile(DATETIME_STR)

class DateLexer(BaseLexer):
    def lex(self) -> ParseInfo:

        match RegexChecker(self._source):
            case DatePatterns.DATETIME_STR_PATTERN as m:
                self._advance(len(m))
                t_sep = m.group(3)
                ms = m.group(7) + "%f" if m.group(7) else ""
                z = any([m.group(9), m.group(10), m.group(11), m.group(12)])
                dt_format = f"%Y-%m-%d{t_sep}%H:%M:%S{ms}{'%z' if z else ''}"
                literal = datetime.strptime(str(m), dt_format)
                self._add_token(TokenType.DATE, literal)
                return (self._current, self._current_line - self._start_line)
            case DatePatterns.DATE_STR_PATTERN as m:
                self._advance(len(m))
                literal = datetime.strptime(str(m), "%Y-%m-%d")
                date_literal = literal.date()
                self._add_token(TokenType.DATE, date_literal)
                return (self._current, self._current_line - self._start_line)
            case DatePatterns.TIME_STR_PATTERN as m:
                self._advance(len(m))
                ms = m.group(3) + "%f" if m.group(3) else ""
                literal = datetime.strptime(str(m), f"%H:%M:%S{ms}")
                time_literal = literal.time()
                self._add_token(TokenType.DATE, time_literal)
                return (self._current, self._current_line - self._start_line)
            case _:
                msg = "Invalid date formatting"
                raise InvalidCharacterError(msg)
