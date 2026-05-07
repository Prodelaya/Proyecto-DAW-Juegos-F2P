# Estructura de Archivos y Descripción Detallada

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Roadmap Frontend](04-Roadmap-frontend.md) · [Memoria y defensa](05-Memoria-y-defensa.md)

---

## 1. ESTRUCTURA COMPLETA DE ARCHIVOS

```
f2p-catalog/
│
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── decorators.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── game.py
│   │   ├── review.py
│   │   └── library.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── games.py
│   │   ├── reviews.py
│   │   ├── library.py
│   │   ├── profile.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   └── freetogame.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── main/
│   │   │   └── home.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── games/
│   │   │   ├── catalog.html
│   │   │   └── detail.html
│   │   ├── reviews/
│   │   │   └── form.html
│   │   ├── library/
│   │   │   └── my_library.html
│   │   ├── profile/
│   │   │   └── index.html
│   │   ├── admin/
│   │   │   └── reviews.html
│   │   ├── errors/
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   └── partials/
│   │       ├── navbar.html
│   │       ├── footer.html
│   │       ├── game_card.html
│   │       ├── flash_messages.html
│   │       └── pagination.html
│   │
│   └── static/
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── main.js
│       └── img/
│           └── logo.png
│
├── seeds/
│   ├── seed_all.py
│   ├── seed_games.py
│   ├── seed_users.py
│   ├── seed_reviews.py
│   └── seed_library.py
│
└── docs/
    ├── 01-Arquitectura.md
    ├── 02-Estructura-y-archivos.md
    ├── 03-Roadmap-backend.md
    ├── 04-Roadmap-frontend.md
    └── 05-Memoria-y-defensa.md
```

---

## 2. QUÉ ES CADA ARCHIVO, QUÉ CONTIENE Y PARA QUÉ SIRVE

### Raíz del proyecto

| Archivo | Qué es | Qué contiene | Para qué sirve |
|---------|--------|-------------|----------------|
| `docker-compose.yml` | Configuración de Docker | Define 2 servicios: la app Flask y PostgreSQL. Puertos, volúmenes, variables de entorno | Levantar todo el proyecto con un solo comando |
| `Dockerfile` | Instrucciones de imagen Docker | Base Python, instalación de dependencias, copia de `app/`, `seeds/` y archivos raíz necesarios, comando de arranque | Construir el contenedor de la app Flask y permitir ejecutar seeds dentro del contenedor |
| `.env.example` | Plantilla de variables de entorno | DATABASE_URL, SECRET_KEY, FLASK_ENV, FREETOGAME_API_URL, ADMIN_EMAIL, ADMIN_PASSWORD | Que cualquiera sepa qué variables configurar sin ver las reales |
| `.gitignore` | Exclusiones de Git | .env, __pycache__, .venv, node_modules, *.pyc | No subir archivos sensibles ni basura al repositorio |
| `README.md` | Documentación del repo | Descripción del proyecto, instrucciones de instalación, uso, tecnologías | Primera impresión del proyecto, instrucciones rápidas |
| `requirements.txt` | Dependencias Python | Flask, SQLAlchemy, Flask-Login, Flask-WTF (CSRF), bcrypt, requests, psycopg2-binary, python-dotenv | pip install -r requirements.txt instala todo lo necesario |

---

### app/__init__.py — Factoría de la aplicación

- **Qué es:** El punto de entrada de la app Flask.
- **Qué contiene:** La función `create_app()` que crea la instancia de Flask, carga la configuración, inicializa las extensiones (BD, login manager, CSRF), registra todos los blueprints (rutas), registra los manejadores de errores (404, 500) y devuelve la app lista.
- **Para qué sirve:** Patrón "Application Factory" de Flask. Permite crear la app de forma limpia y testeable.
- **Depende de:** `config.py`, `extensions.py`, todos los archivos de `routes/`.

### app/config.py — Configuración

- **Qué es:** Clase con los ajustes de la app.
- **Qué contiene:** Lee las variables de entorno (.env) y las expone como atributos: DATABASE_URL, SECRET_KEY, FREETOGAME_API_URL, ADMIN_EMAIL, ADMIN_PASSWORD.
- **Para qué sirve:** Centralizar toda la configuración en un solo sitio.
- **Depende de:** El archivo `.env` (a través de python-dotenv).

### app/extensions.py — Extensiones Flask

- **Qué es:** Archivo donde se instancian las extensiones.
- **Qué contiene:** La instancia de SQLAlchemy (`db`), la instancia de Flask-Login (`login_manager`), la instancia de Bcrypt (`bcrypt`), la instancia de CSRFProtect (`csrf`). Solo se crean aquí, se inicializan en `__init__.py`. También la función `user_loader` que Flask-Login necesita para cargar el usuario de sesión.
- **Para qué sirve:** Evitar importaciones circulares. Los modelos importan `db` de aquí, las rutas importan `login_manager` de aquí. Todo apunta a este archivo.
- **Depende de:** Nada (es la base que otros importan).

### app/decorators.py — Decoradores personalizados

- **Qué es:** Archivo con decoradores reutilizables para proteger rutas.
- **Qué contiene:** El decorador `@admin_required` que verifica que el usuario actual esté logueado Y tenga `is_admin=True`. Si no, redirige a la home con un mensaje flash de error. Se usa combinado con `@login_required` de Flask-Login.
- **Para qué sirve:** Proteger las rutas de admin de forma limpia y reutilizable.
- **Depende de:** `extensions.py` (login_manager), `models/user.py` (campo is_admin).

---

### Modelos (app/models/)

Cada archivo define una tabla de la BD. Todos importan `db` de `extensions.py`.

> **Fechas:** la base de datos conserva los timestamps en UTC. Las plantillas los muestran en hora de Madrid mediante el filtro Jinja `madrid_datetime`.

#### models/__init__.py
- **Qué contiene:** Importa todos los modelos para que Flask los descubra al crear las tablas.
- **Para qué sirve:** Que al hacer `from app.models import User, Game, Review, UserLibrary` funcione.

#### models/user.py — Tabla de usuarios
- **Qué contiene:** Clase `User` con campos: id, username (3–30 chars, solo letras, números y guion bajo), email (formato válido), password_hash, is_admin (Boolean, default False), created_at en UTC. Métodos para hashear y verificar contraseña, validaciones esenciales del modelo y `__repr__` útil. Integración con Flask-Login desde esta fase (is_authenticated, get_id, etc.). Relaciones explícitas con `back_populates`: `reviews` (1:N con Review), `library_entries` (1:N con UserLibrary).
- **Para qué sirve:** Registrar, autenticar y gestionar usuarios, incluyendo el rol admin.
- **Depende de:** `extensions.py` (db, bcrypt).

#### models/game.py — Tabla de juegos (caché de la API)
- **Qué contiene:** Clase `Game` con campos:
  - **Datos básicos** (del endpoint `/games`): id, api_id (unique), title, thumbnail (URL imagen portada), genre, platform, short_description, developer, publisher, release_date, game_url, freetogame_profile_url
  - **Datos detallados** (del endpoint `/game?id`): status (String, ej: "Live"), description (Text, descripción larga y **obligatoria**), req_os, req_processor, req_memory, req_graphics, req_storage (5 campos String para requisitos del sistema), screenshots (JSON, lista de URLs de imágenes)
  - **Metadatos**: cached_at (timestamp UTC de cuándo se cacheó/actualizó el juego)
  - **Relaciones**: `reviews` (1:N con Review), `library_entries` (1:N con UserLibrary), definidas con `back_populates`
- **Decisión de modelado:** El flujo oficial de seed persiste juegos con detalle completo, por eso `description` no se considera opcional en el modelo.
- **Para qué sirve:** Almacenar localmente TODA la información de cada juego (lista + detalle). Se llena con el seed inicial y puede actualizarse manualmente desde el panel admin.
- **Depende de:** `extensions.py` (db).

#### models/review.py — Tabla de reseñas
- **Qué contiene:** Clase `Review` con campos: id, user_id (FK→users), game_id (FK→games), rating (Integer, 1-5), text (String/Text, 10–1000 caracteres y **obligatorio**), created_at UTC, updated_at UTC. Constraint UNIQUE en (user_id, game_id) para que un usuario solo pueda escribir una reseña por juego. Relaciones explícitas con `back_populates`: `user` (N:1 con User), `game` (N:1 con Game).
- **Para qué sirve:** Almacenar las valoraciones y textos de reseña. La reseña es única por usuario+juego, pero el producto contempla edición posterior en fases siguientes.
- **Depende de:** `extensions.py` (db), `user.py`, `game.py` (claves foráneas).

#### models/library.py — Tabla de biblioteca personal
- **Qué contiene:** Clase `UserLibrary` con campos: id, user_id (FK→users), game_id (FK→games), status (String, uno de: 'want_to_play', 'playing', 'played'), created_at UTC. Constraint UNIQUE en (user_id, game_id). Relaciones explícitas con `back_populates`: `user` (N:1), `game` (N:1).
- **Decisión de modelado:** Los estados se guardan como `String` con validación manual en rutas/forms y en el modelo. Se reconocen solo esos tres estados para el producto actual, aunque el diseño podría ampliarse en el futuro.
- **Para qué sirve:** Que cada usuario pueda guardar juegos y marcar su estado.
- **Depende de:** `extensions.py` (db), `user.py`, `game.py` (claves foráneas).

---

### Rutas (app/routes/)

Cada archivo es un Blueprint de Flask que agrupa rutas relacionadas. Todos se registran en `__init__.py`. Todos los formularios POST incluyen token CSRF.

#### routes/__init__.py
- **Qué contiene:** Función `register_routes(app)` que importa y registra cada blueprint con su prefijo de URL.
- **Para qué sirve:** Centralizar el registro. `__init__.py` de la app solo llama a esta función.

#### routes/main.py — Página de inicio
- **Qué contiene:** Blueprint `main_bp`. Ruta GET `/` que consulta juegos destacados (los mejor valorados, los más recientes o unos cuantos aleatorios) y renderiza `home.html` pasando la lista de juegos.
- **Depende de:** `models/game.py`, `models/review.py` (para calcular los mejor valorados).

#### routes/auth.py — Autenticación
- **Qué contiene:** Blueprint `auth_bp`. Rutas:
  - GET+POST `/registro`: muestra formulario / crea usuario con password hasheada. Valida que email y username no existan ya (y cumplen reglas de longitud/formato). Redirige a login tras registro exitoso.
  - GET+POST `/login`: muestra formulario / verifica password con bcrypt, crea sesión con Flask-Login. Redirige a home.
  - POST `/logout`: destruye sesión, redirige a home. Al ser una acción que cambia estado de sesión, debe protegerse con CSRF.
- **Depende de:** `models/user.py`, `extensions.py` (bcrypt, login_manager).

#### routes/games.py — Catálogo y ficha de juego
- **Qué contiene:** Blueprint `games_bp`. Rutas:
  - GET `/catalogo`: recibe query params opcionales (genre, platform, sort, q para búsqueda, page). Consulta juegos filtrados/ordenados en BD con **paginación** (20 por página). Orden por defecto: alfabético (A-Z). Opciones de orden: alfabético, popularidad (más reseñas/mejor valorados). Obtiene listas de géneros y plataformas únicos para los selects. Renderiza `catalog.html` pasando: games (paginados), genres, platforms, filtros actuales, objeto paginación.
  - GET `/juego/<int:id>`: consulta el juego por ID, calcula la nota media de sus reseñas, obtiene las reseñas con su autor, verifica si el usuario logueado ya tiene reseña y si lo tiene en su biblioteca. Renderiza `detail.html` pasando: game, reviews, avg_rating, user_review, user_library_entry.
- **Depende de:** `models/game.py`, `models/review.py`, `models/library.py`.

#### routes/reviews.py — CRUD de reseñas
- **Qué contiene:** Blueprint `reviews_bp`. Rutas (todas con `@login_required`):
  - POST `/juego/<int:game_id>/resena`: crea reseña. Valida: rating entre 1-5, texto 10–1000 chars, que no exista ya una del mismo usuario para ese juego. Redirige a la ficha del juego con flash de éxito.
  - GET+POST `/resena/<int:id>/editar`: solo si el usuario actual es el autor. GET muestra formulario pre-rellenado, POST actualiza rating y texto. Redirige a la ficha del juego.
  - POST `/resena/<int:id>/eliminar`: solo si el usuario actual es el autor **O tiene is_admin=True**. Elimina la reseña. Redirige a la ficha del juego (o al panel admin si viene de ahí).
- **Depende de:** `models/review.py`, `models/game.py`, `extensions.py` (login_required), `decorators.py` (para la comprobación de admin en eliminar).

#### routes/library.py — Biblioteca personal
- **Qué contiene:** Blueprint `library_bp`. Rutas (todas con `@login_required`):
  - GET `/mi-biblioteca`: obtiene todos los juegos del usuario con su estado. Acepta query param opcional `status` para filtrar. Renderiza `my_library.html` pasando: entries, current_status.
  - POST `/biblioteca/agregar/<int:game_id>`: añade juego con status 'want_to_play'. Verifica que no exista ya. Redirige a la ficha del juego.
  - POST `/biblioteca/estado/<int:id>`: recibe el nuevo status por formulario (validado contra lista permitida), actualiza. Redirige a mi-biblioteca.
  - POST `/biblioteca/quitar/<int:id>`: elimina la entrada. Redirige a mi-biblioteca.
- **Depende de:** `models/library.py`, `models/game.py`.

#### routes/profile.py — Perfil de usuario
- **Qué contiene:** Blueprint `profile_bp`. Rutas (con `@login_required`):
  - GET `/perfil`: muestra datos del usuario actual, contadores (X juegos en biblioteca, Y reseñas escritas), listado de sus últimas reseñas con enlace al juego. Renderiza `profile/index.html` pasando: user, review_count, library_count, recent_reviews.
- **Depende de:** `models/user.py`, `models/review.py`, `models/library.py`.

#### routes/admin.py — Panel de administración
- **Qué contiene:** Blueprint `admin_bp`. Rutas (todas con `@login_required` + `@admin_required`):
  - GET `/admin/resenas`: lista todas las reseñas de la plataforma, ordenadas por fecha (más recientes primero). Cada reseña muestra: usuario, juego, rating, texto, fecha, botón eliminar. Renderiza `admin/reviews.html` pasando: reviews.
  - POST `/admin/resenas/<int:id>/eliminar`: elimina cualquier reseña. Redirige a `/admin/resenas` con flash de confirmación.
  - POST `/admin/actualizar-juegos`: re-ejecuta el seed de juegos (llama a la función de seed_games.py). Revisa el catálogo contra la API FreeToGame, crea juegos nuevos, actualiza los que cambian y deja sin tocar los que no presentan cambios. **Rate-limit: 30 segundos entre ejecuciones** (se verifica `cached_at` en servidor; botón con cuenta atrás en cliente). Redirige al panel admin con flash de resumen.
- **Para qué sirve:** Moderación de contenido (eliminar reseñas inapropiadas, spam) y mantenimiento de datos (actualización manual del catálogo de juegos).
- **Depende de:** `models/review.py`, `decorators.py` (@admin_required), `seeds/seed_games.py` (para la actualización del catálogo).

---

### Servicio externo (app/services/)

#### services/freetogame.py — Cliente de la API
- **Qué es:** Módulo Python que encapsula las llamadas HTTP a la API FreeToGame.
- **Qué contiene:** Funciones:
  - `fetch_all_games()`: llama a `GET /api/games`, devuelve lista de diccionarios con los campos básicos de cada juego (id, title, thumbnail, genre, platform, short_description, developer, publisher, release_date, game_url, freetogame_profile_url).
  - `fetch_game_detail(api_id)`: llama a `GET /api/game?id=<api_id>`, devuelve diccionario con datos extendidos (status, description larga, screenshots, minimum_system_requirements). Se llama para juegos nuevos, juegos con cambios básicos o juegos cuyo detalle local está incompleto.
  - Manejo de errores: timeout, API caída, respuesta inesperada. Cada función devuelve None o lista vacía en caso de error, nunca rompe la app. Incluye `time.sleep()` entre llamadas para respetar el rate-limit de 10 req/s de la API.
- **Para qué sirve:** Aislar la comunicación con la API externa. Solo el seed llama a este servicio.
- **Depende de:** La librería `requests` y la URL de la API (de `config.py`).

---

### Seeds (seeds/)

Los scripts de seed llenan la BD con datos iniciales. Se ejecutan una vez tras levantar la app por primera vez (o manualmente desde el panel admin para actualizar juegos).

#### seeds/seed_all.py — Orquestador
- **Qué es:** Script principal que ejecuta los seeds del proyecto en orden.
- **Qué contiene:** Importa la app Flask (para tener el contexto de BD), luego ejecuta seed_games, seed_users, seed_reviews y seed_library en ese orden cuando ese último ya exista en la fase correspondiente. Imprime por consola el progreso ("Cacheando juegos...", "Creando usuarios...", "Generando reseñas...", "Generando biblioteca demo...").
- **Para qué sirve:** Un solo comando para llenar toda la BD: `python seeds/seed_all.py`.
- **Depende de:** `app/__init__.py` (contexto Flask), los otros seeds.

#### seeds/seed_games.py — Cachear juegos de la API
- **Qué contiene:** Función que:
  1. Llama siempre a `fetch_all_games()` → obtiene la lista básica actual de juegos y permite detectar altas nuevas.
  2. Busca cada juego localmente por `api_id`.
  3. Si el juego es nuevo, llama a `fetch_game_detail(api_id)` y lo crea.
  4. Si el juego existe, compara campos básicos; si no cambió nada y el detalle local está completo, lo cuenta como `sin cambios` sin llamar al detalle ni hacer commit.
  5. Si el juego existe pero cambió o tiene detalle incompleto, llama a `fetch_game_detail(api_id)` y actualiza solo entonces.
  6. Guarda screenshots como JSON y requisitos como campos separados cuando hay detalle disponible.
  7. Actualiza `cached_at` solo en juegos creados o actualizados.
  8. Respeta rate-limit de la API con `time.sleep(0.15)` solo cuando llama al endpoint de detalle.
- **Tiempo estimado:** variable. La primera carga o una recarga con muchos cambios puede tardar alrededor de 60-90 segundos; una revisión con catálogo ya caliente debería ser bastante más rápida.
- **Para qué sirve:** Llenar la tabla `games` con TODA la información de cada juego. Reutilizada por la ruta `POST /admin/actualizar-juegos`.
- **Depende de:** `services/freetogame.py`, `models/game.py`.

#### seeds/seed_users.py — Crear usuarios demo
- **Qué contiene:** Función que crea 6 usuarios:
  - 1 admin: email y password tomados del .env (ADMIN_EMAIL, ADMIN_PASSWORD), con `is_admin=True`.
  - 5 usuarios normales: con datos inventados pero realistas (gamer_ana, pixel_pedro, noob_lucia, pro_carlos, indie_maria). Contraseñas simples (demo123) ya que son datos de prueba.
  - Antes de crear, verifica si ya existen para poder re-ejecutar el seed sin duplicar.
- **Para qué sirve:** Que la app tenga usuarios con los que hacer login en la demo. El admin permite mostrar la funcionalidad de moderación.
- **Depende de:** `models/user.py`, `config.py` (para credenciales del admin).

#### seeds/seed_reviews.py — Generar reseñas de muestra
- **Qué contiene:** Función que genera ~50-80 reseñas repartidas entre los 5 usuarios demo y unos 20-30 juegos populares (los primeros de la tabla o unos IDs específicos). Cada reseña tiene:
  - Rating: valor entre 1 y 5 (distribución realista: más 3s y 4s, menos 1s y 5s).
  - Texto: frases cortas variadas de un array predefinido, tipo "Gran juego para pasar el rato", "Los gráficos podrían mejorar pero el gameplay es sólido", "Demasiado pay-to-win para mi gusto", "Lo recomiendo al 100%, llevo 200 horas", "Está bien para ser gratuito, nada del otro mundo", etc. 15-20 frases distintas que se asignan aleatoriamente.
  - Fecha: repartidas en los últimos 30 días (para que no todas tengan la misma fecha).
  - Respeta el constraint unique de user_id + game_id (un usuario no repite juego).
- **Para qué sirve:** Que la web se vea viva en la demo. El profesor verá fichas de juegos con notas medias, reseñas de distintos usuarios y contenido variado.
- **Depende de:** `models/review.py`, `models/user.py`, `models/game.py`.

#### seeds/seed_library.py — Generar biblioteca demo
- **Qué contiene:** Función que crea entradas de biblioteca para usuarios demo con estados variados (`want_to_play`, `playing`, `played`), respetando la unicidad `(user_id, game_id)` y evitando duplicados al reejecutarse.
- **Para qué sirve:** Mejorar la demo de perfil y biblioteca personal con datos iniciales realistas.
- **Depende de:** `models/library.py`, `models/user.py`, `models/game.py`.

---

### Templates (app/templates/)

Todos los templates usan herencia de Jinja2: extienden `base.html` e incluyen los partials. Todos los formularios incluyen token CSRF.

#### base.html — Layout maestro
- **Qué contiene:** Estructura HTML5 completa: doctype, head (meta charset y viewport, título dinámico con `{% block title %}`, Bootstrap CSS vía CDN, enlace a styles.css), body con inclusión de navbar partial, bloque flash_messages, bloque `{% block content %}` vacío, inclusión de footer partial, Bootstrap JS vía CDN, enlace a main.js.
- **Para qué sirve:** No repetir el HTML base. Todas las plantillas heredan de esta.
- **Depende de:** Los partials y los estáticos.

#### partials/navbar.html
- **Qué contiene:** Navbar Bootstrap con: logo/nombre del proyecto como enlace a home, enlaces a Inicio y Catálogo (siempre visibles). Zona condicional: si `current_user.is_authenticated` muestra Mi Biblioteca, Mi Perfil, Cerrar sesión; si además `current_user.is_admin` muestra enlace a Panel Admin. Si no está logueado: Login, Registro.
- **Depende de:** Variable `current_user` (Flask-Login la inyecta automáticamente en todos los templates).

#### partials/footer.html
- **Qué contiene:** Pie de página: nombre del proyecto, año, texto "Datos proporcionados por FreeToGame API" con enlace, nombres de los autores.

#### partials/game_card.html
- **Qué contiene:** Card Bootstrap reutilizable: imagen del juego (thumbnail, con placeholder si la URL falla), título, badge de género (con color), badge de plataforma (PC/Browser/All), nota media si tiene reseñas (estrellas o número), enlace a la ficha. Se incluye con `{% include 'partials/game_card.html' %}` dentro de un bucle for.
- **Para qué sirve:** Reutilizar la misma card en home, catálogo y biblioteca sin duplicar HTML.

#### partials/flash_messages.html
- **Qué contiene:** Bucle Jinja2 que recorre las categorías de flash messages ('success', 'error', 'info', 'warning') y muestra cada mensaje como alerta Bootstrap con botón de cerrar.

#### partials/pagination.html
- **Qué contiene:** Controles de paginación Bootstrap: botones Anterior/Siguiente y números de página. Recibe el objeto `pagination` de Flask-SQLAlchemy y genera los enlaces manteniendo los query params actuales (filtros, búsqueda, orden).
- **Para qué sirve:** Reutilizar paginación en el catálogo (y donde se necesite en el futuro).

#### main/home.html
- **Qué contiene:** Extiende base.html. Sección hero con título del proyecto y breve descripción ("Descubre, valora y organiza los mejores juegos gratuitos"). Grid de juegos destacados (los mejor valorados o aleatorios) usando game_card. Botón "Ver catálogo completo".

#### auth/login.html y auth/register.html
- **Qué contienen:** Extienden base.html. Card Bootstrap centrada con formulario. Login: email + password + botón + enlace a registro. Registro: username (3–30 chars) + email + password (mín 8 chars) + confirmar password + botón + enlace a login. Ambos con validación HTML5 (required, minlength, type=email). El action del form apunta a la misma URL (POST). Token CSRF incluido.

#### games/catalog.html
- **Qué contiene:** Extiende base.html. Zona de filtros: formulario GET con select de género (opciones generadas con for loop de `genres`), select de plataforma, campo input de búsqueda, select de ordenación (alfabético A-Z, popularidad). Los selects mantienen el valor seleccionado (con `selected` condicional). Grid de game_cards. Texto "X juegos encontrados". Controles de paginación (partial `pagination.html`). Mensaje de "sin resultados" si la lista está vacía.

#### games/detail.html
- **Qué contiene:** Extiende base.html. Es la plantilla más compleja:
  - Zona superior: thumbnail como imagen de portada grande, título del juego.
  - Zona de información: tabla/grid con developer, publisher, release_date, género, plataformas, status, enlace "Jugar" a la web oficial. Fecha `cached_at` mostrada en hora de Madrid.
  - Descripción larga (texto completo de la API).
  - Requisitos del sistema: tabla con OS, procesador, memoria, gráficos, almacenamiento (si disponibles, no todos los juegos los tienen).
  - Galería de screenshots: las imágenes del juego en grid o carrusel.
  - Zona de biblioteca (solo si logueado): si el juego NO está en su biblioteca, botón "Añadir a mi biblioteca". Si ya está, muestra el estado actual con select para cambiar y botón quitar.
  - Zona de reseñas: nota media con número de reseñas ("4.2 ★ (12 reseñas)"). Listado de reseñas: cada una con username del autor, rating en estrellas, texto, fecha. Si el usuario logueado es el autor de una reseña: botones editar y eliminar. Si el usuario es admin y NO es el autor: solo botón eliminar. Si el usuario logueado no ha escrito reseña aún: formulario inline (rating + texto + botón enviar).

#### reviews/form.html
- **Qué contiene:** Extiende base.html. Formulario para editar una reseña existente: select de rating pre-seleccionado, textarea con el texto actual (10–1000 chars), botón "Guardar cambios", enlace "Cancelar" que vuelve a la ficha del juego.

#### library/my_library.html
- **Qué contiene:** Extiende base.html. Barra de filtro por estado: 4 botones/enlaces (Todos, Quiero jugar, Jugando, Jugado) que envían query param `status`. Grid de juegos del usuario: cada uno con su game_card, un select para cambiar estado (formulario POST inline), botón quitar. Mensaje "Tu biblioteca está vacía" con enlace al catálogo si no tiene juegos.

#### profile/index.html
- **Qué contiene:** Extiende base.html. Card con datos del usuario: username, email, miembro desde (fecha formateada). Contadores: "X juegos en biblioteca", "Y reseñas escritas". Listado de sus últimas 5-10 reseñas: título del juego (enlace), rating, texto truncado, fecha.

#### admin/reviews.html
- **Qué contiene:** Extiende base.html. Solo accesible si admin. Título "Panel de moderación - Reseñas". Tabla o listado con todas las reseñas: username, juego (enlace), rating, texto (truncado), fecha, botón eliminar (con formulario POST y confirmación JS). Botón "Actualizar catálogo" que ejecuta POST a `/admin/actualizar-juegos` con cooldown de 30 segundos y cuenta atrás visual. Opcionalmente: filtro por juego o usuario.

#### errors/404.html y errors/500.html
- **Qué contienen:** Extienden base.html. Mensaje amable de error ("Página no encontrada" / "Error interno del servidor") con enlace para volver a la home. Diseño limpio acorde al resto de la web.

---

### Archivos estáticos (app/static/)

#### static/css/styles.css
- **Qué contiene:** Estilos personalizados que complementan Bootstrap: paleta de colores del tema (oscuro/gaming), estilos de cards (hover, sombras), estilos de estrellas de rating, ajustes de la navbar, estilos de badges de género/plataforma, estilos de la zona de filtros, estilos específicos de la ficha de juego, estilos de paginación.

#### static/js/main.js
- **Qué contiene:** JavaScript vanilla para: confirmación antes de eliminar (reseña o juego de biblioteca) con `confirm()`, envío de formulario de cambio de estado de biblioteca sin recargar toda la página (opcional, puede ser con submit normal), validación extra de formularios (que las contraseñas coincidan en registro), posible: sistema visual de estrellas clicables para el rating, cuenta atrás de 30 segundos en el botón "Actualizar catálogo" del panel admin.

#### static/img/
- **Qué contiene:** Logo del proyecto, favicon, imagen placeholder para juegos sin thumbnail o con URL de imagen rota.
