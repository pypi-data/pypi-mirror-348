from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import Self

from tomlify.lexer.token_type import TokenType

if TYPE_CHECKING:
    from collections.abc import Iterable

    from tomlify.lexer.lex_token import Literal, Token


@dataclass
class Comment:
    def __init__(self, token: Token) -> None:
        self.token = token

@dataclass
class Value:
    token: Token
    contents: Literal | None

    def __init__(self, token: Token) -> None:
        self.token = token
        if token.type_ == TokenType.BOOLEAN:
            self.contents = token.literal
        else:
            self.contents = token.lexeme

    def __repr__(self) -> str:
        return f"Value({self.contents})"

@dataclass
class Key:

    tokens: list[Token]
    name: Literal | None

    # Initial Call is the construction with a single name
    def __init__(self, token: Token) -> None:
        self.tokens = [token]
        self.name: str = token.lexeme if token.lexeme else str(token.literal)

    # Followup calls return new instances of Key appending them together
    def __iadd__(self, key: Key | None) -> Self:
        if key:
            self.tokens.extend(key.tokens)
            self.name =  f"{self.name}.{key.name}"
        return self

    def __repr__(self) -> str:
        return f"Key({self.name})"

class KeyValue:
    def __init__(self, key: Key, value: Value) -> None:
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        if isinstance(self.value, InlineTable):
            return f"KeyValue({self.key.name} = {{ {self.value.contents} }})"
        if isinstance(self.value, Array):
            if self.value.contents == "":
                return f"KeyValue({self.key.name} = [])"
            return f"KeyValue({self.key.name} = [ {self.value.contents} ])"
        return f"KeyValue({self.key.name} = {self.value.contents})"

class Array(list[Value], Value):
    contents: str

    def __init__(self, *args: Value | Array) -> None:
        super().__init__(args)
        if not args:
            self.contents = ""
            return
        self.contents = ", ".join([str(v.contents) for v in args])
        if isinstance(args[0], Array):
            self.contents = f"[ {self.contents} ]"
        if isinstance(args[0], InlineTable):
            self.contents = f"{{ {self.contents} }}"
        super().__init__(args)

    def append(self, value: Value | Array) -> None:
        new_content = value.contents
        if isinstance(value, Array):
            new_content = f"[ {new_content} ]"
        if isinstance(value, InlineTable):
            new_content = f"{{ {new_content} }}"
        if self.contents:
            new_content = ", " + str(new_content)
        self.contents += f"{new_content}"
        super().append(value)

    def extend(self, values: Iterable[Value | Array]) -> None:
        for value in values:
            self.append(value)

    def __repr__(self) -> str:
        return f"Array({self.contents})"

@dataclass
class Table:
    key: Key

    def __repr__(self) -> str:
        return f"Table({self.key.name})"


@dataclass
class InlineTable(list[KeyValue], Value):
    contents: str

    def __init__(self, *args: KeyValue) -> None:
        self.contents = ", ".join(f"{kv.key.name} = {kv.value.contents}" for kv in args)
        super().__init__(args)

    def __repr__(self) -> str:
        return f"InlineTable({self.contents})"

    def append(self, keyval: KeyValue) -> None:
        if self.contents:
            self.contents += ", "
        self.contents += f"{keyval.key.name} = {keyval.value.contents}"
        super().append(keyval)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InlineTable):
            return False
        return self.contents == other.contents


@dataclass
class ArrayTable(Table):
    key: Key

    def __repr__(self) -> str:
        return f"ArrayTable({self.key.name})"
