# TODO: Implementar modelo User — Tabla de usuarios
# Campos: id (PK), username (unique, 3-30 chars, alfanumérico+guiones bajos),
#   email (unique), password_hash, is_admin (default False), created_at
# Integración: UserMixin (Flask-Login), bcrypt (Flask-Bcrypt)
# Métodos: set_password(password), check_password(password)
# Relaciones: reviews (1:N → Review), library_entries (1:N → UserLibrary), ambas con cascade
# Ver: docs/02-Estructura-y-archivos.md (sección models/user.py)


class User:
    __tablename__ = 'users'
    # TODO: Definir columnas
    # TODO: Definir relaciones
    # TODO: Implementar set_password() y check_password()
    # TODO: Implementar __repr__
    pass
