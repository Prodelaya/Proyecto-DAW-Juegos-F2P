# Seed de juegos — Cachea juegos de la API FreeToGame en la BD local.
# Llama a fetch_all_games() para el listado y fetch_game_detail() para los detalles extendidos.
# INSERT si no existe (por api_id), UPDATE si ya existe. Actualiza cached_at.
# Rate limit: time.sleep(0.15) entre llamadas al detalle (~400 juegos, ~60-90s total).
# Ver: docs/06-API-FreeToGame.md (estrategia de uso)


def seed_games():
    """Cachea todos los juegos de la API. Retorna el número de juegos procesados."""
    # TODO: Implementar seed de juegos
    # 1. Llamar a fetch_all_games() para obtener listado básico (~400 juegos)
    # 2. Para cada juego del listado:
    #    a. Buscar en BD por api_id
    #    b. Si no existe, crear nuevo Game; si existe, actualizar campos
    #    c. Mapear campos: api_id ← id, resto 1:1
    #    d. Llamar a fetch_game_detail(api_id) para obtener description, status,
    #       minimum_system_requirements, screenshots
    #    e. Mapear campos extendidos: req_os, req_processor, req_memory, req_graphics,
    #       req_storage (desde minimum_system_requirements, pueden ser NULL)
    #    f. screenshots: serializar como JSON string (lista de URLs)
    #    g. Actualizar cached_at
    #    h. time.sleep(0.15) entre llamadas al detalle
    # 3. db.session.commit()
    # 4. Retornar conteo
    pass
