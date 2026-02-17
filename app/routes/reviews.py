# Blueprint: CRUD de reseñas
# POST /juego/<game_id>/resena — Crear reseña (rating 1-5, texto 10-1000 chars)
# GET+POST /resena/<id>/editar — Editar reseña (solo autor)
# POST /resena/<id>/eliminar — Eliminar reseña (autor o admin)
# Ver: docs/02-Estructura-y-archivos.md (sección routes/reviews.py)

from flask import Blueprint

reviews_bp = Blueprint('reviews_bp', __name__)


@reviews_bp.route('/juego/<int:game_id>/resena', methods=['POST'])
def create(game_id):
    # TODO: Implementar creación de reseña
    # 1. @login_required
    # 2. Validar: rating entre 1-5, texto 10-1000 chars
    # 3. Verificar que no exista ya una reseña del usuario para este juego
    # 4. Crear Review, db.session.add + commit
    # 5. Flash éxito, redirect a ficha del juego
    pass


@reviews_bp.route('/resena/<int:id>/editar', methods=['GET', 'POST'])
def edit(id):
    # TODO: Implementar edición de reseña
    # 1. @login_required
    # 2. Obtener reseña por ID o 404
    # 3. Verificar que current_user es el autor
    # 4. GET: mostrar formulario pre-rellenado (reviews/form.html)
    # 5. POST: validar y actualizar rating + texto
    # 6. Redirect a ficha del juego
    pass


@reviews_bp.route('/resena/<int:id>/eliminar', methods=['POST'])
def delete(id):
    # TODO: Implementar eliminación de reseña
    # 1. @login_required
    # 2. Obtener reseña por ID o 404
    # 3. Verificar que current_user es el autor O es admin
    # 4. Eliminar, commit
    # 5. Flash confirmación
    # 6. Redirect a ficha del juego (o panel admin si viene de ahí)
    pass
