# Blueprint: Biblioteca personal del usuario
# GET /mi-biblioteca — Lista juegos del usuario con filtro por estado
# POST /biblioteca/agregar/<game_id> — Añadir juego (status 'want_to_play')
# POST /biblioteca/estado/<id> — Cambiar estado
# POST /biblioteca/quitar/<id> — Quitar de biblioteca
# Ver: docs/02-Estructura-y-archivos.md (sección routes/library.py)

from __future__ import annotations

from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.game import Game
from app.models.library import VALID_STATUSES, UserLibrary

library_bp = Blueprint('library_bp', __name__)


def _safe_return_url(candidate: str | None) -> str:
    fallback = url_for("library_bp.my_library")
    normalized_candidate = (candidate or "").strip()

    if not normalized_candidate:
        return fallback

    parsed_candidate = urlsplit(normalized_candidate)
    if parsed_candidate.scheme or parsed_candidate.netloc:
        return fallback

    if not normalized_candidate.startswith("/") or normalized_candidate.startswith("//"):
        return fallback

    return normalized_candidate


def _get_owned_entry_or_redirect(entry_id: int):
    entry = UserLibrary.query.options(joinedload(UserLibrary.game)).get_or_404(entry_id)
    if entry.user_id == current_user.id:
        return entry, None

    flash("No podés gestionar una entrada de biblioteca ajena.", "error")
    return None, redirect(url_for("library_bp.my_library"))


@library_bp.route('/mi-biblioteca')
@login_required
def my_library():
    current_status = (request.args.get("status") or "").strip()
    if current_status and current_status not in VALID_STATUSES:
        flash("El filtro de estado solicitado no es válido.", "error")
        return redirect(url_for("library_bp.my_library"))

    query = UserLibrary.query.options(joinedload(UserLibrary.game)).filter_by(user_id=current_user.id)

    if current_status:
        query = query.filter_by(status=current_status)

    entries = query.order_by(UserLibrary.created_at.desc(), UserLibrary.id.desc()).all()

    return render_template(
        "library/my_library.html",
        entries=entries,
        current_status=current_status,
        available_statuses=VALID_STATUSES,
        has_results=bool(entries),
    )


@library_bp.route('/biblioteca/agregar/<int:game_id>', methods=['POST'])
@login_required
def add(game_id):
    game = Game.query.get_or_404(game_id)

    existing_entry = UserLibrary.query.filter_by(user_id=current_user.id, game_id=game.id).first()
    if existing_entry is not None:
        flash("Ese juego ya está en tu biblioteca.", "error")
        return redirect(url_for("games_bp.detail", id=game.id))

    entry = UserLibrary(user_id=current_user.id, game_id=game.id, status="want_to_play")
    db.session.add(entry)
    db.session.commit()

    flash("El juego se agregó a tu biblioteca en “Quiero jugar”.", "success")
    return redirect(url_for("games_bp.detail", id=game.id))


@library_bp.route('/biblioteca/estado/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    entry, redirect_response = _get_owned_entry_or_redirect(id)
    if redirect_response is not None:
        return redirect_response

    next_url = _safe_return_url(request.form.get("next"))
    new_status = (request.form.get("status") or "").strip()
    if new_status not in VALID_STATUSES:
        flash("El estado enviado no es válido. Usá want_to_play, playing o played.", "error")
        return redirect(next_url)

    entry.status = new_status
    db.session.commit()

    flash("El estado de tu biblioteca fue actualizado correctamente.", "success")
    return redirect(next_url)


@library_bp.route('/biblioteca/quitar/<int:id>', methods=['POST'])
@login_required
def remove(id):
    entry, redirect_response = _get_owned_entry_or_redirect(id)
    if redirect_response is not None:
        return redirect_response

    next_url = _safe_return_url(request.form.get("next"))
    game_title = entry.game.title if entry.game is not None else "El juego"

    db.session.delete(entry)
    db.session.commit()

    flash(f"{game_title} fue quitado de tu biblioteca.", "success")
    return redirect(next_url)
