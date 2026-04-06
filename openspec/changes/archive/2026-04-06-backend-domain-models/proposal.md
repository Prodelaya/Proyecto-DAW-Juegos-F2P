# Propuesta — `backend-domain-models`

## Estado
success

## Título
Implementar modelos de dominio del backend e integración de creación de tablas

## Intención

Definir e implementar la base de dominio del backend para el catálogo F2P mediante los cuatro modelos SQLAlchemy documentados (`User`, `Game`, `Review`, `UserLibrary`), incluyendo constraints y validaciones esenciales del dominio, y completar el wiring en `create_app()` para que la creación de tablas ocurra correctamente.

## Problema

La documentación del proyecto ya fija con claridad la Fase 2 del backend, pero el código actual todavía está en estado de scaffolding:

- `app/extensions.py` existe y está listo.
- `app/__init__.py` sigue devolviendo un `"Hello World"` temporal.
- Los archivos de modelos existen, pero continúan como placeholders/TODO.
- No hay wiring confirmado de imports de modelos + `db.create_all()`.

Sin este change, el backend no tiene persistencia de dominio real y las siguientes fases (seeds, rutas públicas, auth, CRUDs) quedan bloqueadas conceptualmente.

## Alcance

Este change **SÍ incluye**:

1. Implementar los modelos:
   - `User`
   - `Game`
   - `Review`
   - `UserLibrary`

2. Incorporar las restricciones y validaciones esenciales ya cerradas por documentación:
   - unicidad donde corresponda
   - FKs
   - `UniqueConstraint(user_id, game_id)` en `Review`
   - `UniqueConstraint(user_id, game_id)` en `UserLibrary`
   - `Game.description` obligatoria
   - `Review.text` obligatoria con rango 10–1000
   - `Review.rating` válida 1–5
   - `UserLibrary.status` como `String` validado contra:
     - `want_to_play`
     - `playing`
     - `played`

3. Implementar relaciones explícitas con `back_populates`.

4. Mantener timestamps simples en UTC según la convención documentada.

5. Completar el wiring en `create_app()` para:
   - importar modelos
   - entrar en `app.app_context()`
   - ejecutar `db.create_all()`

6. Considerar como parte del “done” la **verificación manual del esquema en PostgreSQL**.

## Fuera de alcance

Este change **NO incluye**:

- rutas HTTP nuevas
- formularios
- lógica de auth
- seeds completos
- templates
- corrección del comentario de `GET /logout`
- eliminación del fallback a SQLite
- migraciones con Flask-Migrate
- funcionalidad end-to-end de catálogo/reseñas/biblioteca

## Criterios de aceptación

El change se considera aceptado cuando se cumple TODO esto:

1. Existen implementaciones reales de:
   - `User`
   - `Game`
   - `Review`
   - `UserLibrary`

2. Los modelos reflejan las decisiones cerradas por docs:
   - `Game.description` requerida
   - `UserLibrary.status` como `String`
   - relaciones con `back_populates`
   - reseña única por `(user_id, game_id)` pero editable en comportamiento futuro
   - timestamps UTC simples

3. `create_app()` importa los modelos antes de crear tablas.

4. `db.create_all()` se ejecuta dentro de `app.app_context()`.

5. `db.create_all()` corre sin errores.

6. Existen las cuatro tablas esperadas.

7. Se realiza verificación manual del esquema en PostgreSQL sobre:
   - columnas
   - FKs
   - UNIQUE
   - nullability relevante

## Restricciones y aclaraciones

### PostgreSQL vs SQLite
La documentación del proyecto es explícitamente PostgreSQL-first, pero la configuración actual permite fallback a SQLite.

Este change:
- **no elimina** ese fallback,
- **no expande** el alcance para rediseñar configuración,
- pero **sí deja explícito** que la aceptación funcional/documental de esta fase depende de la verificación manual en PostgreSQL.

En otras palabras: se preserva la discrepancia como tema de aclaración futura, no como expansión del change.

## Riesgos

- **Medio:** la discrepancia entre fallback a SQLite y documentación PostgreSQL-first puede generar confusión de alcance; conviene preservar el comportamiento actual y aclararlo, no mezclarlo con implementación de dominio.
- **Medio:** un orden incorrecto de imports de modelos dentro de `create_app()` puede impedir la creación real de tablas.
- **Medio:** los constraints del modelo pueden desviarse de las expectativas sobre PostgreSQL si no se contrastan manualmente contra el esquema real.

## Justificación

Este scope es deliberadamente acotado. La intención no es “hacer backend completo”, sino construir los cimientos del dominio para que las fases posteriores puedan apoyarse sobre una base coherente, verificable y alineada con la arquitectura documentada.

## Artefactos

- Engram topic key: `sdd/backend-domain-models/proposal`

## Siguiente paso recomendado

- `sdd-spec`
- `sdd-design`

## Resolución de skills

- injected
