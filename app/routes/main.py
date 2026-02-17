# Blueprint: Página de inicio
# GET / — Muestra juegos destacados (mejor valorados o aleatorios)
# Ver: docs/02-Estructura-y-archivos.md (sección routes/main.py)

from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def home():
    # TODO: Consultar juegos destacados (los mejor valorados, más recientes o aleatorios)
    # Renderizar main/home.html con: games (lista de Game)
    pass
