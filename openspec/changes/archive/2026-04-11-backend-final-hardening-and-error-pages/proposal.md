# Propuesta — `backend-final-hardening-and-error-pages`

## Estado
draft

## Título
Cerrar hardening final del backend y páginas de error

## Intención

Completar la Fase 7 del roadmap backend para dejar el backend legítimamente terminado según los criterios del proyecto: robusto, consistente, con manejo de errores razonable, validaciones y protección revisadas, seed idempotente y arranque limpio listos para handoff al frontend.

## Problema

El proyecto ya cerró los changes funcionales principales del backend (catálogo público, autenticación, áreas privadas y administración moderada), pero todavía queda pendiente el tramo de hardening final definido en el roadmap. Sin este change, el backend tiene valor funcional, pero no puede considerarse “100% terminado” porque faltan páginas de error claras, una auditoría transversal de validaciones y CSRF, revisión de robustez de escrituras con rollback, y una verificación operativa final de seed y arranque limpio.

## Alcance

Incluye: implementar páginas `404` y `500` funcionales y coherentes con la app; registrar error handlers correspondientes; revisar todas las rutas POST y privadas para confirmar CSRF, validaciones server-side, flashes y guards; auditar también rutas públicas desde la perspectiva de robustez y consistencia SSR; revisar escrituras y seeds para garantizar `db.session.rollback()` donde una operación fallida pueda dejar la sesión rota; mejorar de forma pragmática el tratamiento de errores `400`/CSRF cuando la experiencia actual resulte demasiado cruda y el ajuste sea razonable dentro del alcance; verificar arranque limpio con Docker y seed idempotente como criterio de cierre real; corregir la race condition de arranque entre `web` y `db` mediante una espera explícita a disponibilidad real de PostgreSQL antes de iniciar Flask; y dejar un checklist técnico/documental claro de qué quedó validado y qué sigue fuera de alcance.

## Fuera de alcance

No incluye nuevas features de producto, rediseño visual del frontend, tests formales si no forman parte del alcance FP, refactors grandes sin necesidad funcional, observabilidad avanzada, arquitectura global de errores HTTP, background jobs ni mejoras cosméticas no vinculadas al hardening backend.

## Criterios de aceptación

1. El proyecto dispone de páginas `404` y `500` funcionales, claras y coherentes con la aplicación, conectadas mediante error handlers reales.
2. Todas las rutas POST que cambian estado quedan auditadas respecto a CSRF, validaciones server-side, flashes y guards correctos.
3. Las validaciones relevantes de auth, reseñas, biblioteca y admin quedan revisadas y alineadas con el dominio, docs y comportamiento esperado.
4. Las escrituras relevantes y los seeds quedan revisados para evitar dejar `db.session` en estado roto tras errores recuperables.
5. Las rutas públicas también quedan auditadas desde la perspectiva de robustez y consistencia SSR, sin reabrir el alcance funcional ya cerrado.
6. Los errores `400`/CSRF se mejoran solo donde sea razonable y simple dentro del alcance, sin introducir un subsistema global de manejo de errores.
7. El seed general sigue siendo idempotente y el backend puede validarse como listo desde un arranque limpio con Docker.
8. `docker-compose up --build -d` debe poder levantar `web` sin intervención manual posterior para esperar a PostgreSQL.
9. El change deja documentación de cierre y checklist técnico suficiente para defensa académica y handoff al frontend.

## Riesgos

- Medio: al ser un change transversal, puede aparecer scope creep si se intenta “aprovechar” para refactors amplios.
- Medio: revisar validaciones y rollbacks puede revelar inconsistencias entre docs y código que obliguen a decidir cuál es la verdad.
- Bajo: mejorar el tratamiento de errores `400`/CSRF puede empujar a una solución demasiado grande si no se mantiene el criterio pragmático acordado.
- Bajo: la validación con Docker depende del entorno local y puede introducir ruido operativo ajeno al código.

## Justificación

Este change no agrega valor de producto nuevo; agrega confianza técnica y cierra el backend como entregable real. En un TFG FP, esto importa muchísimo: no alcanza con que “las features estén”. Hay que poder defender que el backend quedó consistente, protegido, recuperable ante errores razonables y listo para que el frontend se apoye sobre él sin adivinar contratos ni convivir con pantallas crudas o sesiones de base de datos contaminadas.

## Rollback plan

Revertir los handlers y templates de error, deshacer ajustes transversales de validación/rollback/guards realizados en este change y restaurar la versión anterior de los archivos revisados. No debería requerir rollback de esquema porque el change apunta a hardening, no a cambios estructurales de base de datos.

## Artefactos

- Archivo: `openspec/changes/backend-final-hardening-and-error-pages/proposal.md`
- Áreas candidatas: `app/__init__.py`, `app/routes/*.py`, `app/decorators.py`, `app/templates/errors/*.html`, `app/templates/partials/flash_messages.html`, `seeds/*.py`, `README.md` o docs de cierre si hace falta reflejar validación final.

## Siguiente paso recomendado

- `sdd-spec`
- `sdd-design`

## Resolución de skills

- none
