# ruff: noqa: S101

from pathlib import Path

from tests.integration.runner import RESOURCE_PATH, run_test

SCRIPT_PATH = Path("src/tomlify/parser/parse_runner.py")

def test_parse_dotted_tables_toml() -> None:

    expected_exprs = [
        """KeyValue(fruit.apple.color = "red")""",
        """KeyValue(fruit.apple.taste.sweet = True)""",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "dotted_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_inline_tables_toml() -> None:

    expected_exprs = [
        'KeyValue(name = { first = "Tom", last = "Preston-Werner" })',
        "KeyValue(point = { x = 1, y = 2 })",
        'KeyValue(animal = { type.name = "pug" })',
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "inline_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_invalid_inline_tables_toml() -> None:

    expected_exprs: list[str] = [
        "Table(product)",
        'KeyValue(type = { name = "Nail" })',
        "Table(product)",
        'KeyValue(type.name = "Nail")',
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "invalid_inline_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_invalid_tables_toml() -> None:

    expected_exprs = [
        "Table(fruit)",
        """KeyValue(apple = "red")""",
        "Table(fruit)",
        """KeyValue(orange = "orange")""",
        "Table(fruit)",
        """KeyValue(apple = "red")""",
        "Table(fruit.apple)",
        """KeyValue(texture = "smooth")""",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "invalid_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_levelled_tables_toml() -> None:

    expected_exprs = [
        "Table(fruit)",
        """KeyValue(apple.color = "red")""",
        "KeyValue(apple.taste.sweet = True)",
        "Table(fruit.apple.texture)",
        "KeyValue(smooth = True)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "levelled_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_named_tables_toml() -> None:

    expected_exprs = [
        """Table(dog."tater.man")""",
        """KeyValue(type.name = "pug")""",
        "Table(a.b.c)",
        "Table(d.e.f)",
        "Table(g.h.i)",
        """Table(j."ʞ".'l')""",
        "Table(x.y.z.w)",
        "Table(x)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "named_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_ordered_tables_toml() -> None:

    expected_exprs = [
        "Table(fruit.apple)",
        "Table(animal)",
        "Table(fruit.orange)",
        "Table(fruit.apple)",
        "Table(fruit.orange)",
        "Table(animal)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "ordered_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_tables_toml() -> None:

    expected_exprs = [
        "Table(table)",
        "Table(table-1)",
        """KeyValue(key1 = "some string")""",
        "KeyValue(key2 = 123)",
        "Table(table-2)",
        """KeyValue(key1 = "another string")""",
        "KeyValue(key2 = 456)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs

def test_parse_top_tables_toml() -> None:

    expected_exprs = [
        """KeyValue(name = "Fido")""",
        """KeyValue(breed = "pug")""",
        "Table(owner)",
        """KeyValue(name = "Regina Dogman")""",
        "KeyValue(member_since = 1999-08-04)",
    ]

    test_path = Path(RESOURCE_PATH) / "tables" / "top_tables.toml"
    out, err, return_code = run_test(SCRIPT_PATH, test_path)

    actual_tokens = out.splitlines()

    assert return_code == 0
    assert err == ""
    assert actual_tokens == expected_exprs
