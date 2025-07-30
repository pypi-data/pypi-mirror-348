# ruff: noqa: E501,S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_arrays_toml() -> None:

    expected_exprs = [
        "KeyValue(integers = [ 1, 2, 3 ])",
        'KeyValue(colors = [ "red", "yellow", "green" ])',
        "KeyValue(nested_arrays_of_ints = [ [ 1, 2 ], [ 3, 4, 5 ] ])",
        'KeyValue(nested_mixed_array = [ [ 1, 2 ], [ "a", "b", "c" ] ])',
        """KeyValue(string_array = [ "all", 'strings', \"\"\"are the same\"\"\", '''type''' ])""",
    ]

    test_path = Path(RESOURCE_PATH) / "arrays" / "arrays.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_mixed_arrays_toml() -> None:

    expected_exprs = [
        "KeyValue(numbers = [ 0.1, 0.2, 0.5, 1, 2, 5 ])",
        'KeyValue(contributors = [ "Foo Bar <foo@example.com>", { name = "Baz Qux", email = "bazqux@example.com", url = "https://example.com/bazqux" } ])',
    ]

    test_path = Path(RESOURCE_PATH) / "arrays" / "mixed_arrays.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_multiline_arrays_toml() -> None:

    expected_exprs = [
        "KeyValue(integers2 = [ 1, 2, 3 ])",
        "KeyValue(integers3 = [ 1, 2 ])",
    ]

    test_path = Path(RESOURCE_PATH) / "arrays" / "multiline_arrays.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
