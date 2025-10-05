from domain import User

from auth.domain.exceptions.exceptions import UserAlreadyExistsError

from ...domain.repositories import IUserRepository
from ...domain.value_objects import Email, Password
from ..ports import PasswordHasher


class RegisterUser:
    """Use case for registering a new user."""

    def __init__(self, user_repo: IUserRepository, hasher: PasswordHasher):
        self.user_repo = user_repo
        self.hasher = hasher

    async def execute(self, username: str, email: str, password: str) -> User:
        # validate
        email_vo = Email(email)
        password_vo = Password(password)

        # check exists
        existing_user = await self.user_repo.get_by_email(email_vo.value)

        if existing_user:
            raise UserAlreadyExistsError(f"User with email {email_vo.value} already exists.")

        # hash password
        hashed = self.hasher.hash(password_vo.value)

        # create user entity
        new_user = User(
            id=None,
            username=username,
            email=email_vo.value,
            hashed_password=hashed,
        )

        # persist user
        return await self.user_repo.create(new_user)
