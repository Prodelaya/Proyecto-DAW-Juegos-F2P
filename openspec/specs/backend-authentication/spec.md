# Especificación — Autenticación SSR base y visibilidad de sesión

## Propósito

Definir la autenticación SSR mínima del producto con registro, login, logout y visibilidad coherente de sesión, sin adelantar áreas privadas ni UI específica de administración.

## Requisitos

### Requisito: registro SSR robusto

`GET|POST /registro` MUST aceptar `username`, `email`, `password` y confirmación. El sistema SHALL exigir password mínima de 8 caracteres y confirmación obligatoria, y MUST validar formato/campos antes de persistir. Ante duplicados, SHALL informar por separado si el conflicto es de `username` o `email`. Tras éxito, MUST redirigir a `/login`.

#### Escenario: Registrar un usuario válido
- Given un visitante anónimo con datos válidos y únicos
- When envía `POST /registro`
- Then el sistema SHALL crear el usuario con password hasheada y redirigir a `/login`

#### Escenario: Rechazar conflicto específico en registro
- Given un visitante con `username` o `email` ya existente
- When envía `POST /registro`
- Then la respuesta MUST permanecer en registro e informar específicamente qué campo está duplicado

### Requisito: login SSR solo por email

`GET|POST /login` MUST autenticar solo con `email` y `password`. El sistema SHALL devolver errores específicos para campos faltantes o formato inválido, y MUST usar un mensaje genérico para credenciales inválidas. Tras éxito, SHALL redirigir a un `next` válido; si no existe o no es seguro, MUST redirigir a `/`.

#### Escenario: Login exitoso con next válido
- Given un usuario existente y un parámetro `next` válido
- When envía credenciales correctas a `POST /login`
- Then el sistema SHALL iniciar sesión y redirigir a `next`

#### Escenario: Credenciales inválidas
- Given un email con formato válido y password enviada
- When las credenciales no corresponden a un usuario autenticable
- Then el sistema MUST mostrar un mensaje genérico de credenciales inválidas sin revelar cuál dato falló

### Requisito: acceso a pantallas auth según estado de sesión

Un usuario ya autenticado MUST NOT permanecer en `/login` ni `/registro`. Si intenta acceder a cualquiera de esas rutas, el sistema SHALL redirigirlo a `/`.

#### Escenario: Usuario autenticado abre login o registro
- Given una sesión autenticada vigente
- When solicita `GET /login` o `GET /registro`
- Then el sistema SHALL responder con redirect a `/`

### Requisito: logout seguro

`/logout` MUST aceptar solo `POST`, MUST requerir sesión autenticada y MUST quedar protegido por CSRF. El sistema SHALL cerrar la sesión y redirigir a `/`.

#### Escenario: Cerrar sesión por POST protegido
- Given un usuario autenticado con token CSRF válido
- When envía `POST /logout`
- Then el sistema SHALL destruir la sesión y redirigir a `/`

### Requisito: visibilidad SSR de sesión en navbar

La navbar autenticada MUST mostrar `username` y MUST NOT exponer `email`. Este change SHALL reflejar visibilidad de sesión coherente, pero `is_admin` MUST NOT producir UI diferenciada en esta fase.

#### Escenario: Renderizar navbar autenticada
- Given una request SSR con usuario autenticado
- When se renderiza la navbar
- Then la vista SHALL mostrar el `username` y no SHALL mostrar UI especial por `is_admin`

### Requisito: contrato mínimo SSR y base para rutas protegidas

`login.html`, `register.html` y la navbar autenticada MUST dejar un contrato SSR explícito y estable para formularios, errores/flash y estado de sesión. `login_manager` SHALL quedar configurado con `login_view` y `login_message` efectivos para futuras rutas con `@login_required`.

#### Escenario: Redirigir una ruta protegida futura
- Given una ruta futura protegida con `@login_required` y un visitante anónimo
- When intenta acceder a esa ruta
- Then Flask-Login SHALL redirigir al login configurado usando el mensaje definido

### Requisito: fronteras y done del change

Este change MUST cubrir solo auth SSR base y visibilidad de sesión. Reseñas, biblioteca, perfil, admin UI y CTAs pasivos a futuras acciones MUST quedar fuera de alcance. El change SHALL considerarse done solo cuando exista auth funcional, visibilidad coherente de sesión y contrato SSR explícito.

#### Escenario: Evaluar alcance del change
- Given una necesidad de funcionalidad privada o UI posterior
- When se contrasta contra esta especificación
- Then esa capacidad MUST quedar fuera de alcance de `backend-authentication`
