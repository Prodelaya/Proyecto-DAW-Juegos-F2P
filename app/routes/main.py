from __future__ import annotations

from datetime import datetime, timedelta

from flask import Blueprint, render_template, url_for
from sqlalchemy import func

from app.extensions import db
from app.models.game import Game
from app.models.review import Review


FEATURED_LIMIT = 8
FEATURED_WINDOW_DAYS = 14


def _serialize_featured_game(game, review_count, avg_rating):
    return {
        "id": game.id,
        "title": game.title,
        "thumbnail": game.thumbnail,
        "genre": game.genre,
        "platform": game.platform,
        "short_description": game.short_description,
        "release_date": game.release_date,
        "review_count": int(review_count or 0),
        "avg_rating": float(avg_rating) if avg_rating is not None else None,
    }


def _fallback_featured_rows():
    return [
        (game, 0, None)
        for game in Game.query.order_by(
            Game.release_date.desc(), Game.title.asc()
        )
        .limit(FEATURED_LIMIT)
        .all()
    ]

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def home():
    window_start = datetime.utcnow() - timedelta(days=FEATURED_WINDOW_DAYS)

    recent_reviews = (
        db.session.query(
            Review.game_id.label("game_id"),
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .filter(Review.created_at >= window_start)
        .group_by(Review.game_id)
        .subquery()
    )

    featured_rows = (
        db.session.query(
            Game,
            recent_reviews.c.review_count,
            recent_reviews.c.avg_rating,
        )
        .join(recent_reviews, recent_reviews.c.game_id == Game.id)
        .order_by(
            recent_reviews.c.review_count.desc(),
            recent_reviews.c.avg_rating.desc(),
            Game.release_date.desc(),
            Game.title.asc(),
        )
        .limit(FEATURED_LIMIT)
        .all()
    )

    featured_fallback_message = None
    if not featured_rows:
        featured_rows = _fallback_featured_rows()
        if featured_rows:
            featured_fallback_message = (
                "Todavía no hay reseñas recientes para destacar juegos. Te mostramos los más nuevos del catálogo local."
            )

    featured_games = [
        _serialize_featured_game(game, review_count, avg_rating)
        for game, review_count, avg_rating in featured_rows
    ]

    return render_template(
        "main/home.html",
        featured_games=featured_games,
        catalog_url=url_for("games_bp.catalog"),
        featured_fallback_message=featured_fallback_message,
    )
