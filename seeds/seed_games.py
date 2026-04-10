from __future__ import annotations

import time
from datetime import datetime

from flask import current_app

from app.extensions import db
from app.models.game import Game
from app.services.freetogame import fetch_all_games, fetch_game_detail


DETAIL_RATE_LIMIT_SECONDS = 0.15
DEFAULT_DESCRIPTION = "Descripción no disponible por el momento."


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


def seed_games() -> dict[str, int]:
    """Cachea todos los juegos de la API en la base local de forma idempotente."""
    games_payload = fetch_all_games()
    if not games_payload:
        return {"processed": 0, "failed": 0}

    summary = {"processed": 0, "failed": 0}

    for game_summary in games_payload:
        api_id = game_summary.get("id")
        if api_id is None:
            summary["failed"] += 1
            continue

        detail = fetch_game_detail(api_id)
        requirements = detail.get("minimum_system_requirements", {}) if detail else {}

        try:
            game = Game.query.filter_by(api_id=api_id).first()
            if game is None:
                game = Game(
                    api_id=api_id,
                    title=game_summary.get("title") or f"Juego {api_id}",
                    description=(
                        (detail or {}).get("description")
                        or game_summary.get("short_description")
                        or DEFAULT_DESCRIPTION
                    ),
                )
                db.session.add(game)

            game.title = game_summary.get("title") or game.title
            game.thumbnail = game_summary.get("thumbnail")
            game.short_description = game_summary.get("short_description")
            game.game_url = game_summary.get("game_url")
            game.genre = game_summary.get("genre")
            game.platform = game_summary.get("platform")
            game.publisher = game_summary.get("publisher")
            game.developer = game_summary.get("developer")
            game.release_date = _normalize_release_date(game_summary.get("release_date"))
            game.freetogame_profile_url = game_summary.get("freetogame_profile_url")

            if detail:
                game.description = (
                    detail.get("description")
                    or game_summary.get("short_description")
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
                    or game_summary.get("short_description")
                    or DEFAULT_DESCRIPTION
                )
                game.screenshots = game.screenshots or []

            game.cached_at = datetime.utcnow()

            db.session.commit()
            summary["processed"] += 1
        except Exception as exc:  # pragma: no cover - robustez del seed manual
            db.session.rollback()
            summary["failed"] += 1
            current_app.logger.error(
                "No se pudo seedear el juego api_id=%s: %s", api_id, exc
            )
        finally:
            time.sleep(DETAIL_RATE_LIMIT_SECONDS)

    return summary
