from __future__ import annotations

from flask import current_app

from app.extensions import db
from app.models.user import User

# Usuarios demo con datos de prueba
DEMO_USERS = [
    {'username': 'gamer_ana', 'email': 'ana@demo.com', 'password': 'demo1234'},
    {'username': 'pixel_pedro', 'email': 'pedro@demo.com', 'password': 'demo1234'},
    {'username': 'noob_lucia', 'email': 'lucia@demo.com', 'password': 'demo1234'},
    {'username': 'pro_carlos', 'email': 'carlos@demo.com', 'password': 'demo1234'},
    {'username': 'indie_maria', 'email': 'maria@demo.com', 'password': 'demo1234'},
]


def seed_users():
    """Crea o actualiza usuarios demo y admin de forma idempotente."""
    created_or_updated = 0

    admin_payload = {
        "username": "admin",
        "email": current_app.config["ADMIN_EMAIL"],
        "password": current_app.config["ADMIN_PASSWORD"],
        "is_admin": True,
    }

    for payload in [admin_payload, *DEMO_USERS]:
        user = User.query.filter_by(email=payload["email"].strip().lower()).first()
        if user is None:
            user = User(
                username=payload["username"],
                email=payload["email"],
                is_admin=payload.get("is_admin", False),
            )
            db.session.add(user)

        user.username = payload["username"]
        user.email = payload["email"]
        user.is_admin = payload.get("is_admin", False)
        user.set_password(payload["password"])
        created_or_updated += 1

    db.session.commit()
    return created_or_updated
