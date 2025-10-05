from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Response schema for user information.
    """

    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
