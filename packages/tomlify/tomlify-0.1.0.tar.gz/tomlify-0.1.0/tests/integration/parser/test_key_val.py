# ruff: noqa: S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_key_val_toml() -> None:

    test_path = Path(RESOURCE_PATH) / "key_value.toml"
    _, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_err = err.splitlines()[0]
    expected_err = "InvalidFormattingError: Invalid TOML Expression"

    assert return_code == 1
    assert actual_err == expected_err
