# Blueprint: CRUD de reseñas
# POST /juego/<game_id>/resena — Crear reseña (rating 1-5, texto 10-1000 chars)
# GET+POST /resena/<id>/editar — Editar reseña (solo autor)
# POST /resena/<id>/eliminar — Eliminar reseña propia (solo autor)
# Ver: docs/02-Estructura-y-archivos.md (sección routes/reviews.py)

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.extensions import db
from app.models.game import Game
from app.models.review import Review
from app.routes.games import build_detail_context

reviews_bp = Blueprint('reviews_bp', __name__)


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _build_form_values(rating: str | None, text: str | None) -> dict[str, str]:
    return {
        "rating": (rating or "").strip(),
        "text": text or "",
    }


def _validate_review_payload(rating_raw: str | None, text_raw: str | None):
    form_values = _build_form_values(rating_raw, text_raw)
    errors: dict[str, str] = {}
    rating: int | None = None
    normalized_text = _normalize_text(text_raw)

    if not form_values["rating"]:
        errors["rating"] = "La valoración es obligatoria."
    else:
        try:
            rating = int(form_values["rating"])
        except (TypeError, ValueError):
            errors["rating"] = "La valoración debe ser un número entero entre 1 y 5."
        else:
            if not 1 <= rating <= 5:
                errors["rating"] = "La valoración debe estar entre 1 y 5."

    if not normalized_text:
        errors["text"] = "La reseña es obligatoria."
    elif not 10 <= len(normalized_text) <= 1000:
        errors["text"] = "La reseña debe tener entre 10 y 1000 caracteres."

    form_values["text"] = text_raw or ""
    return rating, normalized_text, form_values, errors


def _render_review_form(review: Review, form_values: dict[str, str], validation_errors: dict[str, str]):
    return render_template(
        "reviews/form.html",
        game=review.game,
        review=review,
        mode="edit",
        form_values=form_values,
        validation_errors=validation_errors,
        cancel_url=url_for("games_bp.detail", id=review.game_id),
    )


def _ensure_review_owner(review: Review, action_message: str):
    if review.user_id == current_user.id:
        return None

    flash(action_message, "error")
    return redirect(url_for("games_bp.detail", id=review.game_id))


@reviews_bp.route('/juego/<int:game_id>/resena', methods=['POST'])
@login_required
def create(game_id):
    game = Game.query.get_or_404(game_id)

    rating, normalized_text, _form_values, errors = _validate_review_payload(
        request.form.get("rating"), request.form.get("text")
    )

    if errors:
        flash("No pudimos publicar tu reseña. Revisá los errores marcados y volvé a intentar.", "error")
        return render_template(
            "games/detail.html",
            **build_detail_context(
                game,
                review_form_values=_form_values,
                review_validation_errors=errors,
            ),
        ), 400

    existing_review = Review.query.filter_by(user_id=current_user.id, game_id=game.id).first()
    if existing_review is not None:
        flash("Ya tenés una reseña para este juego. Podés editarla o eliminarla abajo.", "error")
        return redirect(url_for("games_bp.detail", id=game.id))

    review = Review(
        user_id=current_user.id,
        game_id=game.id,
        rating=rating,
        text=normalized_text,
    )

    try:
        db.session.add(review)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Ya tenés una reseña para este juego. Podés editarla o eliminarla abajo.", "error")
        return redirect(url_for("games_bp.detail", id=game.id))
    except (ValueError, SQLAlchemyError):
        db.session.rollback()
        flash("No pudimos publicar tu reseña. Probá nuevamente en unos segundos.", "error")
        return redirect(url_for("games_bp.detail", id=game.id))

    flash("Tu reseña fue publicada correctamente.", "success")
    return redirect(url_for("games_bp.detail", id=game.id))


@reviews_bp.route('/resena/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def edit(id):
    review = Review.query.get_or_404(id)
    owner_redirect = _ensure_review_owner(review, "No podés editar una reseña ajena.")
    if owner_redirect is not None:
        return owner_redirect

    if request.method == 'GET':
        return _render_review_form(
            review,
            form_values=_build_form_values(str(review.rating), review.text),
            validation_errors={},
        )

    rating, normalized_text, form_values, validation_errors = _validate_review_payload(
        request.form.get("rating"), request.form.get("text")
    )
    if validation_errors:
        flash("No pudimos actualizar tu reseña. Revisá los errores marcados y volvé a intentar.", "error")
        return _render_review_form(review, form_values, validation_errors)

    try:
        review.rating = rating
        review.text = normalized_text
        db.session.commit()
    except (ValueError, SQLAlchemyError):
        db.session.rollback()
        flash("No pudimos actualizar tu reseña. Probá nuevamente en unos segundos.", "error")
        return _render_review_form(review, form_values, validation_errors)

    flash("Tu reseña fue actualizada correctamente.", "success")
    return redirect(url_for("games_bp.detail", id=review.game_id))


@reviews_bp.route('/resena/<int:id>/eliminar', methods=['POST'])
@login_required
def delete(id):
    review = Review.query.get_or_404(id)
    owner_redirect = _ensure_review_owner(review, "No podés eliminar una reseña ajena.")
    if owner_redirect is not None:
        return owner_redirect

    game_id = review.game_id

    try:
        db.session.delete(review)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("No pudimos eliminar tu reseña. Probá nuevamente en unos segundos.", "error")
        return redirect(url_for("games_bp.detail", id=game_id))

    flash("Tu reseña fue eliminada correctamente.", "success")
    return redirect(url_for("games_bp.detail", id=game_id))
