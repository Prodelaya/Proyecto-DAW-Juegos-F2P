# Catálogo de Juegos Free-to-Play (f2p-catalog)

Aplicación web para descubrir, valorar y organizar juegos free-to-play. Proyecto final (TFG) de ciclo formativo.

## Tecnologías

- **Backend:** Python 3.11, Flask, SQLAlchemy, PostgreSQL 15
- **Frontend:** Jinja2, Bootstrap, JavaScript vanilla
- **Infraestructura:** Docker, Docker Compose

## Instalación y uso

1. Clonar el repositorio
2. Copiar `.env.example` a `.env` y configurar las variables
3. Levantar los contenedores:

```bash
docker-compose up --build
```

4. Ejecutar el seed para llenar la base de datos:

```bash
docker-compose exec web python seeds/seed_all.py
```

5. Acceder a `http://localhost:5000`

## Datos

Los juegos se obtienen de la [FreeToGame API](https://www.freetogame.com/api-doc) y se cachean en la base de datos local.
