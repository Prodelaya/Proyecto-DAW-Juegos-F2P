# Seed de usuarios — Crea 1 admin (datos del .env) + 5 usuarios demo.
# Verifica existencia antes de crear (idempotente).
# Ver: docs/02-Estructura-y-archivos.md (sección seeds/seed_users.py)

# Usuarios demo con datos de prueba
DEMO_USERS = [
    {'username': 'gamer_ana', 'email': 'ana@demo.com', 'password': 'demo1234'},
    {'username': 'pixel_pedro', 'email': 'pedro@demo.com', 'password': 'demo1234'},
    {'username': 'noob_lucia', 'email': 'lucia@demo.com', 'password': 'demo1234'},
    {'username': 'pro_carlos', 'email': 'carlos@demo.com', 'password': 'demo1234'},
    {'username': 'indie_maria', 'email': 'maria@demo.com', 'password': 'demo1234'},
]


def seed_users():
    """Crea usuarios demo + admin. Retorna el número de usuarios creados."""
    # TODO: Implementar seed de usuarios
    # 1. Crear admin con ADMIN_EMAIL y ADMIN_PASSWORD del .env, is_admin=True
    # 2. Crear 5 usuarios demo con passwords simples (datos de DEMO_USERS)
    # 3. Verificar si ya existen antes de crear (idempotente)
    # 4. db.session.commit()
    # 5. Retornar conteo de usuarios creados
    pass
