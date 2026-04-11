# Roadmap Frontend — handoff simple y seguro

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Guía de implementación frontend](06-Guia-implementacion-frontend.md)

> **Importante:** para implementar el frontend, el documento que se debe seguir es **`docs/06-Guia-implementacion-frontend.md`**. Este roadmap queda como contexto general del proyecto, no como guía paso a paso.

## Estado real del proyecto hoy

El frontend base **ya existe** y está funcionando con renderizado server-side (SSR):

- ya existe `app/templates/base.html`
- ya existen partials reutilizables (`navbar.html`, `footer.html`, `flash_messages.html`, `pagination.html`, `game_card.html`, `csrf_input.html`)
- ya existen todas las pantallas principales del proyecto
- ya existe Bootstrap por CDN y una estructura visual funcional

### Entonces, ¿cuál es el trabajo frontend real?

**No** hay que inventar el frontend desde cero.

El trabajo correcto es:

1. **pulir la maquetación**
2. **mejorar orden visual y responsive**
3. **mantener los contratos Jinja ya existentes**
4. **no tocar backend, Python, Docker ni despliegue**

---

## Regla de oro

Si una pantalla ya funciona pero se ve simple, el objetivo es **dejarla más clara y prolija sin romper nada**.

Prioridad técnica:

1. **Bootstrap**
2. **HTML limpio**
3. **Jinja simple, sin inventar variables**
4. **CSS corto y seguro**
5. **JS mínimo y opcional**

---

## Qué NO se toca en la fase frontend

No tocar:

- archivos `.py`
- Docker
- base de datos
- seeds
- rutas Flask
- nombres de variables Jinja
- acciones `POST`
- `csrf_token`
- hidden inputs como `next`, `page` o similares

Si algo visual parece raro pero depende de una variable o de un formulario, **no lo renombres ni lo borres**. Primero revisa la guía de implementación frontend.

---

## Fase 1 — Layout global y consistencia visual

### Objetivo

Dejar una base visual prolija y consistente para todo el sitio.

### Archivos frontend a tocar

- `app/templates/base.html`
- `app/templates/partials/navbar.html`
- `app/templates/partials/footer.html`
- `app/templates/partials/flash_messages.html`
- `app/templates/partials/game_card.html`
- `app/templates/partials/pagination.html`
- `app/static/css/styles.css`

### Qué sí hacer

- mejorar espaciados
- mejorar jerarquía visual de títulos
- ordenar navbar y footer
- mantener responsive de Bootstrap
- hacer que cards, alertas y paginación se vean consistentes

### Qué no romper

- links de `url_for(...)`
- include de partials
- estructura de bloques Jinja (`block title`, `block content`)
- botón/formulario de logout con `POST`
- include `partials/csrf_input.html`
- uso de `current_filters` dentro de la paginación

### Checklist simple

- [ ] `base.html` sigue cargando Bootstrap y `styles.css`
- [ ] navbar se ve bien en desktop y móvil
- [ ] footer sigue apareciendo en todas las pantallas
- [ ] flashes siguen visibles
- [ ] cards de juego siguen mostrando imagen, título, rating y link
- [ ] paginación sigue funcionando con filtros activos

### Resultado esperado

Toda la app se siente parte del mismo sitio y ninguna pantalla pierde funcionalidad.

---

## Fase 2 — Home y catálogo público

### Objetivo

Dejar ordenadas las pantallas públicas más importantes sin tocar la lógica de filtros.

### Archivos frontend a tocar

- `app/templates/main/home.html`
- `app/templates/games/catalog.html`
- `app/templates/partials/game_card.html`
- `app/static/css/styles.css`

### Variables reales que ya existen

#### `main/home.html`

- `featured_games`
- `catalog_url`
- `featured_fallback_message`

#### `games/catalog.html`

- `games`
- `pagination`
- `current_filters`
- `filter_options`
- `total_count`
- `has_results`

### Qué sí hacer

- mejorar encabezado de home
- ordenar visualmente el bloque de destacados
- mejorar lectura del formulario de filtros
- cuidar alineación de botones, selects e inputs
- mantener el catálogo fácil de entender

### Qué no romper

- `name="q"`, `name="genre"`, `name="platform"`, `name="publisher"`, `name="sort"`
- hidden input `page`
- loops de `filter_options.genres`, `filter_options.platforms`, `filter_options.publishers`
- lecturas de `current_filters.q`, `current_filters.genre`, etc.

### Checklist simple

- [ ] el form sigue siendo `method="get"`
- [ ] los filtros mantienen el valor seleccionado
- [ ] el botón de reset sigue yendo al catálogo limpio
- [ ] los juegos siguen listando bien
- [ ] la paginación sigue respetando filtros activos
- [ ] el estado sin resultados sigue visible

### Resultado esperado

Home y catálogo prolijos, claros y fáciles de mantener por alguien principiante.

---

## Fase 3 — Ficha de juego

### Objetivo

Mejorar la pantalla más completa del proyecto sin romper formularios privados.

### Archivos frontend a tocar

- `app/templates/games/detail.html`
- `app/static/css/styles.css`
- `app/static/js/main.js` **solo si hace falta algo mínimo y seguro**

### Variables reales que ya existen

- `game`
- `reviews`
- `review_summary`
- `screenshots`
- `requirements`
- `has_requirements`
- `own_review`
- `library_entry`
- `library_status_options`
- `library_status_labels`
- `can_manage_private`
- `review_form_values`
- `review_validation_errors`

### Qué sí hacer

- ordenar portada + datos principales
- mejorar lectura de badges, descripción y requisitos
- ordenar screenshots en grilla simple
- hacer más clara la zona de biblioteca y reseña

### Qué no romper

- formularios `POST`
- includes de `partials/csrf_input.html`
- hidden input `next`
- `name="status"`, `name="rating"`, `name="text"`
- condiciones Jinja como `if can_manage_private`, `if own_review`, `if library_entry`

### Checklist simple

- [ ] el usuario anónimo sigue viendo solo la parte pública
- [ ] el usuario logueado sigue viendo biblioteca y reseña propia
- [ ] agregar/quitar biblioteca sigue con CSRF
- [ ] crear/eliminar reseña sigue con CSRF
- [ ] errores de validación siguen apareciendo
- [ ] screenshots y requisitos no se rompen si faltan datos

### Resultado esperado

La ficha se ve completa, ordenada y estable, sin tocar contratos backend.

---

## Fase 4 — Login, registro, perfil y biblioteca

### Objetivo

Pulir pantallas privadas frecuentes con Bootstrap simple.

### Archivos frontend a tocar

- `app/templates/auth/login.html`
- `app/templates/auth/register.html`
- `app/templates/profile/index.html`
- `app/templates/library/my_library.html`
- `app/static/css/styles.css`

### Variables reales que ya existen

#### `auth/login.html`

- `form_data`
- `errors`
- `general_error`
- `next_value`

#### `auth/register.html`

- `form_data`
- `errors`

#### `profile/index.html`

- `user`
- `stats`
- `recent_reviews`
- `links`

#### `library/my_library.html`

- `entries`
- `current_status`
- `available_statuses`
- `has_results`

### Qué sí hacer

- mejorar legibilidad de formularios
- mantener feedback de error bien visible
- ordenar bloques de perfil
- hacer más cómoda la lectura de la biblioteca

### Qué no romper

- hidden input `next` del login
- `csrf_token` en formularios
- `name` reales de cada campo del formulario
- botones/filtros de estado en biblioteca
- formularios inline para cambiar estado o quitar un juego

### Checklist simple

- [ ] login mantiene `email`, `password` y `next`
- [ ] register mantiene `username`, `email`, `password`, `confirm_password`
- [ ] biblioteca sigue filtrando por `status`
- [ ] cambiar estado sigue funcionando
- [ ] quitar juego sigue funcionando
- [ ] perfil sigue mostrando stats y reseñas recientes

### Resultado esperado

Las pantallas privadas quedan claras y usables sin meter lógica nueva.

---

## Fase 5 — Admin, reseñas editables y errores

### Objetivo

Cerrar el frontend con las pantallas menos frecuentes pero importantes.

### Archivos frontend a tocar

- `app/templates/admin/reviews.html`
- `app/templates/reviews/form.html`
- `app/templates/errors/404.html`
- `app/templates/errors/500.html`
- `app/static/css/styles.css`

### Variables reales que ya existen

#### `admin/reviews.html`

- `reviews`
- `has_results`
- `refresh_status`

#### `reviews/form.html`

- `game`
- `review`
- `mode`
- `form_values`
- `validation_errors`
- `cancel_url`

### Qué sí hacer

- mejorar tabla/listado admin
- hacer más visible el estado de cooldown de actualización
- dejar claro el formulario de edición de reseña
- alinear visualmente las pantallas de error con el resto del sitio

### Qué no romper

- form `POST` de eliminar reseña admin
- form `POST` de actualizar catálogo
- include `partials/csrf_input.html`
- lógica visual basada en `refresh_status.cooldown_active`
- inputs de edición de reseña

### Checklist simple

- [ ] admin sigue mostrando reseñas
- [ ] botón de actualizar catálogo no pierde el `POST`
- [ ] delete admin sigue con CSRF
- [ ] editar reseña sigue mostrando valores previos
- [ ] 404 y 500 siguen extendiendo `base.html`

### Resultado esperado

El frontend queda completo y coherente en todas las pantallas principales.

---

## Recomendación final de trabajo

Orden sugerido:

1. primero `styles.css` + layout global
2. después home y catálogo
3. después ficha de juego
4. después auth, perfil y biblioteca
5. al final admin y errores

No intentes hacer todo junto.

**Pantalla por pantalla. Cambio chico, controlado y fácil de revisar.**

---

## Definición de “terminado” para la fase frontend

Se considera bien hecho si:

- todas las pantallas SSR siguen renderizando
- no se cambiaron contratos Jinja
- no se tocó Python ni Docker
- todos los formularios `POST` conservaron CSRF e inputs ocultos
- Bootstrap resuelve casi toda la interfaz
- el resultado es claro, simple, responsive y mantenible por un novato
