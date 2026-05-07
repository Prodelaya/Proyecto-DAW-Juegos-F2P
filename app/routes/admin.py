# Blueprint: Panel de administración
# GET /admin/resenas — Lista todas las reseñas (moderación)
# POST /admin/resenas/<id>/eliminar — Eliminar cualquier reseña
# POST /admin/actualizar-juegos — Re-seed desde API FreeToGame (cooldown 30s)
# Ver: docs/02-Estructura-y-archivos.md (sección routes/admin.py)

from __future__ import annotations

from datetime import datetime

from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.decorators import admin_required
from app.extensions import db
from app.models.game import Game
from app.models.review import Review
from seeds.seed_games import seed_games

ADMIN_REFRESH_COOLDOWN_SECONDS = 30

admin_bp = Blueprint('admin_bp', __name__)


def _safe_admin_return_url(candidate: str | None) -> str:
    fallback = url_for("admin_bp.reviews")
    normalized_candidate = (candidate or "").strip()

    if not normalized_candidate:
        return fallback

    parsed_candidate = urlsplit(normalized_candidate)
    if parsed_candidate.scheme or parsed_candidate.netloc:
        return fallback

    if not normalized_candidate.startswith("/") or normalized_candidate.startswith("//"):
        return fallback

    return normalized_candidate


def _build_refresh_status() -> dict[str, int | bool | datetime | None]:
    last_cached_at = db.session.query(func.max(Game.cached_at)).scalar()
    if last_cached_at is None:
        return {
            "cooldown_active": False,
            "seconds_remaining": 0,
            "last_cached_at": None,
            "cooldown_seconds": ADMIN_REFRESH_COOLDOWN_SECONDS,
        }

    elapsed_seconds = int((datetime.utcnow() - last_cached_at).total_seconds())
    seconds_remaining = max(ADMIN_REFRESH_COOLDOWN_SECONDS - elapsed_seconds, 0)

    return {
        "cooldown_active": seconds_remaining > 0,
        "seconds_remaining": seconds_remaining,
        "last_cached_at": last_cached_at,
        "cooldown_seconds": ADMIN_REFRESH_COOLDOWN_SECONDS,
    }


@admin_bp.route('/admin/resenas')
@login_required
@admin_required
def reviews():
    reviews_list = (
        Review.query.options(joinedload(Review.user), joinedload(Review.game))
        .order_by(Review.updated_at.desc(), Review.created_at.desc(), Review.id.desc())
        .all()
    )

    return render_template(
        "admin/reviews.html",
        reviews=reviews_list,
        has_results=bool(reviews_list),
        refresh_status=_build_refresh_status(),
    )


@admin_bp.route('/admin/resenas/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_review(id):
    review = Review.query.options(joinedload(Review.user), joinedload(Review.game)).get_or_404(id)
    next_url = _safe_admin_return_url(request.form.get("next"))

    author_name = review.user.username if review.user is not None else f"usuario #{review.user_id}"
    game_title = review.game.title if review.game is not None else f"juego #{review.game_id}"

    try:
        db.session.delete(review)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("No hemos podido eliminar la reseña seleccionada. Inténtalo de nuevo.", "error")
        return redirect(next_url)

    flash(
        f"La reseña de {author_name} sobre {game_title} fue eliminada correctamente.",
        "success",
    )
    return redirect(next_url)


@admin_bp.route('/admin/actualizar-juegos', methods=['POST'])
@login_required
@admin_required
def update_games():
    refresh_status = _build_refresh_status()
    if refresh_status["cooldown_active"]:
        flash(
            "Todavía no puedes actualizar el catálogo. Espera "
            f"{refresh_status['seconds_remaining']} segundos más.",
            "error",
        )
        return redirect(url_for("admin_bp.reviews"))

    try:
        summary = seed_games()
    except Exception:
        db.session.rollback()
        flash("No hemos podido actualizar el catálogo en este momento. Inténtalo de nuevo.", "error")
        return redirect(url_for("admin_bp.reviews"))

    reviewed = summary.get("reviewed", 0)
    created = summary.get("created", 0)
    updated = summary.get("updated", 0)
    unchanged = summary.get("unchanged", 0)
    failed = summary.get("failed", 0)
    processed = summary.get("processed", created + updated)

    if failed:
        flash(
            "Catálogo revisado correctamente. "
            f"{reviewed} revisado(s), {created} nuevo(s), {updated} actualizado(s), "
            f"{unchanged} sin cambios y {failed} fallo(s). "
            f"(Procesados: {processed})",
            "warning",
        )
    else:
        flash(
            "Catálogo revisado correctamente. "
            f"{reviewed} revisado(s), {created} nuevo(s), {updated} actualizado(s), "
            f"{unchanged} sin cambios y {failed} fallo(s). "
            f"(Procesados: {processed})",
            "success",
        )

    return redirect(url_for("admin_bp.reviews"))
