from __future__ import annotations

import re
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import validates

from app.extensions import bcrypt, db


USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.UniqueConstraint("username", name="uq_users_username"),
        db.UniqueConstraint("email", name="uq_users_email"),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    library_entries = db.relationship(
        "UserLibrary",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @validates("username")
    def validate_username(self, _key, username: str) -> str:
        if not isinstance(username, str):
            raise ValueError("El username debe ser un string.")

        normalized_username = username.strip()
        if not USERNAME_PATTERN.fullmatch(normalized_username):
            raise ValueError(
                "El username debe tener entre 3 y 30 caracteres y solo puede contener letras, números o _."
            )

        return normalized_username

    @validates("email")
    def validate_email(self, _key, email: str) -> str:
        if not isinstance(email, str) or not email.strip():
            raise ValueError("El email es obligatorio.")

        return email.strip().lower()

    def set_password(self, password: str) -> None:
        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña es obligatoria.")

        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        if not isinstance(password, str) or not password:
            return False

        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}'>"
