# ruff: noqa: E501,S101,S603

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/lexer/lex_runner.py")

def test_basic_strings_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"I\\\'m a string. \\\\"You can quote me\\\\". Name\\\\tJos\\\\u00E9\\\\nLocation\\\\tSF."', literal='I\\\'m a string. \\\\"You can quote me\\\\". Name\\\\tJos\\\\u00E9\\\\nLocation\\\\tSF.', line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=2)",
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "basic_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_literal_strings_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# What you see is what you get.', literal=' What you see is what you get.', line=1)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='winpath', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'C:\\\\Users\\\\nodejs\\\\templates\'", literal='C:\\\\Users\\\\nodejs\\\\templates', line=2)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=2)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='winpath2', literal=None, line=3)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=3)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'\\\\\\\\ServerX\\\\admin$\\\\system32\\\\'", literal='\\\\\\\\ServerX\\\\admin$\\\\system32\\\\', line=3)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='quoted', literal=None, line=4)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=4)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='\\\'Tom "Dubs" Preston-Werner\\\'', literal='Tom "Dubs" Preston-Werner', line=4)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='regex', literal=None, line=5)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=5)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'<\\\\i\\\\c*\\\\s*>'", literal='<\\\\i\\\\c*\\\\s*>', line=5)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=6)",
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "literal_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens


def test_multiline_strings_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str1', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""\\nRoses are red\\nViolets are blue"""', literal='\\nRoses are red\\nViolets are blue', line=1)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=3)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=4)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# On a Unix system, the above multi-line string will most likely be the same as:', literal=' On a Unix system, the above multi-line string will most likely be the same as:', line=5)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=5)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str2', literal=None, line=6)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=6)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Roses are red\\\\nViolets are blue"', literal='Roses are red\\\\nViolets are blue', line=6)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=6)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# On a Windows system, it will most likely be equivalent to:', literal=' On a Windows system, it will most likely be equivalent to:', line=8)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str3', literal=None, line=9)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=9)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"Roses are red\\\\r\\\\nViolets are blue"', literal='Roses are red\\\\r\\\\nViolets are blue', line=9)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=10)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str1', literal=None, line=11)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=11)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"The quick brown fox jumps over the lazy dog."', literal='The quick brown fox jumps over the lazy dog.', line=11)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=11)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=12)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str2', literal=None, line=13)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=13)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""\\nThe quick brown \\\\\\n\\n\\n  fox jumps over \\\\\\n    the lazy dog."""', literal='\\nThe quick brown \\\\\\n\\n\\n  fox jumps over \\\\\\n    the lazy dog.', line=13)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=16)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=17)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str3', literal=None, line=18)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=18)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""\\\\\\n       The quick brown \\\\\\n       fox jumps over \\\\\\n       the lazy dog.\\\\\\n       """', literal='\\\\\\n       The quick brown \\\\\\n       fox jumps over \\\\\\n       the lazy dog.\\\\\\n       ', line=18)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=18)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=19)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str4', literal=None, line=20)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=20)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""Here are two quotation marks: "". Simple enough."""', literal='Here are two quotation marks: "". Simple enough.', line=20)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=20)",
        '''Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# str5 = """Here are three quotation marks: """."""  # INVALID', literal=' str5 = """Here are three quotation marks: """."""  # INVALID', line=21)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=21)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str5', literal=None, line=22)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=22)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""Here are three quotation marks: ""\\\\"."""', literal='Here are three quotation marks: ""\\\\".', line=22)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=22)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='str6', literal=None, line=23)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=23)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='"""Here are fifteen quotation marks: ""\\\\"""\\\\"""\\\\"""\\\\"""\\\\"."""', literal='Here are fifteen quotation marks: ""\\\\"""\\\\"""\\\\"""\\\\"""\\\\".', line=23)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=23)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=24)",
        """Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# "This," she said, "is just a pointless statement."', literal=' "This," she said, "is just a pointless statement."', line=25)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=25)",
        '''Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# str7 = """"This," she said, "is just a pointless statement.""""', literal=' str7 = """"This," she said, "is just a pointless statement.""""', line=26)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=26)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=27)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# TODO: Figure out how to uncomment str7', literal=' TODO: Figure out how to uncomment str7', line=28)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=28)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=29)",

    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "multiline_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens

def test_multiline_literal_strings_toml() -> None:

    expected_tokens = [
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='regex2', literal=None, line=1)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=1)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'''I [dw]on't need \\\\d{2} apples'''", literal="I [dw]on't need \\\\d{2} apples", line=1)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=1)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='lines', literal=None, line=2)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=2)",
        """Token(type_=<TokenType.STRING: 'STRING'>, lexeme="'''\\nThe first newline is\\ntrimmed in raw strings.\\n   All other whitespace\\n   is preserved.\\n'''", literal='\\nThe first newline is\\ntrimmed in raw strings.\\n   All other whitespace\\n   is preserved.\\n', line=2)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=7)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=8)",
        "Token(type_=<TokenType.IDENTIFIER: 'IDENTIFIER'>, lexeme='quot15', literal=None, line=9)",
        "Token(type_=<TokenType.EQUAL: 'EQUAL'>, lexeme='=', literal=None, line=9)",
        '''Token(type_=<TokenType.STRING: 'STRING'>, lexeme='\\\'\\\'\\\'Here are fifteen quotation marks: """""""""""""""\\\'\\\'\\\'', literal='Here are fifteen quotation marks: """""""""""""""', line=9)''',
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=9)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=10)",
        """Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme="# apos15 = '''Here are fifteen apostrophes: ''''''''''''''''''  # INVALID", literal=" apos15 = '''Here are fifteen apostrophes: ''''''''''''''''''  # INVALID", line=11)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=11)",
        """Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# apos15 = "Here are fifteen apostrophes: \\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'"', literal=' apos15 = "Here are fifteen apostrophes: \\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'\\\'"', line=12)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=12)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=13)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# TODO : Figure out how to uncomment the second apos15 and still have it work', literal=' TODO : Figure out how to uncomment the second apos15 and still have it work', line=14)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=14)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=15)",
        """Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme="# 'That,' she said, 'is still pointless.'", literal=" 'That,' she said, 'is still pointless.'", line=16)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=16)",
        """Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme="# str = ''''That,' she said, 'is still pointless.''''", literal=" str = ''''That,' she said, 'is still pointless.''''", line=17)""",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=17)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=18)",
        "Token(type_=<TokenType.COMMENT: 'COMMENT'>, lexeme='# TODO : Figure out how to uncomment the second str and still have it work', literal=' TODO : Figure out how to uncomment the second str and still have it work', line=19)",
        "Token(type_=<TokenType.NEWLINE: 'NEWLINE'>, lexeme='\\n', literal=None, line=19)",
        "Token(type_=<TokenType.EOF: 'EOF'>, lexeme='', literal=None, line=20)",
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "multiline_literal_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_tokens
