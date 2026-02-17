# TODO: Instanciar extensiones Flask
# Se crean aquí y se inicializan en create_app() para evitar importaciones circulares.
# Extensiones: db (SQLAlchemy), login_manager (LoginManager), bcrypt (Bcrypt), csrf (CSRFProtect)
# Configurar login_manager: login_view, login_message, login_message_category
# Definir @login_manager.user_loader → carga User por ID
# Ver: docs/01-Arquitectura.md §7

# TODO: Crear instancias de extensiones
# TODO: Configurar Flask-Login (login_view, mensajes)
# TODO: Implementar user_loader callback
