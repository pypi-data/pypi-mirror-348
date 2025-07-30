# ruff: noqa: S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_base_integers_toml() -> None:

    expected_exprs = [
        "KeyValue(hex1 = 0xDEADBEEF)",
        "KeyValue(hex2 = 0xdeadbeef)",
        "KeyValue(hex3 = 0xdead_beef)",
        "KeyValue(oct1 = 0o01234567)",
        "KeyValue(oct2 = 0o755)",
        "KeyValue(bin1 = 0b11010110)",
    ]

    test_path = Path(RESOURCE_PATH) / "integers" / "base_integers.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_integers_toml() -> None:

    expected_exprs = [
        "KeyValue(int1 = +99)",
        "KeyValue(int2 = 42)",
        "KeyValue(int3 = 0)",
        "KeyValue(int4 = -17)",
    ]

    test_path = Path(RESOURCE_PATH) / "integers" / "integers.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_underscore_integers_toml() -> None:

    expected_exprs = [
        "KeyValue(int5 = 1_000)",
        "KeyValue(int6 = 5_349_221)",
        "KeyValue(int7 = 53_49_221)",
        "KeyValue(int8 = 1_2_3_4_5)",
    ]

    test_path = Path(RESOURCE_PATH) / "integers" / "underscore_integers.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
