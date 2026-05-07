from __future__ import annotations

import time
from datetime import datetime

from flask import current_app

from app.extensions import db
from app.models.game import Game
from app.services.freetogame import fetch_all_games, fetch_game_detail


DETAIL_RATE_LIMIT_SECONDS = 0.15
DEFAULT_DESCRIPTION = "Descripción no disponible por el momento."
REQUIRED_DETAIL_FIELDS = ("status", "req_os", "req_processor", "req_memory", "req_graphics", "req_storage")


def _normalize_release_date(value: str | None) -> str | None:
    if not value:
        return None

    normalized_value = value.strip()
    if not normalized_value:
        return None

    try:
        return datetime.strptime(normalized_value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return normalized_value


def _normalize_screenshots(raw_screenshots) -> list[str]:
    if not isinstance(raw_screenshots, list):
        return []

    screenshots: list[str] = []
    for screenshot in raw_screenshots:
        if isinstance(screenshot, dict):
            image_url = (screenshot.get("image") or "").strip()
            if image_url:
                screenshots.append(image_url)
        elif isinstance(screenshot, str) and screenshot.strip():
            screenshots.append(screenshot.strip())

    return screenshots


def _normalize_basic_fields(game_summary: dict) -> dict[str, str | None]:
    return {
        "title": game_summary.get("title") or None,
        "thumbnail": game_summary.get("thumbnail") or None,
        "short_description": game_summary.get("short_description") or None,
        "game_url": game_summary.get("game_url") or None,
        "genre": game_summary.get("genre") or None,
        "platform": game_summary.get("platform") or None,
        "publisher": game_summary.get("publisher") or None,
        "developer": game_summary.get("developer") or None,
        "release_date": _normalize_release_date(game_summary.get("release_date")),
        "freetogame_profile_url": game_summary.get("freetogame_profile_url") or None,
    }


def _has_basic_changes(game: Game, basic_fields: dict[str, str | None]) -> bool:
    return any(getattr(game, field_name) != value for field_name, value in basic_fields.items())


def _has_complete_local_detail(game: Game) -> bool:
    has_valid_description = bool(game.description and game.description.strip() and game.description.strip() != DEFAULT_DESCRIPTION)
    has_screenshots = isinstance(game.screenshots, list) and len(game.screenshots) > 0
    has_requirements = any(getattr(game, field_name) for field_name in REQUIRED_DETAIL_FIELDS)
    return has_valid_description and has_screenshots and has_requirements


def seed_games() -> dict[str, int]:
    """Cachea todos los juegos de la API en la base local de forma idempotente."""
    games_payload = fetch_all_games()
    if not games_payload:
        return {
            "reviewed": 0,
            "created": 0,
            "updated": 0,
            "unchanged": 0,
            "failed": 0,
            "processed": 0,
        }

    summary = {
        "reviewed": 0,
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "failed": 0,
        "processed": 0,
    }

    for game_summary in games_payload:
        summary["reviewed"] += 1
        api_id = game_summary.get("id")
        if api_id is None:
            summary["failed"] += 1
            continue

        try:
            game = Game.query.filter_by(api_id=api_id).first()
            basic_fields = _normalize_basic_fields(game_summary)
            is_new_game = game is None

            needs_detail = is_new_game
            if not needs_detail and game is not None:
                needs_detail = _has_basic_changes(game, basic_fields) or not _has_complete_local_detail(game)

            detail = None
            requirements = {}
            if needs_detail:
                detail = fetch_game_detail(api_id)
                requirements = detail.get("minimum_system_requirements", {}) if detail else {}
                time.sleep(DETAIL_RATE_LIMIT_SECONDS)

            if is_new_game:
                game = Game(
                    api_id=api_id,
                    title=basic_fields.get("title") or f"Juego {api_id}",
                    description=(
                        (detail or {}).get("description")
                        or basic_fields.get("short_description")
                        or DEFAULT_DESCRIPTION
                    ),
                )
                db.session.add(game)

            if not needs_detail and game is not None:
                summary["unchanged"] += 1
                continue

            game.title = basic_fields.get("title") or game.title
            game.thumbnail = basic_fields.get("thumbnail")
            game.short_description = basic_fields.get("short_description")
            game.game_url = basic_fields.get("game_url")
            game.genre = basic_fields.get("genre")
            game.platform = basic_fields.get("platform")
            game.publisher = basic_fields.get("publisher")
            game.developer = basic_fields.get("developer")
            game.release_date = basic_fields.get("release_date")
            game.freetogame_profile_url = basic_fields.get("freetogame_profile_url")

            if detail:
                game.description = (
                    detail.get("description")
                    or basic_fields.get("short_description")
                    or game.description
                    or DEFAULT_DESCRIPTION
                )
                game.status = detail.get("status")
                game.req_os = requirements.get("os")
                game.req_processor = requirements.get("processor")
                game.req_memory = requirements.get("memory")
                game.req_graphics = requirements.get("graphics")
                game.req_storage = requirements.get("storage")
                game.screenshots = _normalize_screenshots(detail.get("screenshots"))
            else:
                game.description = (
                    game.description
                    or basic_fields.get("short_description")
                    or DEFAULT_DESCRIPTION
                )
                game.screenshots = game.screenshots or []

            game.cached_at = datetime.utcnow()

            db.session.commit()
            if is_new_game:
                summary["created"] += 1
            else:
                summary["updated"] += 1
            summary["processed"] = summary["created"] + summary["updated"]
        except Exception as exc:  # pragma: no cover - robustez del seed manual
            db.session.rollback()
            summary["failed"] += 1
            current_app.logger.error(
                "No se pudo seedear el juego api_id=%s: %s", api_id, exc
            )

    return summary
