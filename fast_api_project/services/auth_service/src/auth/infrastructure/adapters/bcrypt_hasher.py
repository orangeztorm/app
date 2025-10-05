import bcrypt

from ...application.ports import PasswordHasher


class BcryptHasher(PasswordHasher):
    """
    Bcrypt implementation of the PasswordHasher interface.
    """

    def __init__(self, cost: int = 12):
        self.cost = cost

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=self.cost)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
