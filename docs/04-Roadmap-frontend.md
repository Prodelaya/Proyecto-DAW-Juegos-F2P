# Roadmap Frontend + Calendario — Catálogo de Juegos Free-to-Play

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Memoria y defensa](05-Memoria-y-defensa.md)

> Empieza cuando el backend esté terminado (Fase 7 completada). Todos los templates mínimos ya existen con las variables Jinja2 correctas. El trabajo de Pablo Pérez es reemplazar cada template con una versión maquetada **sencilla**, apoyándose al máximo en Bootstrap y **sin tocar Python**.

> **Criterio clave:** el frontend debe ser fácil de mantener para un compañero novato. Primero funcional, limpio y responsive. Los extras visuales o de JavaScript solo se hacen si sobra tiempo.

---

## Fase F1: Layout base y partials (Días 1-3 del frontend)

**Objetivo:** Estructura visual base lista.

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/base.html` | Reescribir el template mínimo: HTML5 completo, Bootstrap CDN en head, bloque title, bloque content, scripts al final. Include de los partials |
| 2 | `app/templates/partials/navbar.html` | Navbar Bootstrap responsive: logo, enlaces públicos (Inicio, Catálogo), zona auth condicional (Login/Registro si anónimo; Mi Biblioteca, Mi Perfil, formulario POST de Cerrar Sesión si logueado; + Panel Admin si admin). Hamburger menu en móvil |
| 3 | `app/templates/partials/footer.html` | Footer: créditos, enlace FreeToGame API, año |
| 4 | `app/templates/partials/flash_messages.html` | Alertas Bootstrap con dismiss para cada categoría de flash |
| 5 | `app/templates/partials/pagination.html` | Controles de paginación Bootstrap reutilizables |
| 6 | `app/static/css/styles.css` | CSS mínimo: colores base, separación entre bloques, tamaño de imágenes y pequeños ajustes sobre Bootstrap. Evitar reinventar componentes |

**Checkpoint:** Todas las páginas ya tienen navbar, footer y estilos base. La app se ve coherente sin depender de CSS complejo.

---

## Fase F2: Home y catálogo básico (Días 3-6)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/partials/game_card.html` | Card Bootstrap simple: imagen, título, badges de género y plataforma, nota media si existe y enlace a detalle |
| 2 | `app/templates/main/home.html` | Cabecera simple con título, descripción corta y botón al catálogo. Debajo, grid de juegos destacados con `game_card` |
| 3 | `app/templates/games/catalog.html` | Formulario de filtros sencillo arriba, grid responsive de cards, texto de resultados, paginación y mensaje si no hay resultados |

**Checkpoint:** Home y catálogo se ven ordenados y son fáciles de mantener. Cards reutilizables funcionando.

---

## Fase F3: Ficha de juego (Días 6-8)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/games/detail.html` | Layout claro y simple: portada, datos básicos (developer, publisher, fecha, género, plataforma, status, enlace oficial), descripción, requisitos si existen, screenshots en grid simple si existen, zona de biblioteca, formulario de reseña y listado de reseñas |
| 2 | `app/static/js/main.js` | Solo JavaScript mínimo: confirm antes de eliminar y, como mucho, comprobación visual de passwords coinciden en registro |

**Checkpoint:** La ficha muestra toda la información importante sin componentes difíciles de mantener.

---

## Fase F4: Auth, perfil y biblioteca (Días 8-11)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/auth/login.html` | Card centrada con formulario estilizado, validación HTML5, token CSRF |
| 2 | `app/templates/auth/register.html` | Igual que login, con campos de registro y ayuda visual simple sobre las reglas básicas |
| 3 | `app/templates/profile/index.html` | Card de perfil con contadores y lista de reseñas recientes |
| 4 | `app/templates/library/my_library.html` | Lista o grid simple de juegos guardados, filtro por estado y controles inline para cambiar estado o quitar |

**Checkpoint:** Login, registro, perfil y biblioteca están maquetados con Bootstrap de forma clara y sin lógica visual compleja.

---

## Fase F5: Admin, errores y responsive (Días 11-14)

| Orden | Archivo | Qué hacer |
|-------|---------|-----------
| 1 | `app/templates/reviews/form.html` | Formulario de edición con campos pre-rellenados, select o radios simples para rating y textarea |
| 2 | `app/templates/admin/reviews.html` | Tabla/lista de moderación con botones claros. El botón "Actualizar catálogo" puede ser simple; la cuenta atrás visual es opcional |
| 3 | `app/templates/errors/404.html` y `500.html` | Páginas de error con estilo acorde al resto |
| 4 | Revisión responsive | Probar todas las páginas en móvil y corregir desbordes, columnas y navbar |

**Checkpoint:** Todas las páginas maquetadas.

---

## Fase F6: Extras solo si sobra tiempo (Días 14-15)

| Tarea | Detalle |
|-------|---------
| Estados vacíos | Mensajes amables: "Tu biblioteca está vacía", "No hay resultados para esta búsqueda", "Sé el primero en dejar una reseña" |
| Consistencia | Mismos paddings, márgenes, colores y tipografía en todas las páginas |
| Microinteracciones | Solo si todo lo demás ya está estable: hover suave en cards o pequeña mejora visual en botones |
| Favicon + logo | Añadir en static/img/ |
| Testing visual | Recorrer todos los flujos y verificar que nada se rompe visualmente |

> **Importante:** Si falta tiempo, esta fase se puede recortar sin problema. Lo obligatorio es que el frontend sea claro, funcional y responsive.

---

## CALENDARIO CONJUNTO

> Backend primero (Pablo Laya), frontend después (Pablo Pérez). No trabajan en paralelo en el código, pero Pablo Pérez puede ir preparando wireframes, paleta de colores y estructura CSS mientras Pablo Laya hace el backend.

| Semana | Pablo Laya (Backend) | Pablo Pérez (mientras tanto) |
|--------|-------------|--------------------------
| **Sem 1** | Fase 1 (cimientos + Docker) + Fase 2 (modelos) | Preparar wireframes sencillos en papel/Figma. Mirar ejemplos básicos de Bootstrap y entender cómo funciona un template Jinja2 |
| **Sem 2** | Fase 3 (seed completo) + Fase 4 (decorador + rutas públicas) | Pensar la estructura de `base.html`, navbar, cards y formularios sin meterse aún en detalles visuales complejos |
| **Sem 3** | Fase 5 (auth) + Fase 6 (rutas privadas + admin) | Estudiar Jinja2 básico (`{% block %}`, `{{ var }}`, `{% for %}`, `{% if %}`) y practicar con HTML simple |
| **Sem 4** | Fase 7 (errores + pulido) → **ENTREGA BACKEND** | **Empieza frontend:** Fases F1-F2 (base, home y catálogo) |
| **Sem 5** | Apoyo + revisión + testing conjunto | Fases F3-F5 (ficha, auth, biblioteca, admin, responsive) |
| **Sem 6** | Testing final + Docker limpio + escritura memoria | Testing final + últimos ajustes + escritura memoria |

---

## MOMENTO DE CONEXIÓN CLAVE

**Al terminar la Fase 7**, Pablo Laya le entrega a Pablo Pérez:

1. **El repo funcionando** con docker-compose up + seed
2. **Un documento de "contrato de variables"**: por cada template, qué variables Jinja2 recibe, su tipo y un ejemplo. Esto es clave para que Pablo Pérez no tenga que adivinar nada ni tocar Python. Así:

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

---

## PRINCIPIO DE TRABAJO PARA PABLO PEREZ

1. No tocar rutas, modelos ni lógica Python.
2. Si Bootstrap ya resuelve algo, usar Bootstrap y no inventar un componente nuevo.
3. Evitar JavaScript salvo para cosas muy simples.
4. Hacer primero que se vea bien en escritorio y después ajustar móvil.
5. Priorizar páginas completas y limpias antes que detalles visuales avanzados.
6. Si una mejora visual da problemas, se elimina. Mejor simple y estable que bonito y roto.
