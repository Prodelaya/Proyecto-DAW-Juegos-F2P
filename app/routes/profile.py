# Blueprint: Perfil de usuario
# GET /perfil — Datos del usuario, contadores, últimas reseñas
# Ver: docs/02-Estructura-y-archivos.md (sección routes/profile.py)

from flask import Blueprint, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app.models.library import UserLibrary
from app.models.review import Review

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/perfil')
@login_required
def index():
    review_count = Review.query.filter_by(user_id=current_user.id).count()
    library_count = UserLibrary.query.filter_by(user_id=current_user.id).count()
    recent_reviews = (
        Review.query.options(joinedload(Review.game))
        .filter_by(user_id=current_user.id)
        .order_by(Review.updated_at.desc(), Review.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "profile/index.html",
        user=current_user,
        stats={
            "review_count": review_count,
            "library_count": library_count,
        },
        recent_reviews=recent_reviews,
        links={
            "catalog": url_for("games_bp.catalog"),
            "library": url_for("library_bp.my_library"),
        },
    )
