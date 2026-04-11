# Especificación — Hardening final del backend y páginas de error

## Propósito

Definir el cierre técnico del backend para completar la Fase 7 del roadmap, asegurando manejo de errores razonable, validaciones y protección revisadas, robustez de escritura, consistencia SSR y preparación final para handoff al frontend sin agregar nuevas features de producto.

## Requisitos

### Requisito: páginas de error funcionales y conectadas

La aplicación MUST disponer de páginas `404` y `500` funcionales y coherentes con el resto del proyecto. El sistema SHALL registrar error handlers reales para estos casos y MUST evitar dejar al usuario en respuestas HTML crudas del framework cuando el alcance permita una alternativa clara.

#### Escenario: Recurso inexistente
- Given un usuario solicita una ruta no existente
- When Flask resuelve un `404`
- Then el sistema SHALL renderizar una página de error 404 clara y coherente con la aplicación

#### Escenario: Error interno no controlado
- Given ocurre una excepción no controlada en una ruta o handler cubierto
- When Flask resuelve un `500`
- Then el sistema SHALL renderizar una página de error 500 clara y coherente con la aplicación

### Requisito: auditoría completa de rutas POST con cambio de estado

Todas las rutas POST que cambian estado MUST quedar revisadas respecto a CSRF, validaciones server-side, feedback funcional y guards de acceso. El change SHALL confirmar que estas protecciones son efectivas de manera consistente en auth, reseñas, biblioteca y admin.

#### Escenario: POST protegido con CSRF
- Given una ruta POST que modifica estado del sistema
- When se revisa su integración entre ruta y formulario/template
- Then la operación MUST estar protegida por CSRF y SHALL rechazar solicitudes inválidas según la política del proyecto

#### Escenario: Ruta privada protegida correctamente
- Given una ruta POST o GET privada del sistema
- When se revisan sus guards de acceso
- Then la ruta SHALL exigir `@login_required` o `@admin_required` cuando corresponda a su nivel de acceso

### Requisito: validaciones server-side alineadas con dominio y docs

Las validaciones relevantes del backend MUST quedar auditadas y ajustadas si hay inconsistencias con el dominio cerrado, la spec funcional previa o el roadmap. El sistema SHALL mantener mensajes específicos cuando el rechazo pueda explicarse con precisión.

#### Escenario: Validación de entrada inconsistente detectada
- Given una ruta acepta datos de entrada del usuario
- When la revisión detecta una discrepancia entre comportamiento real y reglas del dominio o documentación
- Then el sistema SHALL corregir la validación o documentar explícitamente la verdad del proyecto dentro del alcance del change

### Requisito: robustez de escritura y recuperación de sesión

Las rutas de escritura y los seeds relevantes MUST evitar dejar `db.session` en estado roto tras errores recuperables. El sistema SHALL aplicar `db.session.rollback()` donde una operación fallida pueda contaminar escrituras posteriores.

#### Escenario: Error recuperable durante escritura
- Given una ruta POST o seed ejecuta una operación de escritura y ocurre una excepción recuperable
- When el backend maneja la falla
- Then el sistema SHALL revertir la sesión mediante rollback antes de continuar o devolver control

### Requisito: auditoría de robustez sobre rutas públicas

Las rutas públicas (`/`, `/catalogo`, `/juego/<id>`) MUST quedar revisadas desde la perspectiva de robustez y consistencia SSR. El change SHALL corregir inconsistencias claras de contexto, fallos de degradación o respuestas impropias dentro del alcance técnico acordado, sin redefinir la funcionalidad ya cerrada.

#### Escenario: Revisión de contexto SSR público
- Given una ruta pública del catálogo o la ficha
- When se contrasta su comportamiento con el contrato SSR esperado
- Then la ruta SHALL mantener coherencia de contexto, degradación razonable y ausencia de regresiones funcionales dentro del alcance actual

### Requisito: tratamiento pragmático de errores 400/CSRF

Los errores `400` relacionados con formularios o CSRF SHALL mejorarse solo cuando la respuesta actual sea excesivamente cruda y el ajuste sea razonable dentro del alcance del change. El sistema MUST NOT introducir una arquitectura global de manejo uniforme para todos los errores HTTP.

#### Escenario: Error CSRF con respuesta demasiado cruda
- Given una petición POST falla por token CSRF ausente o inválido
- When la experiencia actual resulte impropia para el nivel del proyecto y exista una mejora simple
- Then el sistema SHALL aplicar una mejora pragmática y acotada, sin convertir este change en una re-arquitectura global de errores

### Requisito: seed general idempotente y cierre operativo

El backend MUST poder validarse desde un arranque limpio con Docker y seed general repetible. El sistema SHALL mantener idempotencia del seed y comportamiento consistente al ejecutar el flujo operativo de arranque desde cero.

#### Escenario: Arranque web espera disponibilidad real de base de datos
- Given el entorno Docker del proyecto se levanta desde volúmenes vacíos
- When `docker-compose up --build -d` inicia `db` y `web`
- Then el servicio `web` SHALL esperar explícitamente a que PostgreSQL acepte conexiones antes de arrancar Flask y MUST NOT requerir un restart manual posterior

#### Escenario: Repetir seed sin duplicados inválidos
- Given una base ya poblada por el seed general
- When el seed vuelve a ejecutarse
- Then el sistema SHALL mantener idempotencia y MUST NOT crear duplicados inválidos en datos demo o cacheados

#### Escenario: Arranque limpio del backend
- Given un entorno limpio levantado con Docker
- When se ejecuta el flujo previsto de arranque y seed
- Then el backend SHALL poder considerarse listo para uso funcional con sus templates SSR mínimos

### Requisito: documentación de cierre técnico

El change MUST dejar documentación clara de qué se revisó, qué se corrigió, qué se validó y qué sigue fuera de alcance. Esta documentación SHALL servir como evidencia de que el backend quedó 100% terminado antes del inicio del frontend.

#### Escenario: Cierre del backend
- Given el change se aproxima a su cierre
- When se revisan sus artefactos finales
- Then deberá existir un checklist técnico/documental suficiente para defender el estado final del backend y su handoff al frontend

### Requisito: respeto estricto del alcance

Este change MUST endurecer y pulir el backend existente sin abrir nuevas features de producto ni un rediseño visual del frontend. El sistema SHALL mantener fuera de alcance refactors grandes no justificados, observabilidad avanzada, tests formales si no entran en FP, background jobs y mejoras cosméticas no esenciales.

#### Escenario: Aparición de una mejora atractiva pero fuera de alcance
- Given surge una posible mejora que no forma parte del hardening final acordado
- When se contrasta contra este documento
- Then esa mejora MUST quedar fuera del change si no aporta directamente al cierre técnico del backend
