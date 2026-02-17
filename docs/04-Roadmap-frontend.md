# Roadmap Frontend + Calendario — Catálogo de Juegos Free-to-Play

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Memoria y defensa](05-Memoria-y-defensa.md)

> Empieza cuando el backend esté terminado (Fase 7 completada). Todos los templates mínimos ya existen con las variables Jinja2 correctas. El trabajo de Pablo Pérez es reemplazar cada template con la versión maquetada, sin tocar Python.

---

## Fase F1: Layout base y partials (Días 1-3 del frontend)

**Objetivo:** Estructura visual base lista.

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/base.html` | Reescribir el template mínimo: HTML5 completo, Bootstrap CDN en head, bloque title, bloque content, scripts al final. Include de los partials |
| 2 | `app/templates/partials/navbar.html` | Navbar Bootstrap responsive: logo, enlaces públicos (Inicio, Catálogo), zona auth condicional (Login/Registro si anónimo; Mi Biblioteca, Mi Perfil, Cerrar Sesión si logueado; + Panel Admin si admin). Hamburger menu en móvil |
| 3 | `app/templates/partials/footer.html` | Footer: créditos, enlace FreeToGame API, año |
| 4 | `app/templates/partials/flash_messages.html` | Alertas Bootstrap con dismiss para cada categoría de flash |
| 5 | `app/templates/partials/pagination.html` | Controles de paginación Bootstrap reutilizables |
| 6 | `app/static/css/styles.css` | Paleta de colores gaming/oscuro, variables CSS, estilos base de cards, badges, estrellas de rating, ajustes sobre Bootstrap |

**Checkpoint:** Todas las páginas ya tienen navbar, footer y estilos base. La app se ve coherente.

---

## Fase F2: Home y componente card (Días 3-5)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/partials/game_card.html` | Card Bootstrap: imagen (con placeholder si falla), título, badges de género y plataforma, nota media, enlace. Hover effect |
| 2 | `app/templates/main/home.html` | Hero section (título, descripción, CTA al catálogo), grid de juegos destacados con game_card, diseño atractivo |

**Checkpoint:** Home con aspecto profesional. Cards reutilizables.

---

## Fase F3: Catálogo y ficha (Días 5-8)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/games/catalog.html` | Zona de filtros (selects estilizados, buscador, selector de orden: A-Z / popularidad), grid responsive de cards, texto de resultados, controles de paginación, mensaje vacío |
| 2 | `app/templates/games/detail.html` | Layout de ficha completo: portada (thumbnail grande), título, tabla de datos (developer, publisher, release_date, género, plataformas, status, enlace oficial), cached_at como "(Actualizado: DD/MM/YYYY)", descripción larga, tabla de requisitos del sistema (OS, procesador, memoria, gráficos, almacenamiento — condicional, no todos los juegos lo tienen), galería de screenshots (grid/carrusel), zona de biblioteca, zona de reseñas con estrellas visuales, formulario inline de reseña (con CSRF), listado de reseñas |
| 3 | `app/static/js/main.js` | Confirm antes de eliminar, validación passwords coinciden en registro, posible sistema visual de estrellas clicables, cuenta atrás de 30s en botón "Actualizar catálogo" |

**Checkpoint:** Catálogo navegable con filtros y paginación. Ficha de juego completa y atractiva.

---

## Fase F4: Auth y perfil (Días 8-10)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/auth/login.html` | Card centrada con formulario estilizado, validación HTML5, token CSRF |
| 2 | `app/templates/auth/register.html` | Idem pero con más campos (username 3-30, password mín 8) |
| 3 | `app/templates/profile/index.html` | Card de perfil con contadores y lista de reseñas recientes |

**Checkpoint:** Flujo de auth visualmente pulido.

---

## Fase F5: Biblioteca, reseña y admin (Días 10-13)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/library/my_library.html` | Filtro por pestañas/botones de estado, grid de juegos con controles inline |
| 2 | `app/templates/reviews/form.html` | Formulario de edición con campos pre-rellenados, estrellas, textarea (10-1000 chars) |
| 3 | `app/templates/admin/reviews.html` | Tabla/lista de moderación con botones eliminar estilizados. Botón "Actualizar catálogo" con cuenta atrás 30s y feedback visual |
| 4 | `app/templates/errors/404.html` y `500.html` | Páginas de error con estilo acorde al resto |

**Checkpoint:** Todas las páginas maquetadas.

---

## Fase F6: Responsive y pulido (Días 13-15)

| Tarea | Detalle |
|-------|---------
| Responsive | Testear TODAS las páginas en móvil: catálogo (cards a 1 columna), ficha, filtros, formularios, navbar hamburger, paginación |
| Estados vacíos | Mensajes amables: "Tu biblioteca está vacía", "No hay resultados para esta búsqueda", "Sé el primero en dejar una reseña" |
| Consistencia | Mismos paddings, márgenes, colores, tipografía en todas las páginas |
| Microinteracciones | Hover en cards, transiciones suaves, animación de estrellas, cuenta atrás en botón admin |
| Favicon + logo | Añadir en static/img/ |
| Testing visual | Recorrer TODOS los flujos y verificar que nada se rompe visualmente |

---

## CALENDARIO CONJUNTO

> Backend primero (Pablo Laya), frontend después (Pablo Pérez). No trabajan en paralelo en el código, pero Pablo Pérez puede ir preparando wireframes, paleta de colores y estructura CSS mientras Pablo Laya hace el backend.

| Semana | Pablo Laya (Backend) | Pablo Pérez (mientras tanto) |
|--------|-------------|--------------------------
| **Sem 1** | Fase 1 (cimientos + Docker) + Fase 2 (modelos) | Preparar wireframes en papel/Figma de todas las pantallas. Definir paleta de colores y estilo visual |
| **Sem 2** | Fase 3 (seed completo) + Fase 4 (decorador + rutas públicas) | Diseñar la estructura de cada template: qué va en cada zona, qué componentes se reutilizan. Puede ir creando styles.css base |
| **Sem 3** | Fase 5 (auth) + Fase 6 (rutas privadas + admin) | Preparar presentación/Canva para la defensa. Estudiar Jinja2 básico ({% block %}, {{ var }}, {% for %}, {% if %}) |
| **Sem 4** | Fase 7 (errores + pulido) → **ENTREGA BACKEND** | **Empieza frontend:** Fases F1-F3 (base, home, catálogo, ficha) |
| **Sem 5** | Apoyo + revisión + testing conjunto | Fases F4-F6 (auth, biblioteca, admin, responsive, pulido) |
| **Sem 6** | Testing final + Docker limpio + escritura memoria | Testing final + últimos ajustes + escritura memoria |

---

## MOMENTO DE CONEXIÓN CLAVE

**Al terminar la Fase 7**, Pablo Laya le entrega a Pablo Pérez:

1. **El repo funcionando** con docker-compose up + seed
2. **Un documento de "contrato de variables"**: por cada template, qué variables Jinja2 recibe, su tipo y un ejemplo. Así:

```
catalog.html recibe:
  - games        → objeto Pagination de Flask-SQLAlchemy (iterable, con .items, .page, .pages, .has_prev, .has_next)
  - genres       → lista de strings ["Shooter", "MMORPG", "Strategy", ...]
  - platforms    → lista de strings ["PC (Windows)", "Web Browser", "All"]
  - current_genre    → string o None (filtro activo)
  - current_platform → string o None
  - current_sort     → string o None ("alpha" o "popularity", default "alpha")
  - current_query    → string o None (texto de búsqueda)

detail.html recibe:
  - game             → objeto Game completo, con todos los campos:
                         .title, .thumbnail, .genre, .platform, .status,
                         .short_description, .description (texto largo),
                         .developer, .publisher, .release_date, .game_url,
                         .freetogame_profile_url, .cached_at,
                         .req_os, .req_processor, .req_memory, .req_graphics, .req_storage,
                         .screenshots (lista JSON de URLs, ej: ["https://...1.jpg", "https://...2.jpg"])
  - reviews          → lista de objetos Review (cada uno tiene .user.username, .rating, .text, .created_at)
  - avg_rating       → float o None (nota media)
  - review_count     → int
  - user_review      → objeto Review o None (la reseña del usuario actual, si existe)
  - user_library_entry → objeto UserLibrary o None (si el usuario tiene el juego en biblioteca)
```

Con eso Pablo Pérez puede reemplazar cada template mínimo por la versión maquetada sin preguntar nada.
