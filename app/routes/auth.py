# Blueprint: Autenticación (registro, login, logout)
# POST /registro — Valida campos, hashea password, crea User
# POST /login — Verifica password con bcrypt, crea sesión
# GET /logout — Destruye sesión
# Ver: docs/02-Estructura-y-archivos.md (sección routes/auth.py)

from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/registro', methods=['GET', 'POST'])
def register():
    # TODO: Implementar registro
    # 1. Si usuario ya autenticado, redirect a home
    # 2. GET: renderizar auth/register.html
    # 3. POST: obtener username, email, password del formulario
    # 4. Validar: username 3-30 chars alfanumérico+guiones bajos, email válido, password mín 8 chars
    # 5. Verificar unicidad de email y username
    # 6. Crear User con password hasheada (user.set_password())
    # 7. db.session.add + commit
    # 8. Flash éxito, redirect a login
    pass


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: Implementar login
    # 1. Si usuario ya autenticado, redirect a home
    # 2. GET: renderizar auth/login.html
    # 3. POST: obtener email y password del formulario
    # 4. Buscar user por email
    # 5. Verificar password con user.check_password()
    # 6. login_user(user)
    # 7. Flash éxito, redirect a home
    pass


@auth_bp.route('/logout')
def logout():
    # TODO: Implementar logout
    # 1. @login_required
    # 2. logout_user()
    # 3. Flash confirmación, redirect a home
    pass
