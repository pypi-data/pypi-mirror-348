# ruff: noqa: S101, FBT003

from tomlify.lexer.lex_token import Token
from tomlify.lexer.token_type import TokenType
from tomlify.parser.expr import (
    Array,
    ArrayTable,
    Comment,
    InlineTable,
    Key,
    KeyValue,
    Value,
)


def test_comment() -> None:
    token = Token(TokenType.COMMENT, "# This is a comment", "This is a comment", 1)
    comment = Comment(token)
    assert comment.token == token

def test_value_boolean() -> None:
    token = Token(TokenType.BOOLEAN, "true", True, 1)
    boolean = Value(token)
    assert boolean.token == token
    assert boolean.contents
    assert boolean.__repr__() == "Value(True)"

def test_value_string() -> None:
    token = Token(TokenType.STRING, '"This is a string"', "This is a string", 1)
    string = Value(token)
    assert string.token == token
    assert string.contents == '"This is a string"'
    assert string.__repr__() == 'Value("This is a string")'

def test_value_integer() -> None:
    token = Token(TokenType.NUMBER, "1234", 1234, 1)
    number = Value(token)
    assert number.token == token
    assert number.contents == "1234"
    assert number.__repr__() == "Value(1234)"

def test_value_float() -> None:
    token = Token(TokenType.NUMBER, "12.34", 12.34, 1)
    number = Value(token)
    assert number.token == token
    assert number.contents == "12.34"
    assert number.__repr__() == "Value(12.34)"

def test_value_date() -> None:
    token = Token(TokenType.DATE, "2022-01-01", "2022-01-01", 1)
    date = Value(token)
    assert date.token == token
    assert date.contents == "2022-01-01"
    assert date.__repr__() == "Value(2022-01-01)"

def test_key() -> None:
    token = Token(TokenType.IDENTIFIER, "key", "key", 1)
    key = Key(token)
    assert key.tokens[0] == token
    assert key.name == "key"
    assert key.__repr__() == "Key(key)"

def test_dotted_key() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    key = Key(token1)
    key += Key(token2)
    assert key.tokens == [token1, token2]
    assert key.name == "key1.key2"
    assert key.__repr__() == "Key(key1.key2)"

def test_key_val() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    key = Key(token1)
    value = Value(token2)
    key_val = KeyValue(key, value)
    assert key_val.key.tokens == [token1]
    assert key_val.key.name == "key1"
    assert key_val.value.token == token2
    assert key_val.value.contents == "key2"
    assert key_val.__repr__() == "KeyValue(key1 = key2)"

def test_simple_array() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    array = Array(Value(token1), Value(token2))

    assert array.contents == "key1, key2"
    assert array.__repr__() == "Array(key1, key2)"
    for value, token in zip(array, [token1, token2], strict=False):
        assert value.token == token

def test_simple_array_append() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    token3 = Token(TokenType.IDENTIFIER, "key3", "key3", 1)
    array = Array(Value(token1), Value(token2))
    array.append(Value(token3))

    assert array.contents == "key1, key2, key3"
    assert array.__repr__() == "Array(key1, key2, key3)"
    for value, token in zip(array, [token1, token2, token3], strict=False):
        assert value.token == token

def test_nested_array_first() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    token3 = Token(TokenType.IDENTIFIER, "key3", "key3", 1)

    inner_array = Array(Value(token1), Value(token2))
    array = Array(inner_array)
    array.append(Value(token3))

    assert array.contents == "[ key1, key2 ], key3"
    assert array.__repr__() == "Array([ key1, key2 ], key3)"

def test_nested_array_last() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    token3 = Token(TokenType.IDENTIFIER, "key3", "key3", 1)

    array = Array(Value(token1))
    inner_array = Array(Value(token2), Value(token3))
    array.append(inner_array)

    assert array.contents == "key1, [ key2, key3 ]"
    assert array.__repr__() == "Array(key1, [ key2, key3 ])"

def test_nested_array_middle() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    token2 = Token(TokenType.IDENTIFIER, "key2", "key2", 1)
    token3 = Token(TokenType.IDENTIFIER, "key3", "key3", 1)
    token4 = Token(TokenType.IDENTIFIER, "key4", "key4", 1)

    inner_array = Array(Value(token2), Value(token3))
    array = Array(Value(token1))
    array.append(inner_array)
    array.append(Value(token4))

    assert array.contents == "key1, [ key2, key3 ], key4"
    assert array.__repr__() == "Array(key1, [ key2, key3 ], key4)"

def test_inline_table() -> None:

    token1 = Token(TokenType.STRING, "key1", "key1", 1)
    token2 = Token(TokenType.STRING, "key2", "key2", 1)
    token3 = Token(TokenType.STRING, "key3", "key3", 1)
    token4 = Token(TokenType.STRING, "key4", "key4", 1)


    table = InlineTable(
        KeyValue(Key(token1), Value(token2)),
        KeyValue(Key(token3), Value(token4)),
    )

    assert table.__repr__() == "InlineTable(key1 = key2, key3 = key4)"

def test_array_table() -> None:
    token1 = Token(TokenType.IDENTIFIER, "key1", "key1", 1)
    table = ArrayTable(Key(token1))
    assert table.__repr__() == "ArrayTable(key1)"

