# TODO: Implementar modelo Review — Reseñas de usuarios sobre juegos
# Campos: id (PK), user_id (FK → users.id), game_id (FK → games.id),
#   rating (Integer, 1-5), text (String 1000, 10-1000 chars),
#   created_at, updated_at (con onupdate)
# Constraint: UNIQUE (user_id, game_id) — un usuario solo puede escribir una reseña por juego
# Ver: docs/02-Estructura-y-archivos.md (sección models/review.py)


class Review:
    __tablename__ = 'reviews'
    # TODO: Definir columnas
    # TODO: Definir UniqueConstraint (user_id, game_id)
    # TODO: Implementar __repr__
    pass
