# Catálogo de Juegos Free-to-Play (f2p-catalog)

Aplicación web server-rendered para descubrir, valorar y organizar juegos free-to-play. Proyecto final (TFG) de ciclo formativo.

Los juegos se obtienen desde la FreeToGame API y se cachean en PostgreSQL para que la aplicación pueda seguir funcionando con datos locales.

## Tecnologías

- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-WTF, PostgreSQL 15
- **Frontend:** Jinja2, Bootstrap, JavaScript vanilla
- **Infraestructura:** Docker, Docker Compose

## Funcionalidades

- Catálogo de juegos con búsqueda, filtros y paginación
- Ficha de juego con descripción, requisitos, capturas y reseñas
- Registro, login y logout con sesión de usuario
- Biblioteca personal con estados: `want_to_play`, `playing`, `played`
- Panel de administración para moderar reseñas y actualizar el catálogo

## Instalación y uso

1. Clonar el repositorio
2. Copiar `.env.example` a `.env` y configurar las variables (`DATABASE_URL`, `SECRET_KEY`, `FREETOGAME_API_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`)
3. Levantar los contenedores:

```bash
docker-compose up --build
```

4. Ejecutar el seed para llenar la base de datos:

```bash
docker-compose exec web python seeds/seed_all.py
```

5. Acceder a `http://localhost:5000`

## Notas

- El seed crea juegos, usuarios demo, reseñas de ejemplo y puede ampliarse con entradas de biblioteca para mejorar la demo.
- Las credenciales del administrador se leen desde el archivo `.env`.
- Todas las rutas que modifican datos usan protección CSRF.

## Datos

Los juegos se obtienen de la [FreeToGame API](https://www.freetogame.com/api-doc) y se cachean en la base de datos local.
