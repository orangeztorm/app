from dataclasses import (  # generates useful methods like __init__, __repr__, etc.
    dataclass,
    field,
)
from datetime import datetime, timezone  # python's built-in datetime module
from typing import Optional  # for optional type hinting


@dataclass
class User:
    """
    Represents a user in the authentication system.

    LEARN:
    - This class is part of the DOMAIN layer.
    - It has no framework dependencies (pure Python).
    - Business logic lives here, not in your controllers.
    """

    id: Optional[int]  # Unique identifier for the user, optional for new users
    username: str  # Username of the user
    email: str  # Email address of the user
    hashed_password: str  # Hashed password for security
    is_active: bool = True  # Indicates if the user account is active
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))  # Timestamp of when the user was created

    def deactivate(self):
        '''
        Deactivates the user account.
        '''
        self.is_active = False

    def activate(self):
        '''
        Activates the user account.
        '''
        self.is_active = True
