class LexerEOFError(EOFError):
    """Attempting to advance past end of file."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"LexerEOFError: {self.message}"


class InvalidCharacterError(ValueError):
    """Invalid character in input file."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidCharacterError: {self.message}"

class UnterminatedStringError(ValueError):
    """Unterminated string in input file."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"UnterminatedStringError: {self.message}"
