# Tasks: Implementar experiencia pública de lectura para home, catálogo y ficha de juego

## Phase 1: Foundation

- [x] 1.1 Ajustar `app/services/freetogame.py` para uso exclusivo en seed/refresh manual con timeouts, reintentos moderados, retorno seguro (`[]`/`None`) y logging de fallos persistentes.
- [x] 1.2 Actualizar `seeds/seed_games.py` para upsert idempotente por `api_id`, normalización mínima de `release_date`, mapeo de detalle completo y continuidad ante fallos parciales por juego.
- [x] 1.3 Actualizar `seeds/seed_users.py`, `seeds/seed_reviews.py` y `seeds/seed_all.py` para crear usuarios demo + reseñas demo recientes con `rating` en `Review`, volumen suficiente para destacados/agregados y ejecución idempotente.
- [x] 1.4 Alinear en `app/routes/games.py` y templates el contrato canónico de `sort` (`alphabetical`, `review_count`, `avg_rating`, `release_date`) definido para el estado URL de catálogo, dejando el parámetro inequívoco.

## Phase 2: Public read models and routes

- [x] 2.1 Implementar en `app/routes/main.py` la consulta SSR de `GET /` con 8 destacados, ventana híbrida de 14 días, desempate por `release_date` descendente y fallback claro cuando falten reseñas recientes.
- [x] 2.2 Implementar en `app/routes/games.py` la lectura de query params `q`, `genre`, `platform`, `publisher`, `sort`, `page` como única fuente de verdad de `GET /catalogo`.
- [x] 2.3 Implementar en `app/routes/games.py` búsqueda sobre `Game.title` + `Game.short_description`, filtros combinables y reinicio de paginación a `page=1` ante cambios de búsqueda/filtros/orden.
- [x] 2.4 Implementar en `app/routes/games.py` ordenaciones `alphabetical`, `review_count`, `avg_rating`, `release_date` usando agregaciones de `Review` y fallback por `release_date` para juegos sin reseñas, sin falsear `NULL` como cero.
- [x] 2.5 Implementar en `app/routes/games.py` `GET /juego/<id>` con `Game`, métricas agregadas (`count`, `avg_rating`) y reseñas read-only con autor, manteniendo fuera de alcance auth, CRUD, biblioteca y admin.
- [x] 2.6 Ajustar `app/routes/__init__.py` para registrar el wiring público SSR sin introducir endpoints POST ni dependencias de áreas privadas.

## Phase 3: Templates SSR contract

- [x] 3.1 Actualizar `app/templates/main/home.html` para consumir `featured_games` y `catalog_url`, contemplando vacío de destacados y datos faltantes sin romper SSR.
- [x] 3.2 Actualizar `app/templates/games/catalog.html` para consumir el contrato mínimo (`games`, `pagination`, `current_filters`, `filter_options`, `total_count`, `has_results`) y preservar query params en reset/paginación.
- [x] 3.3 Actualizar `app/templates/games/detail.html` para consumir `game`, `reviews`, `review_summary`, ocultar screenshots vacías y mostrar mensaje breve cuando falten requisitos.
- [x] 3.4 Ajustar `app/templates/partials/game_card.html` y `app/templates/partials/pagination.html` para reutilizar métricas (`review_count`, `avg_rating`) y mantener navegación consistente con el estado canónico del catálogo.

## Phase 4: Verification and scope guards

- [x] 4.1 Verificar manualmente con seed local que `/`, `/catalogo` y `/juego/<id>` lean solo PostgreSQL cacheado, preserven filtros/orden/paginación y degraden bien en estados vacíos.
- [x] 4.2 Verificar manualmente seed inicial y refresh manual: idempotencia, continuidad ante fallos de FreeToGame y datos demo suficientes para home, catálogo ordenado y ficha pública.
- [x] 4.3 Revisar archivos tocados para confirmar fronteras out-of-scope: sin auth, biblioteca, perfil, admin, hardening global ni consumo runtime de FreeToGame desde rutas públicas.

## Notas de verificación manual

- `docker-compose run --rm web python -m seeds.seed_all` se ejecutó dos veces con resultados consistentes: `405 juegos`, `6 usuarios`, `50 reseñas`.
- Se verificó con Flask test client que `/`, `/catalogo` y `/juego/<id>` responden `200`, renderizan el contrato Jinja canónico y siguen funcionando aun parcheando `requests.get` para fallar, evidenciando lectura pública solo desde BD local.
- El comando directo `python seeds/seed_all.py` quedó corregido para ser import-safe además de mantenerse funcional `python -m seeds.seed_all`.
