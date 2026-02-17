# TODO: Implementar decoradores personalizados para protección de rutas
# Ver: docs/02-Estructura-y-archivos.md (sección decorators.py)


def admin_required(f):
    """Decorador que verifica que el usuario actual es admin.
    Usar siempre junto con @login_required (que va primero).
    Si no es admin: flash error + redirect a home.
    """
    # TODO: Implementar verificación de admin con @wraps(f)
    pass
