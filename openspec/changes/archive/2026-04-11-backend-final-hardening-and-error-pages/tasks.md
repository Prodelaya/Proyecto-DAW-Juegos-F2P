# Tasks: Hardening final del backend y páginas de error

## Phase 1: Error handlers y páginas de error

- [x] 1.1 Registrar en `app/__init__.py` handlers de `404` y `500` conectados a templates SSR reales, manteniendo el wiring claro dentro de `create_app()`.
- [x] 1.2 Implementar `app/templates/errors/404.html` como página funcional, clara y coherente con la app, extendiendo `base.html`.
- [x] 1.3 Implementar `app/templates/errors/500.html` como página funcional, clara y coherente con la app, extendiendo `base.html`.
- [x] 1.4 Implementar en `app/__init__.py` un manejo pragmático de `CSRFError` con feedback claro y redirect seguro, sin abrir una arquitectura global de `400`.

## Phase 2: Auditoría de rutas POST, guards y validaciones

- [x] 2.1 Revisar `app/routes/auth.py` para confirmar validaciones, feedback, comportamiento de logout y protección efectiva de formularios POST.
- [x] 2.2 Revisar `app/routes/reviews.py` para confirmar validaciones de `rating`/`text`, ownership, feedback y rollback donde una escritura fallida pueda dejar sesión rota.
- [x] 2.3 Revisar `app/routes/library.py` para confirmar estados válidos, ownership, `next` seguro, feedback y rollback en escrituras.
- [x] 2.4 Revisar `app/routes/admin.py` para confirmar `@login_required + @admin_required`, feedback coherente, cooldown de refresh y rollback donde aplique.
- [x] 2.5 Revisar `app/decorators.py` para confirmar que el acceso denegado admin mantiene un comportamiento coherente con el resto del backend.
- [x] 2.6 Auditar todos los templates con formularios POST y parciales relacionados para confirmar presencia y consistencia del token CSRF.

## Phase 3: Robustez pública, seeds y escritura recuperable

- [x] 3.1 Revisar `app/routes/main.py` y `app/routes/games.py` para detectar y corregir inconsistencias claras de robustez o contexto SSR en rutas públicas, sin reabrir el alcance funcional.
- [x] 3.2 Revisar seeds relevantes (`seed_all.py`, `seed_games.py`, `seed_users.py`, `seed_reviews.py`, `seed_library.py`) para confirmar idempotencia y rollback en errores recuperables.
- [x] 3.3 Revisar puntos de escritura del backend para asegurar que no queda `db.session` contaminada tras fallos recuperables.

## Phase 4: Verificación operativa y cierre técnico

- [x] 4.1 Verificar runtime/controladamente las páginas `404` y `500` y confirmar que ya no quedan respuestas HTML crudas dentro del alcance previsto.
- [x] 4.2 Verificar runtime/controladamente el tratamiento de error CSRF y confirmar que el usuario recibe una respuesta más razonable que la cruda por defecto.
- [x] 4.3 Verificar runtime/controladamente rutas POST críticas (auth, reseñas, biblioteca, admin) para confirmar guards, validaciones, feedback y no regresión funcional.
- [x] 4.4 Verificar el seed general como idempotente y el arranque limpio con Docker como criterio real de cierre backend.
- [x] 4.5 Documentar en las notas de verificación qué quedó validado de forma real y qué sigue fuera de alcance.
- [x] 4.6 Confirmar explícitamente que el backend puede considerarse 100% terminado para dar paso al frontend del roadmap.

## Phase 5: Fix de bootstrap Docker limpio

- [x] 5.1 Implementar una espera explícita a disponibilidad real de PostgreSQL antes de arrancar Flask en el contenedor `web`, sin mover esa lógica a `create_app()`.
- [x] 5.2 Revalidar `docker-compose down -v` + `docker-compose up --build -d` para confirmar que `web` ya no requiere `restart` manual y que la app queda operativa tras seed.
- [x] 5.3 Actualizar las notas de verificación y el cierre técnico final según el resultado real del bootstrap limpio corregido.

## Notas de verificación manual

- 2026-04-10 — Verificación runtime/controlada ejecutada dentro del contenedor `web` con `docker-compose exec -T web python` sobre una SQLite aislada (`/tmp/phase4_verify.sqlite`) para no contaminar la base compartida del stack principal.
- 2026-04-10 — `404` validado con `GET /ruta-inexistente-phase4` → `404` + copy SSR de `errors/404.html`; `500` validado con ruta controlada `GET /__force_500` → `500` + copy SSR de `errors/500.html` sin filtrar el texto de la excepción controlada al HTML final.
- 2026-04-10 — `CSRFError` validado con `POST /login` sin `csrf_token` y `Referer` local → redirect de vuelta a `/login` con flash `Tu sesión del formulario expiró o la solicitud no era válida...`; no apareció la respuesta cruda por defecto de Flask-WTF.
- 2026-04-10 — POSTs críticos validados realmente:
  - Auth: `POST /registro` inválido muestra errores server-side; `POST /login` válido respeta `next=/perfil` y mantiene feedback de bienvenida.
  - Reseñas: `POST /juego/<id>/resena` sin sesión redirige a login; con sesión y payload inválido devuelve `400` con flash + errores de rating/text.
  - Biblioteca: `POST /biblioteca/estado/<id>` con estado inválido redirige con flash de validación.
  - Admin: acceso no admin a `/admin/resenas` redirige a home con flash; `POST /admin/resenas/<id>/eliminar` elimina realmente la reseña; `POST /admin/actualizar-juegos` con cooldown activo devuelve feedback coherente.
- 2026-04-10 — Seed general verificado como idempotente en runtime controlado parcheando la integración externa de FreeToGame para usar payload estable: dos ejecuciones consecutivas de `seed_all()` dejaron los mismos conteos (`users=8`, `games=4`, `reviews=24`, `library=24`).
- 2026-04-11 — Verificación Docker destructiva ejecutada realmente con `docker-compose down -v && docker-compose up --build -d` desde volumen PostgreSQL vacío. Resultado inicial HONESTO: `db` levantó bien, pero `web` quedó en `Exit 1` durante el primer arranque.
- 2026-04-11 — Evidencia del fallo inicial: `docker-compose logs --no-color web` mostró `sqlalchemy.exc.OperationalError` / `psycopg2.OperationalError` (`connection to server at "db" ... failed: Connection refused`) porque `create_app()` intentó `db.create_all()` antes de que PostgreSQL aceptara conexiones. Tras esperar `pg_isready`, un `docker-compose restart web` dejó ambos servicios en `Up`.
- 2026-04-11 — Seed general ejecutado realmente en el contenedor `web` ya recuperado: `docker-compose exec -T web python seeds/seed_all.py` → `juegos=405`, `usuarios=6`, `reseñas=50`, `biblioteca=30`, sin fallos reportados por el script.
- 2026-04-11 — Comprobación mínima real de app funcional: `curl -sS -D - http://127.0.0.1:5000/` → `HTTP/1.1 200 OK` y HTML SSR completo de la home.
- 2026-04-11 — Bootstrap Docker limpio REVALIDADO tras el fix: `docker-compose down -v && docker-compose up --build -d` desde volumen PostgreSQL vacío dejó `db` y `web` en `Up` sin `restart` manual (`docker-compose ps`). El log real de `web` mostró la espera explícita (`[wait_for_postgres] PostgreSQL todavía no acepta conexiones...`) y luego el arranque correcto (`PostgreSQL disponible. Iniciando aplicación...` + `Running on http://127.0.0.1:5000`).
- 2026-04-11 — Seed y operatividad revalidados sobre el bootstrap corregido: `docker-compose exec -T web python seeds/seed_all.py` completó OK (`juegos=405`, `usuarios=6`, `reseñas=50`, `biblioteca=30`) y `curl -sS -D - http://127.0.0.1:5000/` devolvió `HTTP/1.1 200 OK` con la home SSR sin intervención manual adicional.
- Fuera de alcance / no validado como hecho: no se ejecutó en esta pasada una batería formal de tests automatizados/CI ni se amplió el alcance a frontend.
- Cierre técnico explícito: el bloqueo operativo del bootstrap limpio con Docker quedó corregido y la revalidación destructiva real confirmó que `web` ya no requiere recuperación manual tras esperar disponibilidad real de PostgreSQL. Con la evidencia runtime/controlada ya recogida (errores, CSRF, POSTs críticos, idempotencia seed y bootstrap limpio), el backend puede considerarse **100% terminado dentro del alcance del proyecto** y listo para dar paso al frontend del roadmap. Lo único que sigue fuera de alcance en estas notas es introducir tests automatizados/CI o trabajo de frontend.
