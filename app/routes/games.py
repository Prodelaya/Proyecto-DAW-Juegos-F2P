# Blueprint: Catálogo y ficha de juego
# GET /catalogo — Filtro, búsqueda, ordenación, paginación (20/página, default A-Z)
# GET /juego/<id> — Ficha de juego con reseñas y nota media
# Ver: docs/02-Estructura-y-archivos.md (sección routes/games.py)

from flask import Blueprint

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/catalogo')
def catalog():
    # TODO: Implementar catálogo con filtros y paginación
    # Query params: genre, platform, sort (alpha/popularity), q (búsqueda), page
    # 1. Construir query base: Game.query
    # 2. Aplicar filtros encadenados (.filter_by o .filter)
    # 3. Aplicar búsqueda con .filter(Game.title.ilike(f'%{q}%'))
    # 4. Aplicar ordenación (default: Game.title.asc())
    # 5. Paginar con .paginate(page=page, per_page=20)
    # 6. Obtener listas de géneros y plataformas únicos para los selects
    # 7. Renderizar catalog.html con: games, genres, platforms, filtros actuales, paginación
    pass


@games_bp.route('/juego/<int:id>')
def detail(id):
    # TODO: Implementar ficha de juego
    # 1. Obtener juego por ID o 404
    # 2. Calcular nota media de reseñas (AVG rating)
    # 3. Obtener reseñas con join a user
    # 4. Si usuario logueado: verificar si tiene reseña y si lo tiene en biblioteca
    # 5. Renderizar detail.html con: game, reviews, avg_rating, review_count,
    #    user_review, user_library_entry
    pass
