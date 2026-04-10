# Especificación — Áreas privadas SSR del usuario y administración moderada

## Propósito

Definir el flujo privado principal del producto sobre SSR Flask, permitiendo que el usuario autenticado gestione reseña y biblioteca desde la ficha del juego, consulte un perfil simple y que el administrador disponga de capacidades moderadas de operación, sin convertir el change en un backoffice sobredimensionado.

## Requisitos

### Requisito: la ficha del juego funciona como hub privado autenticado

La ficha del juego autenticada MUST mantener el contenido público relevante del juego y SHALL sumar capacidades privadas contextuales del usuario. El sistema MUST renderizar bloques separados para biblioteca y reseña propia cuando exista sesión autenticada.

#### Escenario: Mostrar acciones privadas en ficha autenticada
- Given un usuario autenticado visita la ficha de un juego existente
- When el sistema renderiza la vista SSR
- Then la ficha SHALL mantener la información pública del juego y SHALL mostrar bloques privados separados para biblioteca y reseña

### Requisito: CRUD completo de reseña propia

Un usuario autenticado MUST poder crear, editar y eliminar su propia reseña sobre un juego. El sistema SHALL validar `rating` entre 1 y 5 y `text` entre 10 y 1000 caracteres, y MUST impedir operaciones sobre reseñas ajenas salvo capacidades admin explícitas.

#### Escenario: Crear reseña válida desde ficha
- Given un usuario autenticado sin reseña previa sobre un juego
- When envía una reseña con `rating` válido y `text` válido
- Then el sistema SHALL persistir la reseña y SHALL informar éxito con feedback claro

#### Escenario: Editar reseña propia existente
- Given un usuario autenticado con una reseña ya creada sobre un juego
- When actualiza su `rating` o `text` con datos válidos
- Then el sistema SHALL modificar la reseña existente y no SHALL crear un segundo registro

#### Escenario: Eliminar reseña propia
- Given un usuario autenticado con una reseña propia existente
- When solicita eliminarla mediante acción permitida
- Then el sistema SHALL borrar la reseña y SHALL informar éxito

### Requisito: la UX de reseña respeta la unicidad del dominio

La ficha autenticada MUST respetar que solo puede existir una reseña por `(user_id, game_id)`. Si el usuario ya tiene reseña para ese juego, el sistema SHALL mostrar esa reseña actual y ofrecer editar/eliminar en lugar de presentar una nueva alta redundante.

#### Escenario: Sustituir alta por experiencia de edición
- Given un usuario autenticado con reseña existente sobre un juego
- When accede a la ficha SSR de ese juego
- Then el sistema MUST mostrar su reseña actual y MUST NOT ofrecer una segunda creación independiente

### Requisito: biblioteca personal completa y contextual

Un usuario autenticado MUST poder añadir un juego a su biblioteca, cambiar su estado y quitarlo. La primera acción desde la ficha SHALL ser un alta simple en biblioteca; una vez agregado, el sistema SHALL permitir gestión posterior del estado usando solo los valores `want_to_play`, `playing` y `played`.

#### Escenario: Añadir juego a biblioteca desde ficha
- Given un usuario autenticado y un juego que aún no pertenece a su biblioteca
- When ejecuta la acción de añadir a biblioteca
- Then el sistema SHALL crear la entrada correspondiente y SHALL reemplazar el CTA inicial por controles de gestión posteriores

#### Escenario: Cambiar estado de biblioteca
- Given un usuario autenticado con un juego ya presente en su biblioteca
- When envía un nuevo estado válido
- Then el sistema SHALL actualizar el estado de la entrada existente

#### Escenario: Quitar juego de biblioteca
- Given un usuario autenticado con un juego ya presente en su biblioteca
- When solicita quitarlo de su biblioteca
- Then el sistema SHALL eliminar la entrada correspondiente

### Requisito: vista de biblioteca filtrable y simple

`/mi-biblioteca` MUST presentar una lista única de juegos del usuario autenticado y SHALL permitir filtrado por estado. La vista MUST mantenerse simple y no SHALL dividirse en múltiples paneles complejos ni subsecciones de dashboard.

#### Escenario: Filtrar biblioteca por estado
- Given un usuario autenticado con juegos en distintos estados de biblioteca
- When solicita `/mi-biblioteca` con un filtro de estado válido
- Then el sistema SHALL devolver solo las entradas correspondientes a ese estado

#### Escenario: Biblioteca vacía
- Given un usuario autenticado sin juegos en su biblioteca o sin resultados para el filtro aplicado
- When se renderiza `/mi-biblioteca`
- Then la vista SHALL mostrar un estado vacío simple con mensaje útil

### Requisito: perfil SSR simple y navegable

`/perfil` MUST funcionar como un resumen privado simple del usuario autenticado. La vista SHALL mostrar datos básicos, contadores relevantes y accesos directos útiles al flujo privado, y MUST NOT convertirse en un dashboard complejo.

#### Escenario: Renderizar perfil funcional
- Given un usuario autenticado
- When solicita `/perfil`
- Then el sistema SHALL renderizar una vista con datos del usuario, contadores y accesos directos a vistas privadas relevantes

### Requisito: la ficha autenticada conserva valor público

La autenticación MUST ampliar la ficha del juego, no reemplazarla. El sistema SHALL mantener visibles el promedio y las reseñas públicas del juego cuando exista sesión autenticada, añadiendo encima o junto a ello la zona privada del usuario.

#### Escenario: Combinar contenido público y privado en ficha
- Given un usuario autenticado visita la ficha de un juego con reseñas públicas
- When se renderiza la vista
- Then el sistema SHALL mostrar promedio y reseñas públicas y SHALL añadir la capa privada de biblioteca y reseña propia

### Requisito: panel admin moderado y utilizable

El sistema MUST ofrecer un panel admin protegido por autorización que permita moderación y operación básica sin ampliar el alcance a un backoffice complejo. La vista admin SHALL listar reseñas globales con contexto útil básico: autor, juego, rating, fecha y texto o extracto.

#### Escenario: Acceder al panel admin como administrador
- Given un usuario autenticado con `is_admin=True`
- When solicita la vista admin de reseñas
- Then el sistema SHALL permitir acceso y SHALL renderizar el listado global con el contexto definido

#### Escenario: Bloquear acceso admin a usuario no autorizado
- Given un usuario no administrador intenta acceder a la vista admin
- When solicita la ruta protegida
- Then el sistema MUST denegar el acceso según la política de autorización vigente del proyecto

### Requisito: moderación admin de reseñas

Un administrador MUST poder eliminar reseñas de cualquier usuario desde el panel admin. Esta capacidad SHALL coexistir con la restricción general que impide a usuarios normales operar sobre reseñas ajenas.

#### Escenario: Eliminar reseña ajena como admin
- Given un administrador autenticado y una reseña existente de otro usuario
- When ejecuta la acción de eliminación desde el panel admin
- Then el sistema SHALL borrar la reseña y SHALL informar éxito

### Requisito: actualización de catálogo con cooldown y feedback útil

El panel admin MUST ofrecer una acción de actualización de catálogo conectada al seed o servicio correspondiente. La operación SHALL respetar cooldown y MUST devolver feedback útil sobre el resultado operativo sin requerir arquitectura asíncrona avanzada.

#### Escenario: Ejecutar refresh permitido
- Given un administrador autenticado y una ventana de cooldown ya cumplida
- When dispara la actualización de catálogo
- Then el sistema SHALL ejecutar la operación y SHALL mostrar feedback útil del resultado

#### Escenario: Rechazar refresh durante cooldown
- Given un administrador autenticado y una ventana de cooldown todavía activa
- When intenta lanzar una nueva actualización
- Then el sistema MUST rechazar la operación e informar claramente que el cooldown sigue vigente

### Requisito: seed_library idempotente y útil para demo

El change MUST incorporar un `seed_library` idempotente que genere datos variados por usuario y por estado. El sistema SHALL permitir que biblioteca y perfil se prueben con datos creíbles sin depender de carga manual posterior.

#### Escenario: Ejecutar seed_library sobre datos existentes
- Given una base con usuarios y juegos ya sembrados y posibles entradas previas de biblioteca
- When se ejecuta el seed general incluyendo `seed_library`
- Then el proceso SHALL mantener idempotencia y SHALL dejar una biblioteca demo útil sin duplicados inválidos

### Requisito: feedback funcional y validaciones específicas

Las acciones privadas y admin relevantes MUST usar flash messages claros y funcionales. Cuando falle una validación, el sistema SHALL informar el motivo específico del rechazo y MUST NOT limitarse a mensajes genéricos si el caso puede explicarse con precisión.

#### Escenario: Rechazar reseña por texto demasiado corto
- Given un usuario autenticado intenta guardar una reseña con texto inferior al mínimo permitido
- When el backend valida la operación
- Then el sistema SHALL rechazarla e informar específicamente el incumplimiento del rango permitido

#### Escenario: Rechazar estado de biblioteca inválido
- Given un usuario autenticado intenta actualizar una entrada con un estado no permitido
- When el backend valida la operación
- Then el sistema SHALL rechazar la acción e informar que el estado enviado no es válido

### Requisito: contratos SSR explícitos para vistas privadas

Las vistas privadas relevantes MUST dejar un contrato SSR explícito y estable respecto al contexto mínimo esperado desde backend. Esto SHALL aplicar como mínimo a ficha autenticada, formulario o bloque de reseña, biblioteca, perfil y panel admin.

#### Escenario: Mantener contrato SSR verificable
- Given una vista privada definida dentro de este change
- When se revisa su integración entre ruta y template
- Then el contexto renderizado SHALL ser explícito y coherente con su propósito funcional

### Requisito: fronteras y done del change

Este change MUST cerrar un flujo privado coherente para usuario autenticado y una capacidad admin moderada, manteniendo fuera dashboard complejo, vista dedicada de “mis reseñas”, acciones masivas admin, filtros admin avanzados, background jobs y UX enriquecida no esencial. El change SHALL considerarse done solo cuando el flujo `login → ficha → biblioteca/reseña → perfil → admin` sea validable manualmente de punta a punta.

#### Escenario: Evaluar alcance del change
- Given una funcionalidad nueva no contemplada en este documento
- When se contrasta contra el alcance acordado
- Then esa funcionalidad MUST quedar fuera de `backend-private-areas-and-admin` si amplía el change más allá de sus fronteras explícitas
