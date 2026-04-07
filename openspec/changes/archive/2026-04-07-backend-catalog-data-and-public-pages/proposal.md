# Propuesta — `backend-catalog-data-and-public-pages`

## Estado
success

## Título
Implementar experiencia pública de lectura para home, catálogo y ficha de juego

## Intención

Cerrar la experiencia pública SSR que consume datos cacheados en PostgreSQL y expone home, catálogo y detalle en solo lectura, con contrato mínimo estable para `home.html`, `catalog.html` y `detail.html`.

## Problema

El proyecto ya tiene modelos y placeholders de rutas/templates, pero todavía no existe una experiencia pública funcional ni un contrato Jinja confiable. Sin este change, la app no puede mostrar catálogo real, fichas públicas ni destacados de inicio usando datos seed.

## Alcance

Incluye: `GET /` con 8 destacados híbridos de reseñas recientes; `GET /catalogo` con búsqueda (`title` + `short_description`), filtros (`genre`, `platform`, `publisher`), orden (`alphabetical`, `review_count`, `avg_rating`, `release_date`), paginación y estado en URL (`q`, `genre`, `platform`, `publisher`, `sort`, `page`); `GET /juego/<id>` con datos completos, métricas y reseñas read-only; templates mínimos públicos; seed de juegos + usuarios demo + reseñas demo para soportar la experiencia; uso de FreeToGame solo en seed/refresh manual con reintentos moderados y continuación ante fallo persistente.

## Fuera de alcance

Auth, CRUD de reseñas, biblioteca, perfil, admin, hardening global, consumo en tiempo real de FreeToGame desde rutas públicas y cualquier expansión a áreas privadas.

## Criterios de aceptación

1. Home pública muestra 8 destacados usando ventana de 14 días y desempate por `release_date` más reciente.
2. Catálogo mantiene URL como fuente de verdad; cambios de búsqueda/filtros/orden reinician `page=1`; vacíos muestran mensaje claro sin adulterar query.
3. En orden por reseñas o rating, juegos sin reseñas se tratan como ausencia real y caen por `release_date` más reciente.
4. Ficha pública renderiza juego completo, métricas y reseñas read-only; screenshots ausentes ocultan sección y requisitos ausentes muestran mensaje breve.
5. Queda cerrado el contrato mínimo de variables Jinja para `home.html`, `catalog.html` y `detail.html`, usando nombres canónicos estables para filtros y métricas agregadas.

## Riesgos

- Medio: consultas con agregaciones/orden híbrido pueden complicar SQLAlchemy y paginación.
- Medio: seed demo insuficiente puede degradar home y catálogos ordenados por métricas.
- Bajo: desalineación entre placeholders actuales y contrato Jinja esperado.

## Justificación

Este scope prioriza la lectura pública, que es el núcleo visible del producto, y mantiene fronteras estrictas para no mezclar auth, CRUD ni áreas privadas en el mismo change.

## Rollback plan

Revertir wiring de blueprints/templates públicos y volver a placeholders previos; conservar modelos y datos existentes; desactivar lógica de destacados/orden agregado manteniendo solo navegación mínima sobre datos locales seed.

## Artefactos

- Archivo: `openspec/changes/backend-catalog-data-and-public-pages/proposal.md`
- Módulos/paquetes afectados: `app/routes/main.py`, `app/routes/games.py`, `app/routes/__init__.py`, `app/services/freetogame.py`, `seeds/seed_games.py`, `seeds/seed_users.py`, `seeds/seed_reviews.py`, `seeds/seed_all.py`, `app/templates/main/home.html`, `app/templates/games/catalog.html`, `app/templates/games/detail.html`, parciales públicos.

## Siguiente paso recomendado

- `sdd-spec`
- `sdd-design`

## Resolución de skills

- fallback-path
