#ruff: noqa: FBT001, FBT003
from pathlib import Path

import typer

from tomlify.lexer.exceptions import InvalidCharacterError
from tomlify.lexer.lexer import Lexer
from tomlify.parser.exceptions import InvalidFormattingError
from tomlify.parser.parser import Parser


def run(source: str) -> None:
    lexer = Lexer(source)
    try:
        lexer.lex()
    except InvalidCharacterError as e:
        typer.echo(e, err=True)
        raise
    tokens = lexer.get_tokens()
    parser = Parser(tokens)
    try:
        expressions = parser.parse()
    except InvalidFormattingError as e:
        typer.echo(e, err=True)
        raise
    for expression in expressions:
        typer.echo(expression)

def run_file(path: Path) -> None:
    with Path.open(path) as f:
        run(f.read())

def main(path: str) -> None:
    run_file(Path(path))

if __name__ == "__main__":
    typer.run(main)
