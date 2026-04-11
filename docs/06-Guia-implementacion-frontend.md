# Guía de implementación frontend

> **Este es el documento principal de trabajo para frontend.** Si vas a implementar pantallas, usa esta guía y no hace falta ir saltando entre otros documentos.

> Esta guía existe para trabajar el frontend de este proyecto **sin romper el backend, Jinja, formularios ni Docker**.

## 1. Qué es lo que YA está construido

Hoy el proyecto ya tiene:

- layout base en `app/templates/base.html`
- Bootstrap funcionando
- partials reutilizables
- home
- catálogo
- detalle de juego
- login y registro
- perfil
- biblioteca
- panel admin
- páginas de error
- CSS y JS base

### Traducción simple

No tienes que crear la app de cero.

Tu trabajo es **mejorar cómo se ve** y **ordenar mejor el HTML**, pero respetando lo que ya existe.

---

## 2. Qué puedes tocar

Puedes tocar estos archivos frontend:

- `app/templates/base.html`
- `app/templates/main/home.html`
- `app/templates/games/catalog.html`
- `app/templates/games/detail.html`
- `app/templates/auth/login.html`
- `app/templates/auth/register.html`
- `app/templates/profile/index.html`
- `app/templates/library/my_library.html`
- `app/templates/admin/reviews.html`
- `app/templates/reviews/form.html`
- `app/templates/errors/404.html`
- `app/templates/errors/500.html`
- `app/templates/partials/*.html`
- `app/static/css/styles.css`
- `app/static/js/main.js` solo si el cambio es muy pequeño y seguro

### Qué tipo de cambios sí sirven

- mejorar márgenes y paddings
- cambiar clases Bootstrap
- reordenar columnas con `row` y `col`
- mejorar títulos, subtítulos y bloques visuales
- hacer una pantalla más clara en móvil
- mejorar estados vacíos
- hacer formularios más legibles

---

## 3. Qué NO debes tocar nunca

No toques nunca:

- archivos Python (`.py`)
- Docker (`Dockerfile`, `docker-compose.yml`)
- base de datos
- seeds
- nombres de variables Jinja
- rutas `url_for(...)` salvo que solo cambies clases alrededor
- `method="post"` de formularios
- hidden inputs
- `csrf_token`

### Regla importante

Si ves algo como esto:

```html
{% include 'partials/csrf_input.html' %}
<input type="hidden" name="next" value="...">
```

**NO lo borres. NO lo renombres. NO lo muevas porque sí.**

Eso no está “de más”. Eso hace que el backend siga funcionando bien.

---

## 4. Cómo trabajar sin romper backend

### Regla 1

Cambiar clases Bootstrap: **sí**.

Cambiar nombres de variables Jinja: **no**.

### Regla 2

Si un template usa `{{ current_filters.q }}` o `{{ review_summary.count }}` o `{{ own_review.text }}`:

- puedes moverlo de lugar en la pantalla
- puedes envolverlo en `div`, `card`, `row`, `col`
- puedes cambiar clases CSS
- **no puedes cambiarle el nombre**

### Regla 3

Si un formulario tiene `name="email"`, `name="password"`, `name="status"`, `name="rating"` o `name="text"`, esos nombres se quedan así.

### Regla 4

Si algo ya funciona, no lo “reescribas mejor”.

Primero hazlo **más claro**. Después, si sigue siendo seguro, entonces ya lo mejoras visualmente.

---

## 5. Contratos reales que ya usa el proyecto

Esta parte es CLAVE. Estos nombres ya existen. No inventes otros.

### `games/catalog.html`

- `games`
- `pagination`
- `current_filters`
- `filter_options`
- `total_count`
- `has_results`

Dentro de `current_filters` se usan:

- `current_filters.q`
- `current_filters.genre`
- `current_filters.platform`
- `current_filters.publisher`
- `current_filters.sort`
- `current_filters.page`

Dentro de `filter_options` se usan:

- `filter_options.genres`
- `filter_options.platforms`
- `filter_options.publishers`

### `games/detail.html`

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

### `main/home.html`

- `featured_games`
- `catalog_url`
- `featured_fallback_message`

### `auth/login.html`

- `form_data`
- `errors`
- `general_error`
- `next_value`

### `auth/register.html`

- `form_data`
- `errors`

### `profile/index.html`

- `user`
- `stats`
- `recent_reviews`
- `links`

### `library/my_library.html`

- `entries`
- `current_status`
- `available_statuses`
- `has_results`

### `admin/reviews.html`

- `reviews`
- `has_results`
- `refresh_status`

### `reviews/form.html`

- `game`
- `review`
- `mode`
- `form_values`
- `validation_errors`
- `cancel_url`

---

## 6. Formularios: la zona más delicada

Si vas a tocar formularios, presta MUCHÍSIMA atención.

### Nunca rompas estas cosas

#### A. El `method="post"`

Si hoy un formulario es POST, sigue siendo POST.

#### B. El CSRF

Si aparece esto:

```html
{% include 'partials/csrf_input.html' %}
```

se deja.

#### C. Los hidden inputs

Ejemplos reales del proyecto:

- `<input type="hidden" name="page" value="1">`
- `<input type="hidden" name="next" value="...">`

Eso tampoco se toca salvo que entiendas PERFECTO por qué está.

#### D. Los `name="..."`

Estos nombres conectan HTML con backend.

Ejemplos reales:

- `email`
- `password`
- `confirm_password`
- `username`
- `q`
- `genre`
- `platform`
- `publisher`
- `sort`
- `status`
- `rating`
- `text`

No los cambies.

---

## 7. Bootstrap primero, CSS complejo después, JS opcional mínimo

Orden correcto:

1. resuelve con Bootstrap
2. si falta algo, agrega CSS corto en `styles.css`
3. si todavía falta algo, piensa si realmente vale la pena
4. JS solo si es mínimo y seguro

### Buen enfoque

- `container`
- `row`
- `col`
- `card`
- `btn`
- `alert`
- `badge`
- `table-responsive`
- `form-control`
- `form-select`
- `d-flex`
- `gap-*`
- `mb-*`, `py-*`, `px-*`

### Mal enfoque

- rehacer componentes enteros con CSS custom innecesario
- meter animaciones raras
- meter JavaScript para cosas que Bootstrap ya resuelve
- romper una pantalla por querer dejarla “más moderna”

---

## 8. Qué revisar antes de guardar cambios

Antes de cerrar una pantalla, revisa esto:

- [ ] ¿sigues usando las mismas variables Jinja?
- [ ] ¿no borraste ningún `url_for(...)`?
- [ ] ¿no borraste ningún `csrf_input`?
- [ ] ¿no borraste hidden inputs?
- [ ] ¿los `name="..."` de inputs siguen iguales?
- [ ] ¿la pantalla se entiende mejor que antes?
- [ ] ¿en móvil no explota nada raro?
- [ ] ¿Bootstrap resuelve casi todo?
- [ ] ¿el cambio es simple de mantener?

---

## 9. Fases de trabajo sugeridas

No hace falta consultar el roadmap para implementar estas fases. Aquí ya tienes el orden recomendado, los archivos a tocar y el resultado esperado en cada paso.

## Fase 1 — Base visual general

### Archivos

- `base.html`
- `partials/navbar.html`
- `partials/footer.html`
- `partials/flash_messages.html`
- `partials/game_card.html`
- `partials/pagination.html`
- `styles.css`

### Resultado esperado al terminar

Todo el sitio tiene una base visual consistente.

---

## Fase 2 — Home y catálogo

### Archivos

- `main/home.html`
- `games/catalog.html`
- `partials/game_card.html`
- `styles.css`

### Resultado esperado al terminar

La parte pública principal se ve clara, ordenada y responsive.

---

## Fase 3 — Detalle de juego

### Archivos

- `games/detail.html`
- `styles.css`

### Resultado esperado al terminar

La ficha del juego se entiende rápido y no rompe ni biblioteca ni reseñas.

---

## Fase 4 — Login, registro, perfil y biblioteca

### Archivos

- `auth/login.html`
- `auth/register.html`
- `profile/index.html`
- `library/my_library.html`
- `styles.css`

### Resultado esperado al terminar

Las pantallas privadas quedan claras y cómodas para usar.

---

## Fase 5 — Admin, edición de reseña y errores

### Archivos

- `admin/reviews.html`
- `reviews/form.html`
- `errors/404.html`
- `errors/500.html`
- `styles.css`

### Resultado esperado al terminar

El frontend queda completo, consistente y listo para entregar.

---

## 10. Mini checklist final antes de entregar una pantalla

- [ ] no toqué Python
- [ ] no toqué Docker
- [ ] no inventé variables Jinja nuevas
- [ ] no cambié nombres de inputs
- [ ] no borré CSRF
- [ ] no borré hidden inputs
- [ ] usé Bootstrap como base
- [ ] el CSS agregado es corto y razonable
- [ ] la pantalla se ve mejor que antes
- [ ] sigue siendo fácil de mantener por alguien principiante

---

## 11. Si dudas, haz esto

Si no sabes si algo se puede tocar:

1. no lo borres
2. no lo renombres
3. cambia solo clases Bootstrap alrededor
4. deja la lógica Jinja como está

Con eso ya evitás la mayoría de los errores graves.

---

## 12. Resumen brutalmente simple

Tu objetivo NO es programar backend.

Tu objetivo es este:

**tomar pantallas que ya funcionan, ordenarlas visualmente, hacerlas más claras y mantener intacta la conexión con Flask/Jinja.**

Si sigues esa regla, vas bien.
