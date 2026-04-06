# Exploración — `backend-domain-models`

## Estado
completed

## Resumen ejecutivo

- La documentación define la Fase 2 como la implementación de cuatro modelos de dominio con SQLAlchemy más validaciones esenciales a nivel modelo y el wiring de `db.create_all()` dentro de `create_app()`.
- El código actual solo tiene el esqueleto de factory/extensiones: `app/extensions.py` está implementado, pero `app/__init__.py` todavía devuelve el `"Hello World"` temporal y no importa modelos, no registra rutas y no ejecuta `db.create_all()`.
- `app/models/user.py`, `app/models/game.py`, `app/models/review.py` y `app/models/library.py` existen pero siguen como stubs/TODO; `app/models/__init__.py` únicamente reexporta esos placeholders.
- Las discrepancias principales docs/código son:
  - `app/config.py` soporta fallback a SQLite mientras que la documentación y el roadmap están pensados “PostgreSQL-first”.
  - Comentarios en `app/routes/auth.py` todavía describen `GET /logout`, aunque la guía del repo prefiere `POST` para acciones que cambian estado.

## Fuentes verificadas

### Documentación
- `docs/01-Arquitectura.md`
- `docs/03-Roadmap-backend.md`

### Código / estructura relevante
- `app/__init__.py`
- `app/extensions.py`
- `app/models/__init__.py`
- `app/models/user.py`
- `app/models/game.py`
- `app/models/review.py`
- `app/models/library.py`
- `app/config.py`
- `app/routes/auth.py`

## Estado actual del repositorio

### 1. Factoría de aplicación
- Existe la base de la app factory.
- `app/__init__.py` todavía está en estado inicial.
- No hay wiring de modelos antes de crear tablas.
- No está resuelto el `db.create_all()` dentro de `app.app_context()`.

### 2. Extensiones
- `app/extensions.py` sí está implementado.
- El esqueleto de extensiones compartidas existe y es consistente con la arquitectura documentada.

### 3. Paquete de modelos
- La carpeta/model package ya existe.
- Los archivos objetivo para el change ya están creados:
  - `user.py`
  - `game.py`
  - `review.py`
  - `library.py`
- Pero todavía no implementan el dominio requerido por la Fase 2.
- `app/models/__init__.py` todavía funciona como placeholder/reexport básico.

### 4. Integración de creación de tablas
- Hoy no hay evidencia de que `create_app()`:
  1. importe modelos,
  2. entre en `app.app_context()`,
  3. ejecute `db.create_all()`.

## Alcance de dominio requerido identificado en la documentación

Según la documentación revisada, este change debe cubrir:

### User
- `id`
- `username` único, 3–30 chars, alfanumérico y `_`
- `email` único
- `password_hash`
- `is_admin` boolean, default `False`
- `created_at` UTC
- Métodos:
  - `set_password(pw)`
  - `check_password(pw)`
  - `__repr__`
- Debe quedar listo para Flask-Login

### Game
- `id`
- `api_id` único
- `title`
- `thumbnail`
- `genre`
- `platform`
- `short_description`
- `description` **obligatoria**
- `developer`
- `publisher`
- `release_date`
- `game_url`
- `freetogame_profile_url`
- `status`
- `req_os`
- `req_processor`
- `req_memory`
- `req_graphics`
- `req_storage`
- `screenshots` JSON
- `cached_at` UTC
- `__repr__`

### Review
- `id`
- `user_id` FK
- `game_id` FK
- `rating` entre 1 y 5
- `text` **obligatorio**, 10–1000 caracteres
- `created_at` UTC
- `updated_at` UTC
- `__repr__`
- `UniqueConstraint(user_id, game_id)`
- Relaciones explícitas con `back_populates`

### UserLibrary
- `id`
- `user_id` FK
- `game_id` FK
- `status` como `String`
- Estados válidos:
  - `want_to_play`
  - `playing`
  - `played`
- `created_at` UTC
- `__repr__`
- `UniqueConstraint(user_id, game_id)`
- Relaciones explícitas con `back_populates`

## Decisiones de diseño confirmadas por la documentación

- Este change incluye **persistencia + validaciones esenciales en modelos**.
- `Game.description` es requerida.
- `UserLibrary.status` se guarda como `String`, no como `Enum`.
- Las validaciones clave se duplican deliberadamente:
  - en rutas/forms para UX
  - en modelos para integridad del dominio
- Las relaciones deben usar `back_populates`, no `backref`.
- La reseña por `(user_id, game_id)` es única, pero el comportamiento esperado más adelante es que sea editable.
- El “done” de esta fase incluye **verificación manual del esquema real en PostgreSQL**.

## Huecos detectados

- Falta implementar completamente los cuatro modelos.
- Falta agregar constraints y validaciones de dominio requeridas.
- Falta conectar los imports de modelos en el arranque.
- Falta ejecutar `db.create_all()` correctamente dentro de `create_app()`.
- Falta alinear el criterio de aceptación con el hecho de que el config actual admite SQLite.

## Discrepancias entre documentación y código

### PostgreSQL-first vs fallback a SQLite
- La documentación y el roadmap suponen PostgreSQL como base principal.
- El código de configuración actual todavía permite fallback a SQLite.
- Esto no invalida el change, pero sí introduce una ambigüedad de aceptación:
  - el roadmap pide verificación manual en PostgreSQL,
  - mientras que el runtime podría levantar con SQLite.

### Comentarios de logout vs guía de seguridad
- En comentarios de `app/routes/auth.py` todavía aparece `GET /logout`.
- Las reglas del repo prefieren `POST` para acciones que cambian estado.
- No forma parte central de este change, pero es una discrepancia real detectada.

## Dependencias

- `app/extensions.py` debe seguir siendo el lugar único de instanciación de extensiones.
- `create_app()` debe importar modelos antes de intentar crear tablas.
- La Fase 3 (service + seeds) depende de que este change deje el dominio estable.

## Riesgos

- `db.create_all()` seguirá siendo inefectivo si los modelos no se importan antes dentro de `app.app_context()`.
- El trabajo posterior de rutas y seeds todavía está scaffold-only; este change no debe prometer funcionalidad end-to-end.
- La verificación manual en PostgreSQL es requerida por docs, pero el config actual permite SQLite fallback; la aceptación puede quedar ambigua si no se explicita.
- Los comentarios de auth hoy entran en tensión con la guía de seguridad del repo.

## Artefactos

- Engram topic key: `sdd/backend-domain-models/explore`

## Siguiente paso recomendado

- Crear proposal/spec limitado a:
  1. implementar `User`, `Game`, `Review`, `UserLibrary`
  2. agregar constraints y validaciones esenciales según docs
  3. wirear import de modelos + `db.create_all()` dentro de `create_app()`
  4. explicitar en aceptación la discrepancia PostgreSQL-vs-SQLite, sin expandir scope

## Resolución de skills

- none
