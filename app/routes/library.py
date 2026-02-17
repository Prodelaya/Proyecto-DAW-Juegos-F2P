# Blueprint: Biblioteca personal del usuario
# GET /mi-biblioteca — Lista juegos del usuario con filtro por estado
# POST /biblioteca/agregar/<game_id> — Añadir juego (status 'want_to_play')
# POST /biblioteca/estado/<id> — Cambiar estado
# POST /biblioteca/quitar/<id> — Quitar de biblioteca
# Ver: docs/02-Estructura-y-archivos.md (sección routes/library.py)

from flask import Blueprint

library_bp = Blueprint('library_bp', __name__)


@library_bp.route('/mi-biblioteca')
def my_library():
    # TODO: Implementar listado de biblioteca
    # 1. @login_required
    # 2. Obtener todas las entradas del usuario
    # 3. Si query param 'status', filtrar por estado
    # 4. Renderizar my_library.html con: entries, current_status
    pass


@library_bp.route('/biblioteca/agregar/<int:game_id>', methods=['POST'])
def add(game_id):
    # TODO: Implementar agregar a biblioteca
    # 1. @login_required
    # 2. Verificar que el juego existe
    # 3. Verificar que no esté ya en la biblioteca del usuario
    # 4. Crear UserLibrary con status='want_to_play'
    # 5. Flash éxito, redirect a ficha del juego
    pass


@library_bp.route('/biblioteca/estado/<int:id>', methods=['POST'])
def update_status(id):
    # TODO: Implementar cambio de estado
    # 1. @login_required
    # 2. Obtener entrada por ID, verificar que pertenece al usuario
    # 3. Validar nuevo status contra VALID_STATUSES
    # 4. Actualizar, commit
    # 5. Redirect a mi-biblioteca
    pass


@library_bp.route('/biblioteca/quitar/<int:id>', methods=['POST'])
def remove(id):
    # TODO: Implementar quitar de biblioteca
    # 1. @login_required
    # 2. Obtener entrada por ID, verificar que pertenece al usuario
    # 3. Eliminar, commit
    # 4. Flash confirmación, redirect a mi-biblioteca
    pass
