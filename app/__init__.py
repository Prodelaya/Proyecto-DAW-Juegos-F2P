# TODO: Implementar Application Factory completo
# Patrón: create_app() carga config, inicializa extensiones, registra blueprints y error handlers.
# 1. Crear instancia Flask
# 2. Cargar Config desde app.config
# 3. Inicializar extensiones: db, login_manager, bcrypt, csrf
# 4. Registrar blueprints vía register_routes(app)
# 5. Registrar error handlers (404, 500) renderizando templates de errors/
# 6. Crear tablas con db.create_all() dentro de app_context (sin migraciones — MVP)
# Ver: docs/01-Arquitectura.md §7 (Mapa de dependencias)

from flask import Flask


def create_app():
    # TODO: Implementar application factory
    pass
