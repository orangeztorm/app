import re # regular expression matching patterns
from dataclasses import dataclass # generates useful methods like __init__, __repr__, etc.

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
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    


@dataclass(frozen=True)  # frozen makes the instance immutable
class Password:
    """
    Value Object representing a Password.

    LEARN:
    - This class is part of the DOMAIN layer.
    - It has no framework dependencies (pure Python).
    - Business logic lives here, not in your controllers.
    """

    value: str # password string

    def __post_init__(self):
        if not self._is_strong(self.value):
            raise ValueError(f"Weak password: {self._error_message(self.value)}")
        
    @staticmethod
    def _is_strong(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[\W_]', password):  # special characters
            return False
        return True
    
    @staticmethod
    def _error_message(password: str) -> str:
        messages = []
        if len(password) < 8:
            messages.append("at least 8 characters")
        if not re.search(r'[A-Z]', password):
            messages.append("one uppercase letter")
        if not re.search(r'[a-z]', password):
            messages.append("one lowercase letter")
        if not re.search(r'[0-9]', password):
            messages.append("one digit")
        if not re.search(r'[\W_]', password):  # special characters
            messages.append("one special character")
        return "Password must contain: " + ", ".join(messages) + "."



    