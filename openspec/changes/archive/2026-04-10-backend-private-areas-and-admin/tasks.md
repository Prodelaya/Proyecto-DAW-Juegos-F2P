# Tasks: Áreas privadas SSR del usuario y administración moderada

## Phase 1: Foundation / Wiring

- [x] 1.1 Implementar `admin_required` en `app/decorators.py` con `@wraps`, check de `current_user.is_admin`, flash de error y redirect a `main_bp.home`, manteniendo el uso conjunto con `@login_required`.
- [x] 1.2 Registrar `reviews_bp`, `library_bp`, `profile_bp` y `admin_bp` en `app/routes/__init__.py` sin alterar el wiring ya existente de `main_bp`, `auth_bp` y `games_bp`.
- [x] 1.3 Ajustar `seeds/seed_games.py` para devolver un resumen operativo ligero reutilizable por admin/seed general, sin perder idempotencia ni tolerancia a fallos parciales.
- [x] 1.4 Crear `seeds/seed_library.py` con datos demo variados por usuario y por estado, respetando unicidad e idempotencia del dominio.
- [x] 1.5 Actualizar `seeds/seed_all.py` para orquestar `seed_library` después de usuarios/reseñas y reflejar el nuevo contrato de salida del seed.

## Phase 2: Hub privado en ficha + CRUD de reseñas

- [x] 2.1 Enriquecer `app/routes/games.py` para que `GET /juego/<id>` mantenga el contexto público actual y sume `own_review`, `library_entry`, flags y opciones privadas cuando `current_user.is_authenticated`.
- [x] 2.2 Implementar en `app/routes/reviews.py` `POST /juego/<game_id>/resena` con `@login_required`, validación explícita de `rating`/`text`, control de unicidad por `(user_id, game_id)`, flash funcional y redirect a ficha.
- [x] 2.3 Implementar en `app/routes/reviews.py` `GET|POST /resena/<id>/editar` verificando ownership, prefill SSR en `reviews/form.html`, actualización válida y redirect a la ficha del juego.
- [x] 2.4 Implementar en `app/routes/reviews.py` `POST /resena/<id>/eliminar` permitiendo borrar solo reseña propia, con feedback claro y retorno al contexto correcto.
- [x] 2.5 Actualizar `app/templates/games/detail.html` para combinar reseñas públicas + promedio con dos bloques privados separados: biblioteca y reseña propia.
- [x] 2.6 Actualizar `app/templates/reviews/form.html` con contrato SSR explícito (`game`, `review`, `mode`, `form_values`, `validation_errors`, `cancel_url`) y mensajes de error por campo.

## Phase 3: Biblioteca y perfil

- [x] 3.1 Implementar en `app/routes/library.py` `GET /mi-biblioteca` con `@login_required`, listado único, filtro por estado válido y empty state simple.
- [x] 3.2 Implementar en `app/routes/library.py` `POST /biblioteca/agregar/<game_id>` con alta progresiva a `want_to_play`, evitando duplicados y redirigiendo a la ficha.
- [x] 3.3 Implementar en `app/routes/library.py` `POST /biblioteca/estado/<id>` validando ownership, estados permitidos y retorno seguro al contexto origen o fallback a `/mi-biblioteca`.
- [x] 3.4 Implementar en `app/routes/library.py` `POST /biblioteca/quitar/<id>` con validación de ownership, flash funcional y retorno seguro al contexto origen o fallback a `/mi-biblioteca`.
- [x] 3.5 Actualizar `app/templates/library/my_library.html` para consumir `entries`, `current_status`, `available_statuses`, `has_results`, mostrando acciones POST y estado vacío útil.
- [x] 3.6 Implementar en `app/routes/profile.py` `GET /perfil` con datos básicos del usuario, contadores, últimas reseñas y accesos directos funcionales.
- [x] 3.7 Actualizar `app/templates/profile/index.html` para reflejar el contrato SSR simple del perfil sin convertirlo en dashboard complejo.

## Phase 4: Admin moderado y utilizable

- [x] 4.1 Implementar en `app/routes/admin.py` `GET /admin/resenas` con `@login_required + @admin_required`, listado global ordenado por fecha, contexto básico útil y estado vacío simple.
- [x] 4.2 Implementar en `app/routes/admin.py` `POST /admin/resenas/<id>/eliminar` para moderación de reseñas ajenas con feedback claro y redirect al panel admin.
- [x] 4.3 Implementar en `app/routes/admin.py` `POST /admin/actualizar-juegos` calculando cooldown desde `MAX(Game.cached_at)`, rechazando ejecuciones tempranas y mostrando feedback útil con resultado operativo.
- [x] 4.4 Actualizar `app/templates/admin/reviews.html` para reflejar tabla de moderación con autor, juego, rating, fecha, texto/extracto y estado del refresh admin.

## Phase 5: Contrato SSR, feedback y verificación manual

- [x] 5.1 Revisar los templates y rutas privadas tocadas para asegurar contratos SSR explícitos, mensajes flash funcionales y validaciones con errores específicos en reseñas, biblioteca y admin.
- [x] 5.2 Verificar el flujo privado principal con smoke SSR controlado: login → ficha autenticada → añadir a biblioteca → crear/editar/eliminar reseña → volver a ficha y comprobar gestión contextual.
- [x] 5.3 Verificar `/mi-biblioteca` y `/perfil` con smoke SSR controlado: filtros por estado, contadores, reseñas recientes, accesos directos y estados vacíos simples.
- [x] 5.4 Verificar el flujo admin con smoke SSR controlado: acceso protegido, listado de reseñas, borrado de moderación y refresh con cooldown + feedback útil.
- [x] 5.5 Confirmar explícitamente al cierre del change que siguen fuera de alcance dashboard complejo, vista dedicada de “mis reseñas”, acciones masivas admin, filtros admin avanzados, background jobs y UX enriquecida no esencial.

## Notas de verificación manual

- Estado real al cierre del change: **smoke runtime SSR ejecutado con Flask test client sobre SQLite temporal (21/21 checks OK)**. Esto NO sustituye una suite formal ni una validación manual humana paso a paso, pero sí deja evidencia runtime suficiente para cerrar este change a nivel TFG FP.

### 5.2 Flujo privado principal — smoke runtime cubierto

- [x] Login con usuario demo válido.
- [x] Abrir una ficha autenticada (`/juego/<id>`) y confirmar que conviven contenido público + bloques privados.
- [x] Agregar el juego a biblioteca desde la ficha y verificar feedback de éxito + reemplazo del CTA por controles de gestión.
- [x] Crear una reseña válida desde la ficha y verificar feedback de éxito.
- [x] Intentar crear una reseña inválida (rating vacío / texto < 10) y verificar errores específicos inline + feedback funcional.
- [x] Editar la reseña propia desde `/resena/<id>/editar`, guardar cambios y volver a la ficha.
- [x] Eliminar la reseña propia desde la ficha y confirmar retorno contextual correcto.

### 5.3 `/mi-biblioteca` y `/perfil` — smoke runtime cubierto

- [x] Abrir `/mi-biblioteca` sin filtro y verificar listado, estado vacío útil y acciones POST funcionales.
- [x] Probar filtros `want_to_play`, `playing` y `played` con datos demo; verificar empty state simple cuando corresponda.
- [x] Cambiar estado y quitar un juego verificando redirect seguro al contexto origen.
- [x] Abrir `/perfil` y verificar datos básicos, contadores, reseñas recientes y accesos directos.
- [x] Validar estados vacíos simples cuando falten resultados relevantes.

### 5.4 Flujo admin — smoke runtime cubierto

- [x] Confirmar que un usuario no admin autenticado recibe redirect + feedback al intentar entrar a `/admin/resenas`.
- [x] Confirmar que un admin autenticado puede abrir `/admin/resenas` y ver autor, juego, rating, fecha y extracto.
- [x] Eliminar una reseña ajena desde admin y verificar feedback de moderación exitosa.
- [x] Ejecutar `POST /admin/actualizar-juegos` fuera de cooldown y verificar feedback operativo (`processed` / `failed`).
- [x] Reintentar refresh dentro del cooldown y verificar rechazo explícito con segundos restantes.

### 5.5 Guardas de alcance confirmadas

- Sigue fuera de alcance un dashboard complejo de perfil.
- Sigue fuera de alcance una vista dedicada de “mis reseñas”.
- Siguen fuera de alcance acciones masivas admin y filtros admin avanzados.
- Siguen fuera de alcance background jobs para refresh de catálogo.
- Sigue fuera de alcance UX enriquecida no esencial para este change.
