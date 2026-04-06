# Design: Modelos de dominio del backend

## Enfoque técnico

El change se implementará sobre el paquete `app.models` existente, completando los cuatro modelos SQLAlchemy documentados y conectándolos al bootstrap real de Flask. La estrategia sigue el patrón ya definido por el proyecto: `config.py -> create_app() -> extensions -> models`. No se agregan rutas, seeds ni migraciones; el objetivo es dejar el dominio persistente y verificable en PostgreSQL.

## Decisiones de arquitectura

| Decisión | Opciones consideradas | Decisión | Justificación |
|---|---|---|---|
| Validación de dominio | Solo en rutas/forms; solo en modelo; duplicada | Duplicar en modelo y luego en rutas/forms | La doc del proyecto ya cerró esa política. El modelo protege integridad aunque más adelante fallen validaciones de UI. |
| Relaciones ORM | `backref`; `back_populates` explícito | `back_populates` | Hace visible el contrato entre entidades y coincide con la arquitectura aprobada. |
| Estado de biblioteca | `Enum`; `String` + validación | `String` validado | Mantiene simplicidad MVP y preserva la decisión cerrada de no introducir `Enum`. |
| Creación de tablas | Migraciones; `db.create_all()` | `db.create_all()` en `create_app()` | El roadmap define fase sin Flask-Migrate y el proyecto privilegia arranque simple. |
| Timestamps | Timezone compleja; UTC simple | `datetime.utcnow`/equivalente simple | Sigue la convención actual del repo y evita scope extra. |

## Flujo técnico

```text
create_app()
  -> init de extensiones
  -> importar app.models
  -> app.app_context()
  -> db.create_all()
  -> tablas users/games/reviews/user_library listas
```

```text
User 1 ──< Review >── 1 Game
User 1 ──< UserLibrary >── 1 Game
```

## Estructura de archivos a tocar

| Archivo | Acción | Descripción |
|---|---|---|
| `app/models/user.py` | Modificar | Implementar `User`, validación de `username`, hash de contraseña, relaciones a reseñas y biblioteca. |
| `app/models/game.py` | Modificar | Implementar `Game` con campos de catálogo, `description` obligatoria, `screenshots` JSON y relaciones. |
| `app/models/review.py` | Modificar | Implementar `Review` con FKs, `UniqueConstraint`, rating/texto validados, timestamps y relaciones. |
| `app/models/library.py` | Modificar | Implementar `UserLibrary` con FKs, `UniqueConstraint`, estados permitidos y relación con usuario/juego. |
| `app/models/__init__.py` | Mantener/confirmar | Seguir centralizando imports para descubrimiento de metadatos. |
| `app/__init__.py` | Modificar | Importar modelos antes de `db.create_all()` y ejecutar creación de tablas dentro de `app.app_context()`. |

## Estrategia de validación

- `User`: validar `username` con longitud 3–30 y regex alfanumérico + `_`; exigir unicidad vía constraint de columna; encapsular `set_password()` y `check_password()` con bcrypt.
- `Game`: marcar `description` como no nullable y rechazar vacío a nivel modelo; mantener campos de detalle/requisitos como opcionales; guardar `screenshots` en una sola columna JSON.
- `Review`: validar `rating` entre 1 y 5, `text` entre 10 y 1000 caracteres y `user_id + game_id` único.
- `UserLibrary`: validar `status` contra `want_to_play`, `playing`, `played`; reforzar unicidad por `user_id + game_id`.

La validación del modelo debe fallar antes del commit; la validación en rutas/forms queda para fases posteriores sin redefinir reglas.

## Estrategia de relaciones ORM

- `User.reviews <-> Review.user` con `back_populates`.
- `User.library_entries <-> UserLibrary.user` con `back_populates`.
- `Game.reviews <-> Review.game` con `back_populates`.
- `Game.library_entries <-> UserLibrary.game` con `back_populates`.

Se usarán relaciones explícitas y cascadas de colección donde corresponda en el lado padre (`User`, `Game`) para evitar huérfanos al borrar entidades en fases posteriores, sin introducir lógica adicional fuera del modelo.

## Estrategia de creación de tablas

`create_app()` debe respetar este orden:

1. cargar configuración,
2. inicializar extensiones,
3. importar `app.models` para registrar metadatos,
4. abrir `app.app_context()`,
5. ejecutar `db.create_all()`.

La aceptación del change no termina con el arranque local: también requiere inspección manual del esquema real en PostgreSQL para confirmar columnas, nullability, FKs y UNIQUE de `users`, `games`, `reviews` y `user_library`.

## Contratos internos

- Tabla `users`: lista para Flask-Login (`UserMixin`/equivalente) y bcrypt.
- Tabla `games`: `api_id` único, `description` obligatoria, `screenshots` JSON.
- Tabla `reviews`: reseña única por usuario+juego pero editable en comportamiento futuro.
- Tabla `user_library`: `status` persistido como `String`.

## Riesgos

- **Orden de imports incorrecto**: si `db.create_all()` corre antes de importar modelos, no se crean tablas.
- **Ambigüedad SQLite/PostgreSQL**: el fallback actual a SQLite sigue existiendo; por eso el done debe exigir verificación manual en PostgreSQL y no solo arranque local.
- **Desalineación de constraints**: si validaciones y nullability no coinciden, el dominio puede parecer correcto en Python pero no en el esquema real.

## Testing / verificación

No se agrega suite automatizada en este change. La verificación prevista es manual:

| Capa | Verificación |
|---|---|
| Bootstrap | `create_app()` crea tablas sin error |
| ORM | inspección básica de instancias y relaciones |
| PostgreSQL | revisión manual de columnas, FKs, UNIQUE y nullability |

## Preguntas abiertas

- Ninguna bloqueante para este scope.
