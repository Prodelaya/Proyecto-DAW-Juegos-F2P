# Tasks: Autenticación SSR base y visibilidad de sesión

## Phase 1: Foundation / Wiring

- [x] 1.1 Ajustar `app/extensions.py` para dejar `login_manager.login_view` y `login_manager.login_message` efectivos y consistentes con el contrato de rutas protegidas futuras.
- [x] 1.2 Registrar `auth_bp` en `app/routes/__init__.py` y validar en `app/__init__.py` que el blueprint quede cableado sin agregar nuevas extensiones ni ampliar alcance.

## Phase 2: Rutas y reglas de autenticación

- [x] 2.1 Implementar en `app/routes/auth.py` los guards SSR para redirigir a `/` si `current_user.is_authenticated` accede a `GET /login` o `GET /registro`.
- [x] 2.2 Implementar `GET|POST /registro` en `app/routes/auth.py` con lectura de `request.form`, re-render SSR y preservación de valores no sensibles.
- [x] 2.3 Agregar validaciones de registro en `app/routes/auth.py`: `username`, `email`, `password` mínima 8, `confirm_password` y unicidad con mensajes específicos por campo duplicado.
- [x] 2.4 Completar persistencia de registro en `app/routes/auth.py` usando password hasheada, feedback de éxito y redirect obligatorio a `/login`.
- [x] 2.5 Implementar `GET|POST /login` en `app/routes/auth.py` usando solo `email` + `password`, con errores específicos de campos/formato y mensaje genérico para credenciales inválidas.
- [x] 2.6 Agregar resolución segura de `next` en `app/routes/auth.py` para redirigir tras login a un destino válido o fallback a `/`.
- [x] 2.7 Implementar `POST /logout` en `app/routes/auth.py` con `@login_required`, CSRF y redirect a `/`, sin aceptar `GET`.

## Phase 3: Contrato SSR y visibilidad de sesión

- [x] 3.1 Actualizar `app/templates/auth/register.html` con contrato SSR mínimo: formulario POST, `csrf_token`, campos requeridos, errores por campo y enlace a login.
- [x] 3.2 Actualizar `app/templates/auth/login.html` con contrato SSR mínimo: formulario POST, `csrf_token`, `email`, `password`, error general y enlace a registro.
- [x] 3.3 Actualizar `app/templates/partials/navbar.html` para alternar entre estado anónimo y autenticado mostrando `username` y un logout por POST con CSRF, sin `email`, UI admin ni CTAs pasivos.
- [x] 3.4 Validar `app/templates/base.html` para conservar inclusión de navbar/flashes y evitar introducir reseñas, biblioteca, perfil o secciones privadas fuera de scope.

## Phase 4: Verificación manual y cierre de alcance

- [x] 4.1 Verificar manualmente registro SSR: alta válida, password corta, confirmación inválida y duplicados separados de `username`/`email`.
- [x] 4.2 Verificar manualmente login/logout y sesión visible: login válido, errores de formato, credenciales inválidas genéricas, redirect con `next` seguro, guards en `/login` y `/registro`, logout POST con CSRF y navbar autenticada.
- [x] 4.3 Confirmar explícitamente al cerrar el change que quedan fuera de alcance reseñas, biblioteca, perfil, admin UI y CTAs pasivos.

## Notas de verificación manual

- Registro SSR verificado en runtime: alta válida con redirect a `/login`, password hasheada, password corta y confirmación inválida con errores específicos, y duplicados separados para `username` y `email`.
- Login/logout y visibilidad de sesión verificados en runtime: login válido, errores específicos de formato, mensaje genérico para credenciales inválidas, redirect con `next` local seguro, guards para usuarios autenticados en `/login` y `/registro`, `GET /logout` rechazado con `405`, `POST /logout` sin CSRF rechazado con `400` y logout correcto por `POST` con CSRF.
- Cierre de alcance confirmado: el change mantiene fuera de scope reseñas, biblioteca, perfil, admin UI y CTAs pasivos; el blueprint registrado sigue limitado a auth base y visibilidad de sesión en navbar.
