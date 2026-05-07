from __future__ import annotations

from flask import current_app

from app.extensions import db
from app.models.user import User

# Usuarios demo base con datos de prueba
BASE_DEMO_USERS = [
    {'username': 'gamer_ana', 'email': 'ana@demo.com', 'password': 'demo1234'},
    {'username': 'pixel_pedro', 'email': 'pedro@demo.com', 'password': 'demo1234'},
    {'username': 'noob_lucia', 'email': 'lucia@demo.com', 'password': 'demo1234'},
    {'username': 'pro_carlos', 'email': 'carlos@demo.com', 'password': 'demo1234'},
    {'username': 'indie_maria', 'email': 'maria@demo.com', 'password': 'demo1234'},
]


def _build_extra_demo_users(total: int = 100) -> list[dict[str, str]]:
    """Genera usuarios demo adicionales de forma determinista."""
    extra_users: list[dict[str, str]] = []

    for index in range(1, total + 1):
        extra_users.append(
            {
                "username": f"demo_user_{index:03d}",
                "email": f"demo{index:03d}@demo.com",
                "password": "demo1234",
            }
        )

    return extra_users


def seed_users() -> dict[str, int]:
    """Crea o actualiza usuarios demo y admin de forma idempotente."""
    summary = {"processed": 0, "failed": 0, "skipped": 0}

    admin_payload = {
        "username": "admin",
        "email": current_app.config["ADMIN_EMAIL"],
        "password": current_app.config["ADMIN_PASSWORD"],
        "is_admin": True,
    }

    payloads = [admin_payload, *BASE_DEMO_USERS, *_build_extra_demo_users()]

    calaya_password = current_app.config.get("CALAYA_PASSWORD")
    calaya_email = (current_app.config.get("CALAYA_EMAIL") or "").strip().lower()

    if calaya_password:
        payloads.append(
            {
                "username": "Calaya",
                "email": calaya_email or "pablo_laya92@hotmail.com",
                "password": calaya_password,
                "is_admin": False,
            }
        )
    else:
        summary["skipped"] += 1
        current_app.logger.info(
            "Usuario especial Calaya omitido: CALAYA_PASSWORD no está definido."
        )

    for payload in payloads:
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
