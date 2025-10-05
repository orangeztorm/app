
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """
    Request schema for user registration.
    """

    username: str
    email: EmailStr
    password: str
