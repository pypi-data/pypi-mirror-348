# ruff: noqa: S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_bare_keys_toml() -> None:

    expected_exprs = [
        'KeyValue(key = "value")',
        'KeyValue(bare_key = "value")',
        'KeyValue(bare-key = "value")',
        'KeyValue(1234 = "value")',
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "bare_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_dotted_keys_toml() -> None:

    expected_exprs = [
        'KeyValue(name = "Orange")',
        'KeyValue(physical.color = "orange")',
        'KeyValue(physical.shape = "round")',
        'KeyValue(site."google.com" = True)',
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "dotted_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_dotted_keys_2_toml() -> None:

    expected_exprs = [
        'KeyValue(fruit.name = "banana")',
        'KeyValue(fruit.color = "yellow")',
        'KeyValue(fruit.flavor = "banana")',
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "dotted_keys_2.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_dotted_keys_3_toml() -> None:

    expected_exprs = [
        "KeyValue(fruit.apple.smooth = True)",
        "KeyValue(fruit.orange = 2)",
        "KeyValue(fruit.apple = 1)",
        "KeyValue(fruit.apple.smooth = True)",
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "dotted_keys_3.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_duplicate_keys_toml() -> None:

    expected_exprs = [
        'KeyValue(name = "Tom")',
        'KeyValue(name = "Pradyun")',
        'KeyValue(spelling = "favorite")',
        'KeyValue("spelling" = "favourite")',
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "duplicate_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_numeric_keys_toml() -> None:

    expected_exprs = [
        'KeyValue(3.14159 = "pi")',
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "numeric_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_order_keys_toml() -> None:

    expected_exprs = [
        'KeyValue(apple.type = "fruit")',
        'KeyValue(orange.type = "fruit")',
        'KeyValue(apple.skin = "thin")',
        'KeyValue(orange.skin = "thick")',
        'KeyValue(apple.color = "red")',
        'KeyValue(orange.color = "orange")',
        'KeyValue(apple.type = "fruit")',
        'KeyValue(apple.skin = "thin")',
        'KeyValue(apple.color = "red")',
        'KeyValue(orange.type = "fruit")',
        'KeyValue(orange.skin = "thick")',
        'KeyValue(orange.color = "orange")',
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "order_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_quoted_keys_toml() -> None:

    expected_exprs = [
        'KeyValue("127.0.0.1" = "value")',
        'KeyValue("character encoding" = "value")',
        'KeyValue("ʎǝʞ" = "value")',
        'KeyValue(\'key2\' = "value")',
        'KeyValue(\'quoted "value"\' = "value")',
        'KeyValue("" = "blank")',
        "KeyValue('' = 'blank')",
    ]

    test_path = Path(RESOURCE_PATH) / "keys" / "quoted_keys.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
