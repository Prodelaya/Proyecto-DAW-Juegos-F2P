from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from app import create_app
from app.extensions import db
from seeds.seed_games import seed_games
from seeds.seed_library import seed_library
from seeds.seed_reviews import seed_reviews
from seeds.seed_users import seed_users


def _format_seed_result(result):
    if isinstance(result, dict):
        processed = int(result.get("processed", 0))
        failed = int(result.get("failed", 0))
        return f"processed={processed}, failed={failed}"

    return str(result)


def _run_seed_step(label, callback):
    try:
        result = callback()
        print(f"{label}: OK ({_format_seed_result(result)})")
        return result
    except Exception as exc:  # pragma: no cover - flujo manual de seed
        db.session.rollback()
        print(f"{label}: ERROR ({exc})")
        return {"processed": 0, "failed": 1}


def seed_all():
    app = create_app()

    with app.app_context():
        games_result = _run_seed_step("Juegos cacheados", seed_games)
        users_count = _run_seed_step("Usuarios demo", seed_users)
        reviews_count = _run_seed_step("Reseñas demo", seed_reviews)
        library_count = _run_seed_step("Biblioteca demo", seed_library)

        print(
            "Resumen seed -> "
            f"juegos: {_format_seed_result(games_result)}, "
            f"usuarios: {users_count}, reseñas: {reviews_count}, biblioteca: {library_count}"
        )


if __name__ == '__main__':
    seed_all()
