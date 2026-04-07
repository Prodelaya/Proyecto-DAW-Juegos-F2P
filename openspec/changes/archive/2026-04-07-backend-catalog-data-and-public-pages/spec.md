# Especificación — Catálogo público SSR y páginas públicas de lectura

## Propósito

Definir el comportamiento público SSR de solo lectura para home, catálogo y ficha de juego usando datos cacheados en PostgreSQL, con contrato mínimo estable para Jinja y fronteras estrictas de alcance.

## Requisitos

### Requisito: home pública destacada

La ruta `GET /` MUST renderizar exactamente 8 juegos destacados. La selección SHALL usar una señal híbrida compuesta por volumen de reseñas recientes y promedio de rating de esas reseñas dentro de una ventana de 14 días; los empates MUST resolverse por `release_date` más reciente. La ruta MUST leer exclusivamente datos locales cacheados.

#### Escenario: Mostrar destacados híbridos
- Given que existen juegos con reseñas en los últimos 14 días
- When un visitante abre `GET /`
- Then la respuesta SHALL incluir exactamente 8 destacados ordenados por la señal híbrida
- And cualquier empate SHALL resolverse por `release_date` más reciente

### Requisito: catálogo con URL canónica

La ruta `GET /catalogo` MUST tratar `q`, `genre`, `platform`, `publisher`, `sort` y `page` como estado canónico en URL. La búsqueda libre SHALL aplicarse sobre `title` y `short_description`. Los filtros de género, plataforma y publisher MUST poder combinarse libremente. Cambiar búsqueda, filtros u orden MUST reiniciar `page=1`.

#### Escenario: Componer búsqueda y filtros
- Given una URL de catálogo con `q`, `genre`, `platform`, `publisher`, `sort` y `page`
- When el servidor procesa `GET /catalogo`
- Then los resultados SHALL reflejar exactamente ese estado canónico
- And la búsqueda SHALL considerar `title` y `short_description`

#### Escenario: Reiniciar paginación por cambio de criterio
- Given un visitante ubicado en una página mayor a 1
- When modifica `q`, cualquier filtro o `sort`
- Then el siguiente estado canónico MUST fijar `page=1`

### Requisito: ordenaciones y estado vacío del catálogo

`GET /catalogo` MUST soportar `alphabetical`, `review_count`, `avg_rating` y `release_date`. Para `review_count` y `avg_rating`, los juegos sin reseñas MUST NOT tratarse como cero; SHALL ordenarse detrás de los juegos con señal válida y desempatarse por `release_date` más reciente. Si no hay resultados, la vista MUST mostrar un mensaje claro y una sugerencia de reset o ajuste, y MUST NOT aplicar fallback automático.

#### Escenario: Ordenar por métricas sin falsear ausencias
- Given una mezcla de juegos con y sin reseñas
- When el visitante ordena por `review_count` o `avg_rating`
- Then los juegos sin reseñas MUST quedar detrás de los que sí tienen señal válida
- And entre ellos SHALL prevalecer `release_date` más reciente

#### Escenario: Mostrar vacío sin adulterar query
- Given un filtro o búsqueda sin coincidencias
- When se renderiza el catálogo
- Then la vista MUST informar que no hay resultados y sugerir reset o ajuste
- And el sistema MUST NOT reemplazar automáticamente la consulta por otra

### Requisito: ficha pública de juego en solo lectura

La ruta `GET /juego/<id>` MUST renderizar información completa del juego, métricas agregadas de reseñas y reseñas en solo lectura. Si faltan screenshots, la sección MUST ocultarse. Si faltan requisitos mínimos, la vista SHALL mostrar un mensaje breve en lugar de una tabla vacía.

#### Escenario: Renderizar ficha pública completa
- Given un juego existente con datos completos y reseñas
- When un visitante abre `GET /juego/<id>`
- Then la respuesta SHALL incluir datos del juego, métricas agregadas y reseñas solo lectura

#### Escenario: Degradar la vista por datos opcionales faltantes
- Given un juego sin screenshots o sin requisitos mínimos
- When se renderiza la ficha pública
- Then la sección de screenshots MUST ocultarse si no hay imágenes
- And la zona de requisitos SHALL mostrar un mensaje breve si faltan datos

### Requisito: origen de datos, seed demo y contrato Jinja

El change MUST cubrir únicamente lectura pública SSR. El seed de este change SHALL crear juegos, usuarios demo y reseñas demo con `rating` embebido en `Review`, solo para soportar lectura pública. FreeToGame MAY usarse en seed inicial o refresh manual posterior, pero MUST NOT consultarse en tiempo real desde rutas públicas. Durante seed o refresh, el sistema SHOULD reintentar de forma moderada y luego registrar el fallo y continuar. El contrato mínimo de Jinja SHALL quedar cerrado así: `home.html` recibe `featured_games`; `catalog.html` recibe `games`, `pagination`, `current_filters` y `filter_options`; `detail.html` recibe `game`, `reviews` y `review_summary`. Auth, CRUD de reseñas, biblioteca, perfil, admin y hardening global MUST quedar explícitamente fuera de alcance.

#### Escenario: Renderizar templates con contrato mínimo estable
- Given datos locales suficientes para home, catálogo y detalle
- When cada ruta pública renderiza su template
- Then cada template SHALL recibir al menos las variables mínimas definidas por este contrato

#### Escenario: Mantener fronteras del change
- Given una necesidad de escritura, autenticación o gestión privada
- When se evalúa el alcance de `backend-catalog-data-and-public-pages`
- Then esa capacidad MUST quedar fuera de esta especificación
