import re  # regular expression matching patterns
from dataclasses import (
    dataclass,  # generates useful methods like __init__, __repr__, etc.
)


@dataclass(frozen=True)  # frozen makes the instance immutable
class Email:
    """
    Value Object representing an Email address.

    LEARN:
    - This class is part of the DOMAIN layer.
    - It has no framework dependencies (pure Python).
    - Business logic lives here, not in your controllers.
    """

    value: str  # The actual email address

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise ValueError(f"Invalid email address: {self.value}")

    @staticmethod
    def _is_valid(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
