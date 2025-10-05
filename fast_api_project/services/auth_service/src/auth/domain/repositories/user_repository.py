from abc import ABC, abstractmethod
from typing import Optional

from ..entities import User


class IUserRepository(ABC):
    """
    Abstract base class for User repository.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user in the repository.
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.
        """
        pass
