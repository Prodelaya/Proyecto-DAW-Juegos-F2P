# TODO: Implementar modelo Game — Caché local de juegos de la API FreeToGame
# Campos del listado (/api/games): api_id (unique), title, thumbnail, short_description,
#   game_url, genre, platform, publisher, developer, release_date, freetogame_profile_url
# Campos del detalle (/api/game?id=): description, status
# Requisitos mínimos (NULL para juegos de navegador): req_os, req_processor, req_memory,
#   req_graphics, req_storage
# Screenshots: campo Text con JSON string (lista de URLs)
# Timestamp: cached_at (DateTime, default utcnow)
# Relaciones: reviews (1:N → Review), library_entries (1:N → UserLibrary), ambas con cascade
# Ver: docs/06-API-FreeToGame.md (estrategia de uso)


class Game:
    __tablename__ = 'games'
    # TODO: Definir columnas del listado
    # TODO: Definir columnas del detalle
    # TODO: Definir columnas de requisitos mínimos
    # TODO: Definir campo screenshots (JSON)
    # TODO: Definir cached_at
    # TODO: Definir relaciones
    # TODO: Implementar __repr__
    pass
