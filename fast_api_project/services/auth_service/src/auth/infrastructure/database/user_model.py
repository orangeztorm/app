from sqlalchemy import Boolean, DateTime, String, func  # SQLAlchemy types and functions
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)  # ORM base and mapped column types


class Base(DeclarativeBase):  # Base class for all ORM models.
    """
    Base class for all ORM models.
    """


class UserModel(Base):
    """
    SQLAlchemy model for the User entity.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )  # Primary key column
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )  # Username column
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )  # Email column
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Hashed password column
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )  # Active status column
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )  # Creation timestamp column
