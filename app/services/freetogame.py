# TODO: Implementar cliente HTTP para la API FreeToGame
# Encapsula las llamadas a la API externa. Maneja errores (timeout, API caída).
# Devuelve None o lista vacía en caso de error, nunca rompe la app.
# Rate limit de la API: máximo 10 req/s → usar time.sleep(0.15) entre llamadas a /game?id.
# Ver: docs/06-API-FreeToGame.md


def fetch_all_games():
    """Llama a GET /api/games y devuelve lista de diccionarios con datos básicos de cada juego.
    Retorna lista vacía en caso de error.

    Campos devueltos por la API: id, title, thumbnail, short_description, game_url,
    genre, platform, publisher, developer, release_date, freetogame_profile_url.
    """
    # TODO: Implementar llamada a la API
    # 1. GET {api_url}/games (obtener URL de current_app.config)
    # 2. Manejar excepciones: requests.RequestException, timeout (10s)
    # 3. Verificar response.status_code == 200
    # 4. Retornar response.json() o [] en caso de error
    pass


def fetch_game_detail(api_id):
    """Llama a GET /api/game?id={api_id} y devuelve diccionario con datos extendidos.
    Retorna None en caso de error.

    Campos adicionales sobre fetch_all_games: description, status,
    minimum_system_requirements (os, processor, memory, graphics, storage), screenshots.
    """
    # TODO: Implementar llamada al detalle
    # 1. GET {api_url}/game?id={api_id}
    # 2. Manejar excepciones
    # 3. Retornar response.json() o None en caso de error
    pass
