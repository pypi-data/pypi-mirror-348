# ruff: noqa: E501,S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_basic_strings_toml() -> None:

    expected_exprs = [
        """KeyValue(str = "I'm a string. \\"You can quote me\\". Name\\tJos\\u00E9\\nLocation\\tSF.")""",
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "basic_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_literal_strings_toml() -> None:

    expected_exprs = [
        "KeyValue(winpath = 'C:\\Users\\nodejs\\templates')",
        "KeyValue(winpath2 = '\\\\ServerX\\admin$\\system32\\')",
        """KeyValue(quoted = 'Tom "Dubs" Preston-Werner')""",
        "KeyValue(regex = '<\\i\\c*\\s*>')",
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "literal_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_multiline_literal_strings_toml() -> None:

    expected_exprs = [
        "KeyValue(regex2 = '''I [dw]on't need \\d{2} apples''')",
        "KeyValue(lines = '''",
        "The first newline is",
        "trimmed in raw strings.",
        "   All other whitespace",
        "   is preserved.",
        "''')",
        "KeyValue(quot15 = '''Here are fifteen quotation marks: "
        '"""""""""""""""\'\'\')',
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "multiline_literal_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_multiline_strings_toml() -> None:

    expected_exprs = [
        'KeyValue(str1 = """',
        "Roses are red",
        'Violets are blue""")',
        'KeyValue(str2 = "Roses are red\\nViolets are blue")',
        'KeyValue(str3 = "Roses are red\\r\\nViolets are blue")',
        'KeyValue(str1 = "The quick brown fox jumps over the lazy dog.")',
        'KeyValue(str2 = """',
        "The quick brown \\",
        "",
        "",
        "  fox jumps over \\",
        '    the lazy dog.""")',
        'KeyValue(str3 = """\\',
        "       The quick brown \\",
        "       fox jumps over \\",
        "       the lazy dog.\\",
        '       """)',
        'KeyValue(str4 = """Here are two quotation marks: "". Simple enough.""")',
        'KeyValue(str5 = """Here are three quotation marks: ""\\".""")',
        'KeyValue(str6 = """Here are fifteen quotation marks: '
        '""\\"""\\"""\\"""\\"""\\".""")',
    ]

    test_path = Path(RESOURCE_PATH) / "strings" / "multiline_strings.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
