# Blueprint: Panel de administración
# GET /admin/resenas — Lista todas las reseñas (moderación)
# POST /admin/resenas/<id>/eliminar — Eliminar cualquier reseña
# POST /admin/actualizar-juegos — Re-seed desde API FreeToGame (cooldown 30s)
# Ver: docs/02-Estructura-y-archivos.md (sección routes/admin.py)

from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin/resenas')
def reviews():
    # TODO: Implementar listado de reseñas para moderación
    # 1. @login_required + @admin_required
    # 2. Consultar todas las reseñas ordenadas por fecha (más recientes primero)
    # 3. Renderizar admin/reviews.html con: reviews
    pass


@admin_bp.route('/admin/resenas/<int:id>/eliminar', methods=['POST'])
def delete_review(id):
    # TODO: Implementar eliminación de reseña por admin
    # 1. @login_required + @admin_required
    # 2. Obtener reseña por ID o 404
    # 3. Eliminar, commit
    # 4. Flash confirmación, redirect a panel admin
    pass


@admin_bp.route('/admin/actualizar-juegos', methods=['POST'])
def update_games():
    # TODO: Implementar actualización del catálogo
    # 1. @login_required + @admin_required
    # 2. Verificar cooldown de 30 segundos (comprobar cached_at del último juego)
    # 3. Si no ha pasado el cooldown, flash error y redirect
    # 4. Llamar a la función de seed_games para re-cachear desde la API
    # 5. Flash éxito con conteo de juegos actualizados
    # 6. Redirect al panel admin
    pass
