# ruff: noqa: S101

from datetime import date, datetime, time, timedelta, timezone

from tomlify.lexer.date_lexer import DateLexer
from tomlify.lexer.lex_token import Token
from tomlify.lexer.token_type import TokenType


def test_offset_datetime() -> None:
    input_str = "1979-05-27T07:32:00Z"
    expected_time = datetime(1979,5,27,7,32,0, tzinfo=timezone.utc)
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_offset_datetime_timezone() -> None:
    input_str = "1979-05-27T07:32:00-07:00"
    tz_info = timezone(timedelta(hours=-7))
    expected_time = datetime(1979,5,27,7,32,0, tzinfo=tz_info)
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_offset_datetime_millisec() -> None:
    SECONDS_PER_HOUR = 3600  # noqa: N806
    input_str = "1979-05-27T07:32:00.999999-07:00"
    tz_info = timezone(timedelta(seconds=-7*SECONDS_PER_HOUR))
    expected_time = datetime(1979,5,27,7,32,0,microsecond=999999, tzinfo=tz_info)
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_offset_datetime_space() -> None:
    input_str = "1979-05-27 07:32:00Z"
    expected_time = datetime(1979,5,27,7,32,0, tzinfo=timezone.utc)
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_local_datetime() -> None:
    input_str = "1979-05-27T07:32:00"
    expected_time = datetime(1979,5,27,7,32,0)  # noqa: DTZ001
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_local_datetime_millisec() -> None:
    input_str = "1979-05-27T07:32:00.999999"
    expected_time = datetime(1979,5,27,7,32,0,microsecond=999999)  # noqa: DTZ001
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_local_date() -> None:
    input_str = "1979-05-27"
    expected_time = date(1979,5,27)
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0

def test_local_time() -> None:
    input_str = "00:32:00.999999"
    expected_time = time(0,32,0,microsecond=999999)
    lexer = DateLexer(input_str)
    n_chars, n_lines = lexer.lex()
    tokens = lexer.get_tokens()
    assert tokens == [
        Token(TokenType.DATE, input_str, expected_time, 1),
    ]
    assert n_chars == len(input_str)
    assert n_lines == 0
