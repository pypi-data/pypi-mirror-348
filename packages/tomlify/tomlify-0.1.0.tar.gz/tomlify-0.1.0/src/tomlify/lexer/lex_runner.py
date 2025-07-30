#ruff: noqa: FBT001, FBT003
from pathlib import Path

import typer

from tomlify.lexer.exceptions import InvalidCharacterError
from tomlify.lexer.lexer import Lexer


def run(source: str) -> None:
    lexer = Lexer(source)
    try:
        lexer.lex()
    except InvalidCharacterError as e:
        typer.echo(e, err=True)
        raise
    tokens = lexer.get_tokens()
    for token in tokens:
        typer.echo(f"{token}")

def run_file(path: Path) -> None:
    with Path.open(path) as f:
        run(f.read())

def main(path: str) -> None:
    run_file(Path(path))

if __name__ == "__main__":
    typer.run(main)
