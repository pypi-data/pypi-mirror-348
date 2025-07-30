# ruff: noqa: S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_dates_toml() -> None:

    expected_exprs = [
        "KeyValue(ld1 = 1979-05-27)",
    ]

    test_path = Path(RESOURCE_PATH) / "datetimes" / "dates.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_local_datetimes_toml() -> None:

    expected_exprs = [
        "KeyValue(ldt1 = 1979-05-27T07:32:00)",
        "KeyValue(ldt2 = 1979-05-27T00:32:00.999999)",
    ]

    test_path = Path(RESOURCE_PATH) / "datetimes" / "local_datetimes.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_offset_datetimes_toml() -> None:

    expected_exprs = [
        "KeyValue(odt1 = 1979-05-27T07:32:00Z)",
        "KeyValue(odt2 = 1979-05-27T00:32:00-07:00)",
        "KeyValue(odt3 = 1979-05-27T00:32:00.999999-07:00)",
        "KeyValue(odt4 = 1979-05-27 07:32:00Z)",
    ]

    test_path = Path(RESOURCE_PATH) / "datetimes" / "offset_datetimes.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_times_toml() -> None:

    expected_exprs = [
        "KeyValue(lt1 = 07:32:00)",
        "KeyValue(lt2 = 00:32:00.999999)",
    ]

    test_path = Path(RESOURCE_PATH) / "datetimes" / "times.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
