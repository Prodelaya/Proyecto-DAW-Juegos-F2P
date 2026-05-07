# Cambios frontend: tema oscuro gaming y navegación privada

Este documento resume los cambios visuales aplicados en la rama frontend. El objetivo es mejorar la estética de la aplicación sin alterar los contratos SSR de Flask/Jinja: rutas, formularios POST, CSRF, nombres de inputs y variables de template se mantienen.

## Resumen

- Se aplicó un tema oscuro inspirado en Steam sobre Bootstrap.
- Se añadieron accesos visibles para usuarios autenticados: perfil, biblioteca y administración cuando corresponda.
- Se unificó el copy visible a español neutral de España.
- Se mejoró la experiencia del botón de actualización de catálogo para evitar dudas durante una operación lenta.
- Se revisó el CSS para reducir overrides globales y evitar pisar componentes Bootstrap de forma innecesaria.

## Paleta visual

| Uso | Color |
|---|---|
| Fondo principal | `#1b2838` |
| Fondo oscuro secundario | `#0e141b` |
| Acento azul | `#66c0f4` |
| Acción primaria | `#4c6b22` |
| Texto claro | `#c7d5e0` |
| Texto gris | `#8f98a0` |

## Cambios principales por área

### Layout base

- `app/templates/base.html`
  - Cambia el fondo global a oscuro.
  - Añade un bloque `scripts` para que cada página pueda incluir JavaScript específico sin tocar el layout de nuevo.

### Navegación

- `app/templates/partials/navbar.html`
  - El nombre del usuario autenticado enlaza a `/perfil`.
  - Se añade acceso a `Mi biblioteca`.
  - Si el usuario es administrador, se muestra `Administración`.

### Tema visual

- `app/static/css/styles.css`
  - Define variables de color del tema.
  - Ajusta navbar, botones, formularios, paginación, hero y cards oscuras explícitas.
  - Evita reglas globales peligrosas como redefinir `.container` o forzar todos los `.badge` con `!important`.

### Páginas modificadas

- `app/templates/main/home.html`
- `app/templates/games/catalog.html`
- `app/templates/games/detail.html`
- `app/templates/library/my_library.html`
- `app/templates/profile/index.html`
- `app/templates/admin/reviews.html`
- `app/templates/auth/login.html`
- `app/templates/auth/register.html`
- `app/templates/reviews/form.html`
- `app/templates/errors/404.html`
- `app/templates/errors/500.html`
- `app/templates/partials/footer.html`

### Mensajes visibles del servidor

También se actualizaron mensajes flash y validaciones visibles para mantener el español neutral de España. No se ha cambiado la lógica de negocio.

- `app/routes/auth.py`
- `app/routes/library.py`
- `app/routes/reviews.py`
- `app/routes/admin.py`
- `app/decorators.py`
- `app/extensions.py`

## Validación funcional esperada

- Las variables Jinja se mantienen.
- Las rutas `url_for(...)` se mantienen.
- Los formularios POST conservan CSRF.
- Los inputs ocultos usados para redirección se conservan.
- No se introducen llamadas API públicas nuevas.
- La actualización de catálogo sigue usando el flujo SSR existente.

## Nota sobre rendimiento del catálogo

La actualización del catálogo puede tardar porque el backend consulta el listado completo de FreeToGame y después obtiene el detalle de cada juego. En esta rama solo se mejora la experiencia de espera del botón; optimizar la sincronización sería un cambio backend separado.
