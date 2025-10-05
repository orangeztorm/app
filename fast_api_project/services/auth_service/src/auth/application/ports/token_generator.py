from abc import ABC, abstractmethod
from typing import Dict


class TokenGenerator(ABC):
    """
    Abstract base class for token generation.
    """

    @abstractmethod
    def create_access_token(self, user_id: int, email: str) -> str:
        """
        Create a JWT access token for the given user ID and email.
        """
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Dict:
        """
        Verify the given JWT token and return its payload.
        """
        pass
