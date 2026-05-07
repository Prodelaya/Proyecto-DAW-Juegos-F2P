from __future__ import annotations

import re
from urllib.parse import urljoin, urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import USERNAME_PATTERN, User

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

auth_bp = Blueprint("auth_bp", __name__)


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _normalize_email(value: str | None) -> str:
    return _normalize_text(value).lower()


def _is_safe_next_target(target: str | None) -> bool:
    if not target:
        return False

    ref_url = urlsplit(request.host_url)
    test_url = urlsplit(urljoin(request.host_url, target))
    return test_url.scheme in {"http", "https"} and ref_url.netloc == test_url.netloc


def _resolve_next_target() -> str:
    requested_next = request.form.get("next") or request.args.get("next")
    if _is_safe_next_target(requested_next):
        normalized_target = urlsplit(urljoin(request.host_url, requested_next))
        resolved_target = normalized_target.path or url_for("main_bp.home")
        if normalized_target.query:
            resolved_target = f"{resolved_target}?{normalized_target.query}"
        if normalized_target.fragment:
            resolved_target = f"{resolved_target}#{normalized_target.fragment}"
        return resolved_target

    return url_for("main_bp.home")


def _resolve_next_field_value() -> str:
    requested_next = request.form.get("next") or request.args.get("next")
    if _is_safe_next_target(requested_next):
        return requested_next

    return ""


def _build_register_context(form_data: dict[str, str], errors: dict[str, str]):
    return {
        "form_data": form_data,
        "errors": errors,
    }


def _build_login_context(
    form_data: dict[str, str], errors: dict[str, str], general_error: str | None, next_value: str
):
    return {
        "form_data": form_data,
        "errors": errors,
        "general_error": general_error,
        "next_value": next_value,
    }


@auth_bp.route("/registro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))

    if request.method == "GET":
        return render_template(
            "auth/register.html", **_build_register_context(form_data={}, errors={})
        )

    form_data = {
        "username": _normalize_text(request.form.get("username")),
        "email": _normalize_email(request.form.get("email")),
    }
    password = request.form.get("password") or ""
    confirm_password = request.form.get("confirm_password") or ""
    errors: dict[str, str] = {}

    if not form_data["username"]:
        errors["username"] = "El username es obligatorio."
    elif not USERNAME_PATTERN.fullmatch(form_data["username"]):
        errors["username"] = (
            "El username debe tener entre 3 y 30 caracteres y solo puede contener letras, números o _."
        )

    if not form_data["email"]:
        errors["email"] = "El email es obligatorio."
    elif not EMAIL_PATTERN.fullmatch(form_data["email"]):
        errors["email"] = "Introduce un email válido."

    if not password:
        errors["password"] = "La contraseña es obligatoria."
    elif len(password) < 8:
        errors["password"] = "La contraseña debe tener al menos 8 caracteres."

    if not confirm_password:
        errors["confirm_password"] = "Debes confirmar la contraseña."
    elif password != confirm_password:
        errors["confirm_password"] = "La confirmación no coincide con la contraseña."

    if not errors:
        existing_username = User.query.filter_by(username=form_data["username"]).first()
        existing_email = User.query.filter_by(email=form_data["email"]).first()

        if existing_username:
            errors["username"] = "Ese username ya está en uso."
        if existing_email:
            errors["email"] = "Ese email ya está registrado."

    if errors:
        return render_template(
            "auth/register.html", **_build_register_context(form_data=form_data, errors=errors)
        )

    try:
        user = User(username=form_data["username"], email=form_data["email"])
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), "error")
        return render_template(
            "auth/register.html", **_build_register_context(form_data=form_data, errors=errors)
        )
    except IntegrityError:
        db.session.rollback()

        if User.query.filter_by(username=form_data["username"]).first():
            errors["username"] = "Ese username ya está en uso."
        if User.query.filter_by(email=form_data["email"]).first():
            errors["email"] = "Ese email ya está registrado."

        if not errors:
            flash("No hemos podido completar el registro. Inténtalo de nuevo.", "error")

        return render_template(
            "auth/register.html", **_build_register_context(form_data=form_data, errors=errors)
        )

    flash("Tu cuenta se ha creado. Ahora puedes iniciar sesión.", "success")
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))

    if request.method == "GET":
        return render_template(
            "auth/login.html",
            **_build_login_context(
                form_data={}, errors={}, general_error=None, next_value=_resolve_next_field_value()
            ),
        )

    form_data = {
        "email": _normalize_email(request.form.get("email")),
    }
    password = request.form.get("password") or ""
    errors: dict[str, str] = {}
    general_error = None
    next_value = _resolve_next_field_value()

    if not form_data["email"]:
        errors["email"] = "El email es obligatorio."
    elif not EMAIL_PATTERN.fullmatch(form_data["email"]):
        errors["email"] = "Introduce un email válido."

    if not password:
        errors["password"] = "La contraseña es obligatoria."

    if errors:
        return render_template(
            "auth/login.html",
            **_build_login_context(
                form_data=form_data,
                errors=errors,
                general_error=general_error,
                next_value=next_value,
            ),
        )

    user = User.query.filter_by(email=form_data["email"]).first()
    if user is None or not user.check_password(password):
        general_error = "Credenciales no válidas. Verifica tus datos e inténtalo de nuevo."
        return render_template(
            "auth/login.html",
            **_build_login_context(
                form_data=form_data,
                errors=errors,
                general_error=general_error,
                next_value=next_value,
            ),
        )

    login_user(user)
    flash(f"Bienvenido de nuevo, {user.username}.", "success")
    return redirect(_resolve_next_target())


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("main_bp.home"))
