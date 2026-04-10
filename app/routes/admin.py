# Blueprint: Panel de administración
# GET /admin/resenas — Lista todas las reseñas (moderación)
# POST /admin/resenas/<id>/eliminar — Eliminar cualquier reseña
# POST /admin/actualizar-juegos — Re-seed desde API FreeToGame (cooldown 30s)
# Ver: docs/02-Estructura-y-archivos.md (sección routes/admin.py)

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.decorators import admin_required
from app.extensions import db
from app.models.game import Game
from app.models.review import Review
from seeds.seed_games import seed_games

ADMIN_REFRESH_COOLDOWN_SECONDS = 30

admin_bp = Blueprint('admin_bp', __name__)


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

    author_name = review.user.username if review.user is not None else f"usuario #{review.user_id}"
    game_title = review.game.title if review.game is not None else f"juego #{review.game_id}"

    db.session.delete(review)
    db.session.commit()

    flash(
        f"La reseña de {author_name} sobre {game_title} fue eliminada correctamente.",
        "success",
    )
    return redirect(url_for("admin_bp.reviews"))


@admin_bp.route('/admin/actualizar-juegos', methods=['POST'])
@login_required
@admin_required
def update_games():
    refresh_status = _build_refresh_status()
    if refresh_status["cooldown_active"]:
        flash(
            "Todavía no podés actualizar el catálogo. Esperá "
            f"{refresh_status['seconds_remaining']} segundos más.",
            "error",
        )
        return redirect(url_for("admin_bp.reviews"))

    summary = seed_games()
    processed = summary.get("processed", 0)
    failed = summary.get("failed", 0)

    if failed:
        flash(
            f"Actualización completada con resultados mixtos: {processed} juego(s) procesado(s) y "
            f"{failed} fallo(s).",
            "warning",
        )
    else:
        flash(
            f"Catálogo actualizado correctamente. {processed} juego(s) procesado(s) y 0 fallos.",
            "success",
        )

    return redirect(url_for("admin_bp.reviews"))
