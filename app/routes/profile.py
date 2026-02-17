# Blueprint: Perfil de usuario
# GET /perfil — Datos del usuario, contadores, últimas reseñas
# Ver: docs/02-Estructura-y-archivos.md (sección routes/profile.py)

from flask import Blueprint

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/perfil')
def index():
    # TODO: Implementar perfil
    # 1. @login_required
    # 2. Contar reseñas del usuario
    # 3. Contar juegos en biblioteca
    # 4. Obtener últimas 5-10 reseñas del usuario con join a game
    # 5. Renderizar profile/index.html con: user, review_count, library_count, recent_reviews
    pass
