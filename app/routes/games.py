from __future__ import annotations

from flask import Blueprint, render_template, request
from sqlalchemy import case, func, or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.game import Game
from app.models.review import Review


CATALOG_PER_PAGE = 20
ALLOWED_SORTS = {
    "alphabetical": "alphabetical",
    "review_count": "review_count",
    "avg_rating": "avg_rating",
    "release_date": "release_date",
}


def _sanitize_text_filter(value: str | None) -> str:
    return (value or "").strip()


def _sanitize_page(value: str | None) -> int:
    try:
        return max(int(value or 1), 1)
    except (TypeError, ValueError):
        return 1


def _sanitize_sort(value: str | None) -> str:
    normalized = _sanitize_text_filter(value).lower()
    return ALLOWED_SORTS.get(normalized, "alphabetical")


def _review_aggregates_subquery():
    return (
        db.session.query(
            Review.game_id.label("game_id"),
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .group_by(Review.game_id)
        .subquery()
    )


def _serialize_catalog_game(game, review_count, avg_rating):
    return {
        "id": game.id,
        "title": game.title,
        "thumbnail": game.thumbnail,
        "genre": game.genre,
        "platform": game.platform,
        "publisher": game.publisher,
        "short_description": game.short_description,
        "release_date": game.release_date,
        "review_count": int(review_count or 0),
        "avg_rating": float(avg_rating) if avg_rating is not None else None,
    }


def _distinct_field_values(column):
    rows = (
        db.session.query(column)
        .filter(column.isnot(None), column != "")
        .distinct()
        .order_by(column.asc())
        .all()
    )
    return [value for value, in rows]

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/catalogo')
def catalog():
    current_filters = {
        "q": _sanitize_text_filter(request.args.get("q")),
        "genre": _sanitize_text_filter(request.args.get("genre")),
        "platform": _sanitize_text_filter(request.args.get("platform")),
        "publisher": _sanitize_text_filter(request.args.get("publisher")),
        "sort": _sanitize_sort(request.args.get("sort")),
        "page": _sanitize_page(request.args.get("page")),
    }

    review_aggregates = _review_aggregates_subquery()
    query = db.session.query(
        Game,
        review_aggregates.c.review_count,
        review_aggregates.c.avg_rating,
    ).outerjoin(review_aggregates, review_aggregates.c.game_id == Game.id)

    if current_filters["q"]:
        search_term = f"%{current_filters['q']}%"
        query = query.filter(
            or_(
                Game.title.ilike(search_term),
                Game.short_description.ilike(search_term),
            )
        )

    if current_filters["genre"]:
        query = query.filter(Game.genre == current_filters["genre"])

    if current_filters["platform"]:
        query = query.filter(Game.platform == current_filters["platform"])

    if current_filters["publisher"]:
        query = query.filter(Game.publisher == current_filters["publisher"])

    nulls_last = case((review_aggregates.c.review_count.is_(None), 1), else_=0)
    rating_nulls_last = case((review_aggregates.c.avg_rating.is_(None), 1), else_=0)

    if current_filters["sort"] == "review_count":
        query = query.order_by(
            nulls_last.asc(),
            review_aggregates.c.review_count.desc(),
            Game.release_date.desc(),
            Game.title.asc(),
        )
    elif current_filters["sort"] == "avg_rating":
        query = query.order_by(
            rating_nulls_last.asc(),
            review_aggregates.c.avg_rating.desc(),
            Game.release_date.desc(),
            Game.title.asc(),
        )
    elif current_filters["sort"] == "release_date":
        query = query.order_by(Game.release_date.desc(), Game.title.asc())
    else:
        query = query.order_by(Game.title.asc(), Game.release_date.desc())

    pagination = query.paginate(
        page=current_filters["page"], per_page=CATALOG_PER_PAGE, error_out=False
    )

    games = [
        _serialize_catalog_game(game, review_count, avg_rating)
        for game, review_count, avg_rating in pagination.items
    ]
    filter_options = {
        "genres": _distinct_field_values(Game.genre),
        "platforms": _distinct_field_values(Game.platform),
        "publishers": _distinct_field_values(Game.publisher),
    }

    return render_template(
        "games/catalog.html",
        games=games,
        pagination=pagination,
        current_filters=current_filters,
        filter_options=filter_options,
        total_count=pagination.total,
        has_results=pagination.total > 0,
    )


@games_bp.route('/juego/<int:id>')
def detail(id):
    game = Game.query.get_or_404(id)

    review_count, avg_rating = (
        db.session.query(func.count(Review.id), func.avg(Review.rating))
        .filter(Review.game_id == game.id)
        .one()
    )

    reviews = (
        Review.query.options(joinedload(Review.user))
        .filter(Review.game_id == game.id)
        .order_by(Review.created_at.desc())
        .all()
    )

    screenshots = [
        screenshot.strip()
        for screenshot in (game.screenshots or [])
        if isinstance(screenshot, str) and screenshot.strip()
    ]
    requirements = {
        "os": game.req_os,
        "processor": game.req_processor,
        "memory": game.req_memory,
        "graphics": game.req_graphics,
        "storage": game.req_storage,
    }
    has_requirements = any(requirements.values())

    return render_template(
        "games/detail.html",
        game=game,
        reviews=reviews,
        review_summary={
            "count": int(review_count or 0),
            "avg_rating": float(avg_rating) if avg_rating is not None else None,
        },
        screenshots=screenshots,
        requirements=requirements,
        has_requirements=has_requirements,
    )
