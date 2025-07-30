# ruff: noqa: E501,S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_aots_toml() -> None:

    expected_exprs = [
        "ArrayTable(products)",
        'KeyValue(name = "Hammer")',
        "KeyValue(sku = 738594937)",
        "ArrayTable(products)",
        "ArrayTable(products)",
        'KeyValue(name = "Nail")',
        "KeyValue(sku = 284758393)",
        'KeyValue(color = "gray")',
    ]

    test_path = Path(RESOURCE_PATH) / "aots" / "aots.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_aots_2_toml() -> None:

    expected_exprs = [
        "ArrayTable(fruits)",
        'KeyValue(name = "apple")',
        "Table(fruits.physical)",
        'KeyValue(color = "red")',
        'KeyValue(shape = "round")',
        "ArrayTable(fruits.varieties)",
        'KeyValue(name = "red delicious")',
        "ArrayTable(fruits.varieties)",
        'KeyValue(name = "granny smith")',
        "ArrayTable(fruits)",
        'KeyValue(name = "banana")',
        "ArrayTable(fruits.varieties)",
        'KeyValue(name = "plantain")',
    ]

    test_path = Path(RESOURCE_PATH) / "aots" / "aots_2.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_inline_aots_toml() -> None:

    expected_exprs = [
        "KeyValue(points = [ { x = 1, y = 2, z = 3 }, { x = 7, y = 8, z = 9 }, { x = 2, y = 4, z = 8 } ])",
    ]

    test_path = Path(RESOURCE_PATH) / "aots" / "inline_aots.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_invalid_aots_toml() -> None:

    expected_exprs = [
        "Table(fruit.physical)",
        'KeyValue(color = "red")',
        'KeyValue(shape = "round")',
        "ArrayTable(fruit)",
        'KeyValue(name = "apple")',
        "KeyValue(fruits = [])",
        "ArrayTable(fruits)",
        "ArrayTable(fruits)",
        'KeyValue(name = "apple")',
        "ArrayTable(fruits.varieties)",
        'KeyValue(name = "red delicious")',
        "Table(fruits.varieties)",
        'KeyValue(name = "granny smith")',
        "Table(fruits.physical)",
        'KeyValue(color = "red")',
        'KeyValue(shape = "round")',
        "ArrayTable(fruits.physical)",
        'KeyValue(color = "green")',
    ]

    test_path = Path(RESOURCE_PATH) / "aots" / "invalid_aots.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
