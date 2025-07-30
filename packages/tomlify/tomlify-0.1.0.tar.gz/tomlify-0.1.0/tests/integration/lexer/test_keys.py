# ruff: noqa: E501, S101, S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_bare_key_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='key', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='bare_key', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=2)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='bare-key', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=3)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='1234', literal=1234, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=4)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=5)",
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "bare_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens


def test_dotted_keys_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Orange"', literal='Orange', line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='physical', literal=None, line=2)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='color', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"orange"', literal='orange', line=2)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='physical', literal=None, line=3)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='shape', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"round"', literal='round', line=3)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='site', literal=None, line=4)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"google.com"', literal='google.com', line=4)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        "Token(type_=<TokenType.BOOLEAN: 'BOOLEAN'>, lexeme='true', literal=True, line=4)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=5)",
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "dotted_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_dotted_keys_2_toml() -> None:

    expected_tokens = [
       "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='fruit', literal=None, line=1)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"banana"', literal='banana', line=1)""",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# this is best practice', literal=' this is best practice', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='fruit', literal=None, line=2)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='color', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"yellow"', literal='yellow', line=2)""",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# same as fruit.color', literal=' same as fruit.color', line=2)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='fruit', literal=None, line=3)",
        "Token(type_=<TokenType.DOT: 'DOT'>, lexeme='.', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='flavor', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"banana"', literal='banana', line=3)""",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# same as fruit.flavor', literal=' same as fruit.flavor', line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=4)",
]

    test_path = Path(RESOURCE_PATH) / "keys" / "dotted_keys_2.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_duplicate_keys_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# DO NOT DO THIS', literal=' DO NOT DO THIS', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Tom"', literal='Tom', line=2)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='name', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Pradyun"', literal='Pradyun', line=3)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# THIS WILL NOT WORK', literal=' THIS WILL NOT WORK', line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='spelling', literal=None, line=6)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=6)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"favorite"', literal='favorite', line=6)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"spelling"', literal='spelling', line=7)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=7)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"favourite"', literal='favourite', line=7)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=8)",
]

    test_path = Path(RESOURCE_PATH) / "keys" / "duplicate_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_numeric_keys_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.NUMBER: 'NUMBER'>, lexeme='3.14159', literal=3.14159, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"pi"', literal='pi', line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=2)",
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "numeric_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_quoted_keys_toml() -> None:

    expected_tokens = [
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"127.0.0.1"', literal='127.0.0.1', line=1)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"character encoding"', literal='character encoding', line=2)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=2)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"ʎǝʞ"', literal='ʎǝʞ', line=3)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=3)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'key2'", literal='key2', line=4)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=4)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='\\'quoted "value"\\'', literal='quoted "value"', line=5)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"value"', literal='value', line=5)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        'Token(type_=<TokenType.COMMENT: \'COMMENT\'>, lexeme=\'# = "no key name"  # INVALID\', literal=\' = "no key name"  # INVALID\', line=7)',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='""', literal='', line=8)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=8)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"blank"', literal='blank', line=8)""",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# VALID but discouraged', literal=' VALID but discouraged', line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="''", literal='', line=9)""",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=9)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'blank'", literal='blank', line=9)""",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# VALID but discouraged', literal=' VALID but discouraged', line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=10)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# TODO Fix Commented "
        "Invalid code', literal=' TODO Fix Commented Invalid code', line=11)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, "
        "line=11)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=12)"]


    test_path = Path(RESOURCE_PATH) / "keys" / "quoted_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
