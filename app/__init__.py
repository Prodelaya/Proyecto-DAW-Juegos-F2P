from pathlib import Path
from urllib.parse import urljoin, urlsplit

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError

from app.config import Config
from app.extensions import bcrypt, csrf, db, login_manager
from app.routes import register_routes


def _is_safe_local_url(target: str | None) -> bool:
    if not target:
        return False

    ref_url = urlsplit(request.host_url)
    test_url = urlsplit(urljoin(request.host_url, target))
    return test_url.scheme in {"http", "https"} and ref_url.netloc == test_url.netloc


def _resolve_safe_redirect_target() -> str:
    fallback_target = url_for("main_bp.home")
    referrer = request.referrer

    if not _is_safe_local_url(referrer):
        return fallback_target

    normalized_referrer = urlsplit(urljoin(request.host_url, referrer))
    resolved_target = normalized_referrer.path or fallback_target

    if normalized_referrer.query:
        resolved_target = f"{resolved_target}?{normalized_referrer.query}"

    if normalized_referrer.fragment:
        resolved_target = f"{resolved_target}#{normalized_referrer.fragment}"

    return resolved_target


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    import app.models as models  # noqa: F401

    with app.app_context():
        db.create_all()

    register_routes(app)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        flash(
            "Tu sesión del formulario expiró o la solicitud no era válida. Volvé a intentarlo.",
            "error",
        )
        return redirect(_resolve_safe_redirect_target())

    return app
