# Registro centralizado de todos los blueprints.
# create_app() llama a register_routes(app) para conectar todas las rutas.
# Ver: docs/02-Estructura-y-archivos.md


def register_routes(app):
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.games import games_bp
    from app.routes.library import library_bp
    from app.routes.main import main_bp
    from app.routes.profile import profile_bp
    from app.routes.reviews import reviews_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
