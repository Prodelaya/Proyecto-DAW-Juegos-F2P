# Verify — `backend-domain-models`

## Estado
pass

## Resumen ejecutivo

Se revalidó el change `backend-domain-models` enfocando la revisión SOLO en los tres puntos pedidos:

1. confirmar la corrección de `app/models/review.py` para que `rating` rechace booleanos,
2. ejecutar una verificación manual real del esquema en PostgreSQL,
3. actualizar esta evidencia documental con el nuevo estado.

Resultado: los tres puntos quedaron validados. La corrección de `Review.validate_rating()` ya rechaza `True`/`False`, `create_app()` volvió a crear correctamente las tablas del dominio en PostgreSQL real, y el esquema observado coincide con las constraints esperadas para `users`, `games`, `reviews` y `user_library`.

## Alcance de esta reverificación

- Se tomó como base `openspec/changes/backend-domain-models/spec.md`, `design.md` y `tasks.md`.
- NO se hizo build, por pedido explícito del usuario y por instrucción del repo.
- Esta reverificación no agrega scope nuevo.

## Resultado global por severidad

### CRITICAL
- Ninguno.

### WARNING
- Ninguno en el foco pedido.

### SUGGESTION
- Ninguna para este cierre focalizado.

## Evidencia principal

### 1. `Review.rating` ya rechaza booleanos

**Evidencia estática**

- `app/models/review.py:32-37`
- La validación ya no usa `isinstance(rating, int)`, sino `type(rating) is not int`, evitando que `bool` pase como subtipo de `int` en Python.

**Evidencia de ejecución**

Comando ejecutado sobre el contenedor `web`, apuntando a PostgreSQL real:

```bash
docker-compose run --rm --no-deps -e DATABASE_URL="postgresql://postgres:postgres@db:5432/backend_domain_models_verify" web python3 -c "..."
```

Salida relevante:

```text
TABLES ['games', 'reviews', 'user_library', 'users']
BOOL_RATING: ValueError La valoración debe estar entre 1 y 5.
```

Conclusión: `rating=True` ya es rechazado efectivamente por el modelo.

### 2. Verificación manual real del esquema en PostgreSQL

Se recreó la base temporal `backend_domain_models_verify` en PostgreSQL y luego se ejecutó `create_app()` con `DATABASE_URL` apuntando explícitamente a esa base.

**Preparación ejecutada**

```bash
docker-compose exec -T db psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS backend_domain_models_verify;"
docker-compose exec -T db psql -U postgres -d postgres -c "CREATE DATABASE backend_domain_models_verify;"
```

**Bootstrap ejecutado**

```bash
docker-compose run --rm --no-deps -e DATABASE_URL="postgresql://postgres:postgres@db:5432/backend_domain_models_verify" web python3 -c "from app import create_app; create_app()"
```

**Inspección manual ejecutada**

```bash
docker-compose exec -T db psql -U postgres -d backend_domain_models_verify -c "SELECT table_name, column_name, data_type, is_nullable FROM information_schema.columns ..."
docker-compose exec -T db psql -U postgres -d backend_domain_models_verify -c "SELECT conrelid::regclass AS table_name, conname AS constraint_name, pg_get_constraintdef(oid) AS definition FROM pg_constraint ..."
```

#### Hallazgos del esquema observado

**Tablas creadas**

- `users`
- `games`
- `reviews`
- `user_library`

**Nullability y tipos relevantes**

- `users.username`, `users.email`, `users.password_hash`, `users.is_admin`, `users.created_at` → `NOT NULL`
- `games.api_id`, `games.title`, `games.description`, `games.screenshots`, `games.cached_at` → `NOT NULL`
- `reviews.user_id`, `reviews.game_id`, `reviews.rating`, `reviews.text`, `reviews.created_at`, `reviews.updated_at` → `NOT NULL`
- `user_library.user_id`, `user_library.game_id`, `user_library.status`, `user_library.created_at` → `NOT NULL`
- `games.screenshots` quedó materializado como columna `json`

**Constraints observadas en PostgreSQL**

- `users`: `PRIMARY KEY (id)`, `UNIQUE (username)`, `UNIQUE (email)`
- `games`: `PRIMARY KEY (id)`, `UNIQUE (api_id)`
- `reviews`: `PRIMARY KEY (id)`, `FOREIGN KEY (user_id) REFERENCES users(id)`, `FOREIGN KEY (game_id) REFERENCES games(id)`, `UNIQUE (user_id, game_id)`
- `user_library`: `PRIMARY KEY (id)`, `FOREIGN KEY (user_id) REFERENCES users(id)`, `FOREIGN KEY (game_id) REFERENCES games(id)`, `UNIQUE (user_id, game_id)`

Conclusión: el esquema real de PostgreSQL coincide con lo exigido por `spec.md` y `design.md` para este change.

### 3. Nota sobre la ruta temporal `/` en `app/__init__.py`

La ruta inline `@app.get("/")` sigue presente en `app/__init__.py`, pero en esta reverificación queda documentada como:

- herencia del checkpoint de Fase 1,
- fuera del scope funcional de `backend-domain-models`,
- y NO como warning abierto de este change.

No se amplió el alcance para modificarla.

## Veredicto final

**PASS**

La corrección de `Review.rating` quedó confirmada, la verificación manual real en PostgreSQL quedó reejecutada con evidencia reproducible, y no quedan warnings abiertos dentro del foco pedido para `backend-domain-models`.
