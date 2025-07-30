run target:
    uv run src/tomlify/lexer/lex_runner.py {{target}}

publish:
    just fulltest
    just type 
    just lint 
    git tag -a 0.1.0 -m "Releasing version 0.1.0"
    git push origin 0.1.0

test:
    uv run pytest -vv --ignore=tests/integration

fulltest:
    uv run pytest -vv

lint:
    uv run ruff check --select ALL --fix --ignore D100,D101,D102,D103,D104,D105,D107,D400,FIX002,TD002,TD003,PT011

type:
    uv run mypy --strict src tests

todo:
    git grep "# TODO:" | grep -v grep
    git grep "noqa" -- '*.py' | grep -v N802 | grep -v S101 | grep -v DTZ001
    git grep "# type" -- '*.py'



# TODO: convert to a cleaner script / external tool for managing TODO list
