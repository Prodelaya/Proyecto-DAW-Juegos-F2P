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


def seed_users() -> dict[str, int]:
    """Crea o actualiza usuarios demo y admin de forma idempotente."""
    summary = {"processed": 0, "failed": 0}

    admin_payload = {
        "username": "admin",
        "email": current_app.config["ADMIN_EMAIL"],
        "password": current_app.config["ADMIN_PASSWORD"],
        "is_admin": True,
    }

    for payload in [admin_payload, *DEMO_USERS]:
        email = payload["email"].strip().lower()

        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(
                    username=payload["username"],
                    email=email,
                    is_admin=payload.get("is_admin", False),
                )
                db.session.add(user)

            user.username = payload["username"]
            user.email = email
            user.is_admin = payload.get("is_admin", False)
            user.set_password(payload["password"])

            db.session.commit()
            summary["processed"] += 1
        except Exception as exc:  # pragma: no cover - robustez del seed manual
            db.session.rollback()
            summary["failed"] += 1
            current_app.logger.error(
                "No se pudo seedear el usuario email=%s: %s", email, exc
            )

    return summary
