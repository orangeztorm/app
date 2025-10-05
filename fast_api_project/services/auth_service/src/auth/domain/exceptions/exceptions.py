"""
Domain exceptions for the auth service.
"""


class AuthDomainException(Exception):
    """Base exception for auth domain errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(AuthDomainException):
    """Exception raised when attempting to create a user that already exists."""

    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists.")
        self.email = email


class UserNotFoundError(AuthDomainException):
    """Exception raised when a user is not found."""

    def __init__(self, email: str):
        super().__init__(f"User with email {email} not found.")
        self.email = email


class InvalidCredentialsError(AuthDomainException):
    """Exception raised for invalid login credentials."""

    def __init__(self):
        super().__init__("Invalid email or password.")
