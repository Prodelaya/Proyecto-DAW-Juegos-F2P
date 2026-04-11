from __future__ import annotations

import random
from datetime import datetime, timedelta

from flask import current_app

from app.extensions import db
from app.models.game import Game
from app.models.review import Review
from app.models.user import User

# Frases variadas para reseñas de ejemplo
REVIEW_TEXTS = [
    'Gran juego para pasar el rato, lo recomiendo.',
    'Los gráficos podrían mejorar pero el gameplay es sólido.',
    'Demasiado pay-to-win para mi gusto.',
    'Lo recomiendo al 100%, llevo más de 200 horas.',
    'Está bien para ser gratuito, nada del otro mundo.',
    'Me enganchó desde el primer momento, no puedo parar de jugar.',
    'La comunidad es muy tóxica, pero el juego en sí está genial.',
    'Buen juego casual para jugar en ratos libres.',
    'El mejor free-to-play que he probado este año.',
    'Se nota que los desarrolladores se esfuerzan con las actualizaciones.',
    'Bastante repetitivo después de unas horas.',
    'La historia es sorprendentemente buena para un juego gratuito.',
    'Perfecto para jugar con amigos, en solitario aburre un poco.',
    'Los controles son fluidos y el rendimiento es excelente.',
    'Necesita más contenido pero tiene una base muy sólida.',
    'Me sorprendió gratamente, no esperaba tanto de un F2P.',
    'Regular, hay opciones mejores en el mismo género.',
    'Adictivo y divertido, ideal para sesiones cortas.',
    'El sistema de progresión está bien diseñado.',
    'Buena propuesta, aunque le faltan modos de juego.',
]

# Distribución de ratings (más 3s y 4s, menos 1s y 5s)
RATING_WEIGHTS = [1, 2, 3, 3, 2]  # pesos para ratings 1, 2, 3, 4, 5


def seed_reviews() -> dict[str, int]:
    """Genera reseñas demo recientes e idempotentes para soportar la lectura pública."""
    demo_users = User.query.filter_by(is_admin=False).order_by(User.id.asc()).all()
    candidate_games = Game.query.order_by(Game.release_date.desc(), Game.id.asc()).limit(24).all()

    if not demo_users or not candidate_games:
        return {"processed": 0, "failed": 0}

    rng = random.Random(20260407)
    summary = {"processed": 0, "failed": 0}
    now = datetime.utcnow()

    for user_index, user in enumerate(demo_users):
        start_index = (user_index * 3) % len(candidate_games)
        assigned_games = [
            candidate_games[(start_index + offset) % len(candidate_games)]
            for offset in range(10)
        ]

        for position, game in enumerate(assigned_games):
            rating = rng.choices([1, 2, 3, 4, 5], weights=RATING_WEIGHTS, k=1)[0]
            text = REVIEW_TEXTS[(user_index * len(assigned_games) + position) % len(REVIEW_TEXTS)]
            created_at = now - timedelta(
                days=(user_index + position) % 12,
                hours=(position * 3) % 24,
                minutes=(user_index * 11 + position * 7) % 60,
            )

            try:
                review = Review.query.filter_by(user_id=user.id, game_id=game.id).first()

                if review is None:
                    review = Review(
                        user_id=user.id,
                        game_id=game.id,
                        rating=rating,
                        text=text,
                        created_at=created_at,
                        updated_at=created_at,
                    )
                    db.session.add(review)
                else:
                    review.rating = rating
                    review.text = text
                    review.created_at = created_at
                    review.updated_at = created_at

                db.session.commit()
                summary["processed"] += 1
            except Exception as exc:  # pragma: no cover - robustez del seed manual
                db.session.rollback()
                summary["failed"] += 1
                current_app.logger.error(
                    "No se pudo seedear la reseña user_id=%s game_id=%s: %s",
                    user.id,
                    game.id,
                    exc,
                )

    return summary
