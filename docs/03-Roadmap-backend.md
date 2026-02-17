# Roadmap Backend — Catálogo de Juegos Free-to-Play

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Frontend](04-Roadmap-frontend.md) · [Memoria y defensa](05-Memoria-y-defensa.md)

> El backend se hace completo primero. El frontend empieza cuando el backend esté terminado y probado. Para probar las rutas durante el desarrollo, se usan templates mínimos (HTML sin estilos, solo datos) que luego Pablo Pérez reemplazará con la maquetación definitiva.

---

## Fase 1: Cimientos (Días 1-2)

**Objetivo:** App Flask arrancando con BD conectada y Docker.

| Orden | Archivo | Qué hacer | Por qué este orden |
|-------|---------|-----------|-------------------|
| 1 | `requirements.txt` | Listar: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF), requests, psycopg2-binary, python-dotenv | Lo primero: instalar dependencias |
| 2 | `.env.example` y `.env` | Definir: DATABASE_URL, SECRET_KEY, FLASK_ENV, FREETOGAME_API_URL, ADMIN_EMAIL, ADMIN_PASSWORD | Antes de config.py |
| 3 | `.gitignore` | Excluir: .env, __pycache__, .venv, *.pyc, instance/ | Antes del primer commit |
| 4 | `app/config.py` | Clase Config leyendo cada variable del .env | Base para todo |
| 5 | `app/extensions.py` | Instanciar db, login_manager, bcrypt, csrf. Definir user_loader | Los modelos y rutas lo necesitan |
| 6 | `app/__init__.py` | create_app() que carga config, inicializa extensiones. Sin rutas ni modelos aún. Solo devuelve "Hello World" en ruta / temporal | La app debe arrancar vacía |
| 7 | `Dockerfile` | FROM python:3.11-slim, WORKDIR, COPY requirements, pip install, COPY app, CMD flask run --host=0.0.0.0 | Contenerizar |
| 8 | `docker-compose.yml` | Servicio web (build ., puertos 5000:5000, env_file, depends_on db), Servicio db (postgres:15, volumen persistente, credenciales) | Levantar todo junto |
| 9 | `README.md` | Instrucciones básicas: clonar, copiar .env.example a .env, rellenar, docker-compose up | Documentar desde ya |

**Checkpoint:** `docker-compose up` → Flask responde en localhost:5000 con "Hello World". PostgreSQL escucha en su puerto.

---

## Fase 2: Modelos (Días 3-4)

**Objetivo:** Las 4 tablas creadas en PostgreSQL.

| Orden | Archivo | Qué hacer | Por qué este orden |
|-------|---------|-----------|-------------------|
| 1 | `app/models/__init__.py` | Importar User, Game, Review, UserLibrary | Para que Flask los descubra |
| 2 | `app/models/user.py` | Modelo User: id, username (unique, 3–30 chars), email (unique), password_hash, is_admin (Boolean, default=False), created_at. Métodos: set_password(pw), check_password(pw). Propiedades Flask-Login | Independiente, sin FK |
| 3 | `app/models/game.py` | Modelo Game: id, api_id (unique), title, thumbnail, genre, platform, short_description, description, developer, publisher, release_date, game_url, freetogame_profile_url, cached_at | Independiente, sin FK |
| 4 | `app/models/review.py` | Modelo Review: id, user_id (FK), game_id (FK), rating (1-5), text (10–1000 chars), created_at, updated_at. UniqueConstraint(user_id, game_id). Relaciones backref a user y game | Depende de User y Game |
| 5 | `app/models/library.py` | Modelo UserLibrary: id, user_id (FK), game_id (FK), status (String, validado contra lista), created_at. UniqueConstraint(user_id, game_id). Relaciones backref | Depende de User y Game |
| 6 | Actualizar `app/__init__.py` | Dentro de create_app: importar modelos, dentro de app.app_context() hacer db.create_all() | Crear tablas al arrancar |

**Checkpoint:** Reiniciar containers. Entrar a PostgreSQL y verificar que existen las 4 tablas con sus columnas y constraints.

---

## Fase 3: Servicio API + Seed completo (Días 5-7)

**Objetivo:** BD llena con juegos, usuarios demo y reseñas de ejemplo.

| Orden | Archivo | Qué hacer | Por qué este orden |
|-------|---------|-----------|-------------------|
| 1 | `app/services/freetogame.py` | Funciones fetch_all_games() y fetch_game_detail(api_id) con requests. Manejo de errores (try/except, timeout). Devuelve lista de dicts o None | Primero el servicio, luego el seed |
| 2 | `seeds/seed_games.py` | Función que llama al servicio, recorre resultados, INSERT o UPDATE cada juego en BD. Detecta duplicados por api_id. Actualiza cached_at | Depende del servicio y modelo Game |
| 3 | `seeds/seed_users.py` | Función que crea 1 admin (datos del .env, is_admin=True) + 5 usuarios demo con passwords hasheadas. Verifica si ya existen antes de crear | Depende del modelo User |
| 4 | `seeds/seed_reviews.py` | Función que: selecciona 20-30 juegos de la BD, por cada usuario demo le asigna reseñas a 8-15 juegos aleatorios, rating con distribución realista, texto aleatorio de un array de 15-20 frases, fecha aleatoria en los últimos 30 días. Respeta constraint unique | Depende de que haya juegos y usuarios |
| 5 | `seeds/seed_all.py` | Script ejecutable que crea app context, llama seed_games, seed_users, seed_reviews en orden. Print del progreso y contadores finales ("400 juegos, 6 usuarios, 72 reseñas") | Orquesta todo |

**Checkpoint:** Ejecutar `python seeds/seed_all.py`. Verificar en PostgreSQL: ~400 juegos, 6 usuarios (1 admin), ~50-80 reseñas con datos variados.

---

## Fase 4: Decorador admin + Rutas públicas (Días 7-10)

**Objetivo:** Decorador @admin_required listo. Páginas públicas sirviendo datos reales con paginación. Templates mínimos (sin estilos, solo funcionales).

| Orden | Archivo | Qué hacer | Por qué este orden |
|-------|---------|-----------|-------------------|
| 1 | `app/decorators.py` | Decorador admin_required que comprueba current_user.is_admin. Si no, flash("Acceso no autorizado") y redirect a home | Se usará en rutas admin |
| 2 | Templates mínimos para probar | Crear `base.html` con estructura HTML básica (sin Bootstrap aún, solo bloque content), `home.html`, `catalog.html`, `detail.html` con datos Jinja2 sin estilos. Solo para verificar que las rutas pasan datos correctos | Necesarios para que render_template funcione |
| 3 | `app/routes/__init__.py` | Función register_routes(app) | Estructura base |
| 4 | `app/routes/main.py` | Blueprint main_bp. GET `/`: consulta 8 juegos aleatorios o mejor valorados, renderiza home.html | Página de entrada |
| 5 | `app/routes/games.py` | Blueprint games_bp. GET `/catalogo`: recibe query params (genre, platform, sort, q, page), construye query SQLAlchemy con filtros encadenados y **paginación** (20/página, orden por defecto: alfabético), consulta géneros y plataformas únicos, renderiza catalog.html. GET `/juego/<id>`: consulta juego, calcula AVG de ratings, consulta reseñas con join a user, renderiza detail.html | Core de la app |
| 6 | Actualizar `__init__.py` | Registrar blueprints main y games | Conectar rutas |

**Checkpoint:** Navegar a localhost:5000 → ver juegos. `/catalogo` → filtrar por género, buscar por nombre, paginar. `/juego/1` → ver ficha con nota media y reseñas de los usuarios demo.

---

## Fase 5: Autenticación (Días 10-12)

**Objetivo:** Registro, login y logout funcionales con validaciones y CSRF.

| Orden | Archivo | Qué hacer | Por qué este orden |
|-------|---------|-----------|-------------------|
| 1 | Templates mínimos auth | Crear `login.html` y `register.html` con formularios HTML básicos (sin estilos), incluyendo token CSRF | Para probar las rutas |
| 2 | `app/routes/auth.py` | Blueprint auth_bp. GET+POST `/registro`: valida campos (username 3-30 chars, email válido, password mín 8 chars), verifica unicidad de email/username, hashea password, crea User, flash éxito, redirect a login. GET+POST `/login`: busca user por email, check_password, login_user(), flash, redirect a home. GET `/logout`: logout_user(), redirect a home | Todas las rutas privadas dependen de esto |
| 3 | Actualizar `__init__.py` | Registrar blueprint auth | Conectar |
| 4 | Configurar login_manager | En extensions.py: login_view='auth_bp.login', login_message. Para que @login_required redirija al login | Flask-Login lo necesita |

**Checkpoint:** Registrar usuario nuevo → login → ver que current_user existe en navbar → logout. Login con admin del seed → verificar is_admin.

---

## Fase 6: Rutas privadas (Días 12-16)

**Objetivo:** CRUD completo de reseñas, biblioteca, perfil y panel admin funcionando.

| Orden | Archivo | Qué hacer | Por qué este orden |
|-------|---------|-----------|-------------------|
| 1 | Template mínimo form.html | Formulario reseña básico con CSRF | Para probar |
| 2 | `app/routes/reviews.py` | Blueprint reviews_bp. POST crear: valida (rating 1-5, texto 10-1000 chars), comprueba unique, crea Review, redirect a ficha. GET+POST editar: comprueba autoría, muestra form pre-rellenado, actualiza. POST eliminar: comprueba autoría OR is_admin, elimina, redirect | CRUD principal |
| 3 | Template mínimo my_library.html | Lista de juegos con forms de cambiar estado y quitar | Para probar |
| 4 | `app/routes/library.py` | Blueprint library_bp. GET mi-biblioteca: query con filtro de status. POST agregar: comprueba unique. POST cambiar estado (validado contra lista). POST quitar | Segundo CRUD |
| 5 | Template mínimo profile/index.html | Datos del usuario + contadores | Para probar |
| 6 | `app/routes/profile.py` | Blueprint profile_bp. GET /perfil: datos del usuario, counts, últimas reseñas | Depende de reviews y library |
| 7 | Template mínimo admin/reviews.html | Tabla de reseñas con botón eliminar + botón "Actualizar catálogo" | Para probar |
| 8 | `app/routes/admin.py` | Blueprint admin_bp. GET /admin/resenas con @admin_required: lista todas las reseñas. POST eliminar con @admin_required. POST /admin/actualizar-juegos: re-ejecuta seed_games con rate-limit de 30s (verifica cached_at en servidor) | Depende de decorators.py y seeds/seed_games.py |
| 9 | Actualizar `__init__.py` | Registrar blueprints: reviews, library, profile, admin | Conectar todo |

**Checkpoint:** Flujo completo: login → ir a juego → añadir a biblioteca → escribir reseña → editarla → eliminarla → ver perfil → login como admin → panel admin → eliminar reseña de otro usuario → actualizar catálogo con cooldown.

---

## Fase 7: Errores y pulido backend (Días 16-18)

| Orden | Tarea | Detalle |
|-------|-------|---------|
| 1 | Páginas de error | Crear templates `errors/404.html` y `errors/500.html`. Registrar error handlers en __init__.py con `@app.errorhandler(404)` |
| 2 | Validaciones server-side | Revisar TODAS las rutas POST: campos vacíos, rating fuera de rango (1-5), texto de reseña (10-1000 chars), username (3-30 chars alfanumérico), email válido, contraseña mínima (8 chars), status válido |
| 3 | CSRF | Verificar que todos los formularios POST incluyen token CSRF. Verificar que peticiones sin token son rechazadas (400) |
| 4 | Mensajes flash | Verificar que todas las acciones tienen flash message: éxito en crear/editar/eliminar, errores de validación, acceso denegado |
| 5 | Protección de rutas | Verificar que @login_required está en todas las rutas privadas. Verificar que @admin_required está en las de admin. Verificar que no puedes editar/eliminar reseña ajena (excepto admin) |
| 6 | Docker limpio | Probar `docker-compose down -v` + `docker-compose up --build` + ejecutar seed → todo funciona desde cero |
| 7 | Seed idempotente | Verificar que ejecutar seed_all.py dos veces no duplica datos |

**Checkpoint final backend:** La app funciona completa con templates mínimos feos pero funcionales. Todos los flujos están probados. Docker arranca limpio. Seed llena la BD correctamente. CSRF activo. Paginación funcional. Listo para que Pablo Pérez ponga los templates bonitos encima.
