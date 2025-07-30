# ruff: noqa: S101, SLF001, N802

from tests.parser.test_token import TestToken
from tomlify.parser.expr import (
    Array,
    ArrayTable,
    InlineTable,
    Key,
    KeyValue,
    Table,
    Value,
)
from tomlify.parser.parser import Parser


def test_unquoted_key_unquoted() -> None:
    input_tokens = [TestToken["BARE_KEY"]]
    parser = Parser(input_tokens)
    assert parser._unquoted_key() == Key(input_tokens[0])

def test_unquoted_key_quoted() -> None:
    input_tokens = [TestToken["STRING_KEY"]]
    parser = Parser(input_tokens)
    assert parser._unquoted_key() is None

def test_quoted_key_quoted() -> None:
    input_tokens = [TestToken["STRING_KEY"]]
    parser = Parser(input_tokens)
    assert parser._quoted_key() == Key(input_tokens[0])

def test_quoted_key_unquoted() -> None:
    input_tokens = [TestToken["BARE_KEY"]]
    parser = Parser(input_tokens)
    assert parser._quoted_key() is None

def test_simple_key_unquoted() -> None:
    input_tokens = [TestToken["BARE_KEY"]]
    parser = Parser(input_tokens)
    assert parser._unquoted_key() == Key(input_tokens[0])

def test_simple_key_quoted() -> None:
    input_tokens = [TestToken["STRING_KEY"]]
    parser = Parser(input_tokens)
    assert parser._quoted_key() == Key(input_tokens[0])

def test_dotted_key_bare() -> None:
    input_tokens = [
        TestToken["BARE_KEY"],
        TestToken["KEY_SEP"],
        TestToken["BARE_KEY_2"],
    ]
    parser = Parser(input_tokens)
    expected_key = Key(TestToken["BARE_KEY"])
    expected_key += Key(TestToken["BARE_KEY_2"])
    assert parser._dotted_key() == expected_key

def test_dotted_key_string() -> None:
    input_tokens = [
        TestToken["STRING_KEY"],
        TestToken["KEY_SEP"],
        TestToken["STRING_KEY_2"],
    ]
    parser = Parser(input_tokens)
    expected_key = Key(TestToken["STRING_KEY"])
    expected_key += Key(TestToken["STRING_KEY_2"])
    assert parser._dotted_key() == expected_key

def test_dotted_key_mixed() -> None:
    input_tokens = [
        TestToken["BARE_KEY"],
        TestToken["KEY_SEP"],
        TestToken["STRING_KEY"],
    ]
    parser = Parser(input_tokens)
    expected_key = Key(TestToken["BARE_KEY"])
    expected_key += Key(TestToken["STRING_KEY"])
    assert parser._dotted_key() == expected_key

def test_dotted_key_three() -> None:
    input_tokens = [
        TestToken["BARE_KEY"],
        TestToken["KEY_SEP"],
        TestToken["STRING_KEY"],
        TestToken["KEY_SEP"],
        TestToken["BARE_KEY_2"]]
    parser = Parser(input_tokens)
    expected_key = Key(TestToken["BARE_KEY"])
    expected_key += Key(TestToken["STRING_KEY"])
    expected_key += Key(TestToken["BARE_KEY_2"])
    assert parser._dotted_key() == expected_key

def test_key_complex() -> None:
    input_tokens = [
        TestToken["BARE_KEY"],
        TestToken["KEY_SEP"],
        TestToken["STRING_KEY"],
        TestToken["KEY_SEP"],
        TestToken["BARE_KEY_2"],
    ]
    parser = Parser(input_tokens)
    expected_key = Key(TestToken["BARE_KEY"])
    expected_key += Key(TestToken["STRING_KEY"])
    expected_key += Key(TestToken["BARE_KEY_2"])
    assert parser._key() == expected_key

def test_key_value() -> None:
    input_tokens = [
        TestToken["BARE_KEY"],
        TestToken["EQUAL"],
        TestToken["STRING_KEY"],
    ]
    parser = Parser(input_tokens)
    expected_key = Key(TestToken["BARE_KEY"])
    assert parser._key() == expected_key

def test_array_one_line() -> None:
    input_tokens = [
        TestToken["ARRAY_START"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["STRING_KEY"],
        TestToken["ARRAY_END"],
    ]
    parser = Parser(input_tokens)
    expected_array = Array(
       Value(TestToken["STRING_KEY"]),
       Value(TestToken["STRING_KEY"]),
       Value(TestToken["STRING_KEY"]),
    )
    assert parser._array() == expected_array

def test_array_trailing_comma() -> None:
    input_tokens = [
        TestToken["ARRAY_START"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["ARRAY_END"],
    ]
    parser = Parser(input_tokens)
    test_value = Value(TestToken["STRING_KEY"])
    expected_array = Array(test_value, test_value, test_value)
    assert parser._array() == expected_array

def test_array_multiline() -> None:
    input_tokens = [
        TestToken["ARRAY_START"],
        TestToken["NEWLINE"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["NEWLINE"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["NEWLINE"],
        TestToken["STRING_KEY"],
        TestToken["NEWLINE"],
        TestToken["ARRAY_END"],
    ]
    parser = Parser(input_tokens)
    actual_array = parser._array()
    test_value = Value(TestToken["STRING_KEY"])
    expected_array = Array(test_value, test_value, test_value)

    assert actual_array == expected_array

def test_array_nested() -> None:
    input_tokens = [
        TestToken["ARRAY_START"],
        TestToken["NEWLINE"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["NEWLINE"],
        TestToken["ARRAY_START"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["NEWLINE"],
        TestToken["STRING_KEY"],
        TestToken["NEWLINE"],
        TestToken["ARRAY_END"],
        TestToken["NEWLINE"],
        TestToken["ARRAY_END"],
    ]
    parser = Parser(input_tokens)
    test_value = Value(TestToken["STRING_KEY"])
    expected_array = Array(test_value, Array(test_value, test_value))
    assert parser._array() == expected_array


def test_array_table() -> None:
    input_tokens = [
        TestToken["ARRAY_TABLE_START"],
        TestToken["STRING_KEY"],
        TestToken["ARRAY_TABLE_END"],
    ]
    parser = Parser(input_tokens)
    assert parser._array_table() == ArrayTable(Key(TestToken["STRING_KEY"]))

def test_array_table_mixed_key() -> None:
    input_tokens = [
        TestToken["ARRAY_TABLE_START"],
        TestToken["BARE_KEY"],
        TestToken["KEY_SEP"],
        TestToken["STRING_KEY"],
        TestToken["ARRAY_TABLE_END"],
    ]
    input_key = Key(TestToken["BARE_KEY"])
    input_key += Key(TestToken["STRING_KEY"])

    parser = Parser(input_tokens)
    assert parser._array_table() == ArrayTable(input_key)

def test_standard_table_mixed_key() -> None:
    input_tokens = [
        TestToken["TABLE_START"],
        TestToken["BARE_KEY"],
        TestToken["KEY_SEP"],
        TestToken["STRING_KEY"],
        TestToken["TABLE_END"],
    ]
    input_key = Key(TestToken["BARE_KEY"])
    input_key += Key(TestToken["STRING_KEY"])

    parser = Parser(input_tokens)
    assert parser._std_table() == Table(input_key)

def test_inline_table() -> None:
    input_tokens = [
        TestToken["INLINE_TABLE_START"],
        TestToken["STRING_KEY"],
        TestToken["EQUAL"],
        TestToken["STRING_KEY"],
        TestToken["COMMA"],
        TestToken["STRING_KEY"],
        TestToken["EQUAL"],
        TestToken["STRING_KEY"],
        TestToken["INLINE_TABLE_END"],
    ]
    parser = Parser(input_tokens)
    test_key_value = KeyValue(
        Key(TestToken["STRING_KEY"]),
        Value(TestToken["STRING_KEY"]),
    )
    expected_table = InlineTable(test_key_value, test_key_value)
    actual_table = parser._inline_table()
    assert actual_table == expected_table
