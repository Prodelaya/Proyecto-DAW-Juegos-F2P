# TODO: Implementar decoradores personalizados para protección de rutas
# Ver: docs/02-Estructura-y-archivos.md (sección decorators.py)

from functools import wraps

from flask import flash, redirect, request, url_for
from flask_login import current_user


def admin_required(f):
    """Decorador que verifica que el usuario actual es admin.
    Usar siempre junto con @login_required (que va primero).
    Si no es admin: flash error + redirect a home.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            next_target = request.full_path if request.query_string else request.path
            return redirect(url_for("auth_bp.login", next=next_target))

        if not getattr(current_user, "is_admin", False):
            flash("No tenés permisos para acceder a esa sección.", "error")
            return redirect(url_for("main_bp.home"))

        return f(*args, **kwargs)

    return decorated_function
