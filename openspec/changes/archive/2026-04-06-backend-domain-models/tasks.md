# Tasks: Implementar modelos de dominio del backend

## Fase 1: Base del dominio

- [x] 1.1 Completar `app/models/user.py` con `User`, columnas requeridas, unicidad de `username`/`email`, `created_at` UTC, `__repr__` seguro y métodos `set_password()` / `check_password()`.
- [x] 1.2 Incorporar en `app/models/user.py` la validación de `username` para longitud 3–30 y patrón alfanumérico con `_`, rechazando valores inválidos antes de persistir.
- [x] 1.3 Completar `app/models/game.py` con `Game`, `api_id` único, `description` obligatoria, `screenshots` JSON, `cached_at` UTC y el resto de campos documentados como opcionales cuando corresponda.

## Fase 2: Integridad y relaciones ORM

- [x] 2.1 Completar `app/models/review.py` con `Review`, FKs a `users` y `games`, `UniqueConstraint(user_id, game_id)`, `rating` válido entre 1–5, `text` obligatorio de 10–1000 caracteres, `created_at`, `updated_at` y `__repr__`.
- [x] 2.2 Completar `app/models/library.py` con `UserLibrary`, FKs a `users` y `games`, `UniqueConstraint(user_id, game_id)`, `status` como `String`, validación contra `want_to_play|playing|played`, `created_at` UTC y `__repr__`.
- [x] 2.3 Declarar en `app/models/user.py`, `app/models/game.py`, `app/models/review.py` y `app/models/library.py` todas las relaciones bidireccionales usando `back_populates`, evitando `backref` y dejando las colecciones listas para uso del dominio.

## Fase 3: Wiring de descubrimiento y creación de tablas

- [x] 3.1 Actualizar `app/models/__init__.py` para reexportar `User`, `Game`, `Review` y `UserLibrary`, asegurando que el paquete registre los metadatos de todos los modelos.
- [x] 3.2 Modificar `app/__init__.py` para que `create_app()` cargue configuración, inicialice extensiones, importe `app.models`, entre en `app.app_context()` y ejecute `db.create_all()` dentro de ese contexto.
- [x] 3.3 Confirmar en `app/__init__.py` y `app/models/*.py` que el change no introduce rutas, seeds, migraciones ni cambios de configuración fuera del alcance aprobado.

## Fase 4: Verificación manual de cierre

- [x] 4.1 Verificar manualmente que el arranque con `create_app()` crea sin error las tablas `users`, `games`, `reviews` y `user_library`.
- [x] 4.2 Inspeccionar manualmente en PostgreSQL columnas, nullability, claves foráneas y restricciones `UNIQUE` de las cuatro tablas para contrastarlas con `openspec/changes/backend-domain-models/spec.md` y `design.md`.
- [x] 4.3 Registrar cualquier discrepancia detectada durante la inspección manual, especialmente la ambigüedad PostgreSQL vs SQLite, sin ampliar el scope de `backend-domain-models`.

## Notas de verificación manual

- Verificación ejecutada contra PostgreSQL en una base temporal `backend_domain_models_verify` usando `create_app()` y consultas a `information_schema`/`pg_indexes`.
- No se detectaron discrepancias de esquema en `users`, `games`, `reviews` ni `user_library` respecto de `spec.md` y `design.md`.
- Sigue existiendo la ambigüedad operativa documentada entre PostgreSQL y el fallback SQLite de `app/config.py` cuando no hay `DATABASE_URL`; no se amplió el scope para modificar esa política, pero el done de este change quedó validado explícitamente en PostgreSQL.
