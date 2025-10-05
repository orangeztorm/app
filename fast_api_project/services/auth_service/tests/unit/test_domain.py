import pytest

from auth.domain import Email, Password, User


class TestUser:
    def test_user_creation(self):
        """
        Test creating a User entity.
        """

        email_vo = Email("testuser@example.com")
        hashed = Password("Bcrypt$2b$12$fakehash")
        user = User(
            id=1,
            username="testuser",
            email=email_vo.value,
            hashed_password=hashed.value,
        )
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == email_vo.value
        assert user.hashed_password == hashed.value
        assert user.is_active is True
        assert user.created_at is not None

    def test_user_deactivation(self):
        """
        Test deactivating a User entity.
        """
        email_vo = Email("testuser@example.com")
        hashed = Password("Bcrypt$2b$12$fakehash")
        user = User(
            id=1,
            username="testuser",
            email=email_vo.value,
            hashed_password=hashed.value,
        )
        user.deactivate()
        assert user.is_active is False


class TestEmail:
    def test_valid_email(self):
        """
        Test creating a valid Email value object.
        """
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_invalid_email(self):
        """
        Test creating an invalid Email value object.
        """
        with pytest.raises(ValueError):
            Email("invalid-email")


class TestPassword:
    def test_strong_password(self):
        """
        Test creating a strong Password value object.
        """
        password = Password("Str0ngP@ssw0rd!")
        assert password.value == "Str0ngP@ssw0rd!"

    def test_weak_password(self):
        """
        Test creating a weak Password value object.
        """
        with pytest.raises(ValueError):
            Password("weak")  # Too short and lacks complexity
