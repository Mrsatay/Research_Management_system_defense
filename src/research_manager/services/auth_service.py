from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from sqlalchemy import select

from ..database import session_scope
from ..models import User


class AuthService:
    """Authentication operations for application users."""

    def __init__(self) -> None:
        self.password_hasher = PasswordHasher()

    def ensure_default_admin(self) -> None:
        with session_scope() as session:
            existing = session.scalar(select(User).where(User.username == "admin"))
            if existing is None:
                session.add(
                    User(
                        username="admin",
                        password_hash=self.password_hasher.hash("admin123"),
                    )
                )

    def authenticate(self, username: str, password: str) -> bool:
        username = username.strip()
        if not username or not password:
            return False

        with session_scope() as session:
            user = session.scalar(select(User).where(User.username == username))
            if user is None:
                return False
            try:
                return self.password_hasher.verify(user.password_hash, password)
            except (VerifyMismatchError, VerificationError):
                return False
