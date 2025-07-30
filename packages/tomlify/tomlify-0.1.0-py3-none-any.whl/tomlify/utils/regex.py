import dataclasses
import re
from typing import Any


@dataclasses.dataclass
class RegexChecker:
    string: str
    match: str | None = None
    _groups: tuple[str | Any, ...] = ()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            other = re.compile(other)
        if not isinstance(other, re.Pattern):
            raise NotImplementedError
        match = other.match(self.string)
        if match is None:
            return False
        self.match = match.string[match.start(): match.end()]
        self._groups = match.groups()
        return self.match is not None

    def __str__(self) -> str:
        if not self.match:
            return ""
        return self.match

    def __len__(self) -> int:
        if not self.match:
            return 0
        return len(self.match)

    def groups(self) -> tuple[str | Any, ...]:
        if not self.match:
            return ("",)
        return self._groups

    def group(self, num: int) -> str:
        if not self.match:
            return ""
        return self._groups[num]
