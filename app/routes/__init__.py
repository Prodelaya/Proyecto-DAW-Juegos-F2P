# Registro centralizado de todos los blueprints.
# create_app() llama a register_routes(app) para conectar todas las rutas.
# Ver: docs/02-Estructura-y-archivos.md


def register_routes(app):
    from app.routes.games import games_bp
    from app.routes.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(games_bp)
