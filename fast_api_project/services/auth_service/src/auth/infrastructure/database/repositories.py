from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.domain.entities import User
from auth.domain.repositories.user_repository import IUserRepository

from .user_model import UserModel


class SQLAlchemyUserRepository(IUserRepository):
    """
    SQLAlchemy implementation of the User repository.
    """

    def __init__(
        self, session: AsyncSession
    ):  # Initialize with an async database session.
        self.session = session

    def to_domain(user_model: UserModel) -> User:
        """
        Convert a UserModel instance to a User entity.
        """
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
        )

    def to_model(user: User) -> UserModel:
        """
        Convert a User entity to a UserModel instance.
        """
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
        )

    async def create(self, user: User) -> User:
        user_model = self.to_model(user)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return self.to_domain(user_model)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return self.to_domain(user_model) if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self.to_domain(user_model) if user_model else None
