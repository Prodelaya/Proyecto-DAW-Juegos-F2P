# TODO: Implementar modelo UserLibrary — Biblioteca personal de cada usuario
# Campos: id (PK), user_id (FK → users.id), game_id (FK → games.id),
#   status (String 20, default 'want_to_play'), created_at
# Valores válidos de status: 'want_to_play', 'playing', 'played'
# Constraint: UNIQUE (user_id, game_id)
# Ver: docs/02-Estructura-y-archivos.md (sección models/library.py)

VALID_STATUSES = ['want_to_play', 'playing', 'played']


class UserLibrary:
    __tablename__ = 'user_library'
    # TODO: Definir columnas
    # TODO: Definir UniqueConstraint (user_id, game_id)
    # TODO: Implementar __repr__
    pass
