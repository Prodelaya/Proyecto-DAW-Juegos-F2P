from __future__ import annotations

import time
from typing import Any

import requests
from flask import current_app


REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1


def _build_url(path: str) -> str:
    base_url = current_app.config["FREETOGAME_API_URL"].rstrip("/")
    return f"{base_url}/{path.lstrip('/')}"


def _request_json(path: str, *, params: dict[str, Any] | None = None) -> Any | None:
    url = _build_url(path)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            if attempt == MAX_RETRIES:
                current_app.logger.error(
                    "FreeToGame request failed after %s attempts: %s params=%s error=%s",
                    MAX_RETRIES,
                    url,
                    params,
                    exc,
                )
            else:
                current_app.logger.warning(
                    "FreeToGame request failed (attempt %s/%s): %s params=%s error=%s",
                    attempt,
                    MAX_RETRIES,
                    url,
                    params,
                    exc,
                )
                time.sleep(RETRY_DELAY_SECONDS)

    return None


def fetch_all_games() -> list[dict[str, Any]]:
    """Obtiene el listado básico de juegos para seed/refresh manual."""
    payload = _request_json("games")
    if not isinstance(payload, list):
        current_app.logger.error("FreeToGame devolvió un listado inválido para /games")
        return []

    return payload


def fetch_game_detail(api_id: int) -> dict[str, Any] | None:
    """Obtiene el detalle de un juego para seed/refresh manual."""
    payload = _request_json("game", params={"id": api_id})
    if not isinstance(payload, dict):
        current_app.logger.error(
            "FreeToGame devolvió un detalle inválido para game id=%s", api_id
        )
        return None

    return payload
