class InvalidArrayError(ValueError):
    """Invalid Array formatting."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidArrayError: {self.message}"

class InvalidArrayTableError(ValueError):
    """Invalid Array Table formatting."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidArrayTableError: {self.message}"

class InvalidTableError(ValueError):
    """Invalid Table formatting."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidTableError: {self.message}"

class InvalidInlineTableError(ValueError):
    """Invalid Inline Table formatting."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidInlineTableError: {self.message}"


class InvalidFormattingError(ValueError):
    """Invalid formatting."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidFormattingError: {self.message}"
