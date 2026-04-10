from __future__ import annotations

from app.extensions import db
from app.models.game import Game
from app.models.library import UserLibrary, VALID_STATUSES
from app.models.user import User


ENTRIES_PER_USER = 6


def _build_status_sequence(user_index: int) -> list[str]:
    statuses = list(VALID_STATUSES)
    rotation = user_index % len(statuses)
    rotated = statuses[rotation:] + statuses[:rotation]
    return [rotated[offset % len(rotated)] for offset in range(ENTRIES_PER_USER)]


def seed_library() -> int:
    """Genera biblioteca demo idempotente y variada para usuarios no admin."""
    demo_users = User.query.filter_by(is_admin=False).order_by(User.id.asc()).all()
    candidate_games = Game.query.order_by(Game.release_date.desc(), Game.id.asc()).limit(24).all()

    if not demo_users or not candidate_games:
        return 0

    created_or_updated = 0

    for user_index, user in enumerate(demo_users):
        start_index = (user_index * 4) % len(candidate_games)
        assigned_games = [
            candidate_games[(start_index + offset) % len(candidate_games)]
            for offset in range(ENTRIES_PER_USER)
        ]
        status_sequence = _build_status_sequence(user_index)

        for game, status in zip(assigned_games, status_sequence, strict=False):
            entry = UserLibrary.query.filter_by(user_id=user.id, game_id=game.id).first()

            if entry is None:
                entry = UserLibrary(user_id=user.id, game_id=game.id, status=status)
                db.session.add(entry)
            else:
                entry.status = status

            created_or_updated += 1

    db.session.commit()
    return created_or_updated
