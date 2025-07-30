# ruff: noqa: S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_floats_toml() -> None:

    expected_exprs = [
        "KeyValue(flt1 = +1.0)",
        "KeyValue(flt2 = 3.1415)",
        "KeyValue(flt3 = -0.01)",
        "KeyValue(flt4 = 5e+22)",
        "KeyValue(flt5 = 1e06)",
        "KeyValue(flt6 = -2E-2)",
        "KeyValue(flt7 = 6.626e-34)",
    ]

    test_path = Path(RESOURCE_PATH) / "floats" / "floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_invalid_floats_toml() -> None:

    test_path = Path(RESOURCE_PATH) / "floats" / "invalid_floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_err = err.splitlines()[0]
    expected_err = "InvalidCharacterError: Invalid floating point input"

    assert return_code == 1
    assert actual_err == expected_err

def test_parse_special_floats_toml() -> None:

    expected_exprs = [
        "KeyValue(sf1 = inf)",
        "KeyValue(sf2 = +inf)",
        "KeyValue(sf3 = -inf)",
        "KeyValue(sf4 = nan)",
        "KeyValue(sf5 = +nan)",
        "KeyValue(sf6 = -nan)",
    ]

    test_path = Path(RESOURCE_PATH) / "floats" / "special_floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_underscore_floats_toml() -> None:

    expected_exprs = [
        "KeyValue(flt8 = 224_617.445_991_228)",
    ]

    test_path = Path(RESOURCE_PATH) / "floats" / "underscore_floats.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
