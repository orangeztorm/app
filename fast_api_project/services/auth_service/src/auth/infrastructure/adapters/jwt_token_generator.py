from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from jose import jwt

from ...application.ports.token_generator import TokenGenerator


class JWTTokenGenerator(TokenGenerator):
    """
    JWT implementation of the TokenGenerator interface.
    """

    def __init__(
        self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 1440
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, user_id: int, email: str) -> str:
        payload = {
            "sub": str(user_id),  # JWT standard uses string for subject
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes),
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
