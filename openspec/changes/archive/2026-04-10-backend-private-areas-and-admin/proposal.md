# Propuesta — `backend-private-areas-and-admin`

## Estado
draft

## Título
Implementar áreas privadas SSR del usuario y administración moderada

## Intención

Cerrar el flujo privado principal del producto sobre la base ya existente de catálogo público y autenticación SSR, permitiendo que el usuario autenticado gestione su relación con un juego desde la ficha (`reseña` + `biblioteca`), consulte un perfil simple y que el administrador disponga de un panel moderado y utilizable, todo dentro de un alcance realista para TFG nivel FP.

## Problema

La aplicación ya cuenta con modelos de dominio, seed de juegos y reseñas, catálogo público SSR y autenticación base, pero todavía no existe un flujo privado coherente para el usuario autenticado. Hoy no puede gestionar su reseña desde la ficha, organizar su biblioteca personal, consultar un perfil útil ni existe una superficie admin operativa para moderar reseñas y refrescar catálogo. Sin este change, el producto queda partido entre catálogo público y login, pero sin experiencia privada con valor real.

## Alcance

Incluye: usar la ficha del juego como hub privado del usuario autenticado; CRUD completo de reseña propia respetando la unicidad `(user_id, game_id)` y mostrando edición/eliminación cuando la reseña ya existe; biblioteca completa con agregar, cambiar estado y quitar, usando los estados cerrados del dominio; vista `/mi-biblioteca` como lista única filtrable por estado; perfil SSR simple con datos del usuario, contadores y accesos directos útiles; mantenimiento de promedio y reseñas públicas en la ficha autenticada, sumando bloques privados separados para biblioteca y reseña; panel admin moderado con listado global de reseñas mostrando autor, juego, rating, fecha y texto/extracto, más eliminación y acción de actualizar catálogo con cooldown y feedback útil; `seed_library` útil y variado para sostener demo y validación; contratos SSR explícitos y acotados para vistas privadas; flash messages claros, validaciones con mensajes específicos y estados vacíos simples con mensaje útil.

## Fuera de alcance

Dashboard complejo de perfil, vista específica de “mis reseñas”, acciones masivas admin, filtros avanzados en panel admin, background jobs para refresh de catálogo, UX enriquecida no esencial, métricas complejas, auditoría avanzada o cualquier expansión que convierta este change en un backoffice sobredimensionado.

## Criterios de aceptación

1. Usuario autenticado puede crear, editar y eliminar su propia reseña desde la ficha del juego, con validaciones server-side y mensajes específicos por error.
2. Si ya existe reseña del usuario para ese juego, la ficha muestra su reseña actual y ofrece editar/eliminar en lugar de una nueva alta redundante.
3. Usuario autenticado puede añadir un juego a su biblioteca desde la ficha; una vez añadido, puede cambiar estado o quitarlo.
4. `/mi-biblioteca` muestra una lista única filtrable por estado (`want_to_play`, `playing`, `played`).
5. `/perfil` funciona como resumen simple: datos básicos, contadores y accesos directos útiles al flujo privado.
6. La ficha autenticada mantiene visibles el promedio y las reseñas públicas del juego, añadiendo bloques privados separados para biblioteca y reseña propia.
7. El panel admin permite listar reseñas globales con contexto básico útil, eliminar una reseña y lanzar actualización de catálogo con cooldown y feedback operativo.
8. `seed_library` genera datos demo variados e idempotentes que permiten probar biblioteca y perfil sin depender de carga manual.
9. Las vistas privadas relevantes dejan explícito su contrato SSR mínimo de contexto esperado.
10. El change queda validable mediante un flujo manual end-to-end principal: login → ficha → biblioteca → reseña → perfil → admin.

## Riesgos

- Medio: concentrar demasiadas acciones en la ficha puede volver difuso el contrato SSR si no se separan bien los bloques privados.
- Medio: mezclar moderación admin con flujo privado del usuario puede desbordar alcance si se agregan extras no pactados.
- Bajo: un `seed_library` pobre o poco variado puede debilitar la demo y la validación del perfil/biblioteca.
- Bajo: feedback inconsistente entre acciones privadas puede degradar la experiencia aunque el backend funcione.

## Justificación

Este change completa la primera experiencia privada realmente usable del producto sin salir del marco académico del proyecto. La decisión central es priorizar valor de usuario sobre sofisticación técnica: la ficha se convierte en el punto natural de acción, la biblioteca y la reseña cierran el caso de uso principal y el admin queda contenido como capacidad operativa razonable. Se busca un backend SSR coherente, defendible y con alcance sano para TFG FP, no una solución sobrearquitecturada.

## Rollback plan

Revertir blueprints y vistas privadas incorporadas para reseñas, biblioteca, perfil y admin; quitar wiring asociado en `register_routes()` / `create_app()`; retirar `seed_library` del orquestador general; restaurar la ficha a su variante pública previa manteniendo intactas autenticación SSR, catálogo público, modelos de dominio y seeds ya existentes.

## Artefactos

- Archivo: `openspec/changes/backend-private-areas-and-admin/proposal.md`
- Módulos/paquetes afectados: `app/routes/reviews.py`, `app/routes/library.py`, `app/routes/profile.py`, `app/routes/admin.py`, `app/routes/games.py`, `app/routes/__init__.py`, `app/__init__.py`, `app/decorators.py`, `seeds/seed_library.py`, `seeds/seed_all.py`, templates privados y parciales SSR relacionados.

## Siguiente paso recomendado

- `sdd-spec`
- `sdd-design`

## Resolución de skills

- none
