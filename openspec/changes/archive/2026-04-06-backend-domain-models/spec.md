# Especificación — Modelos de dominio del backend

## Propósito

Definir el comportamiento requerido para la base de dominio del backend del catálogo F2P, limitado a los modelos `User`, `Game`, `Review` y `UserLibrary`, sus validaciones esenciales, relaciones ORM, timestamps UTC simples y la creación inicial de tablas.

## Requisitos

### Requisito: modelo de dominio User

El sistema DEBE proporcionar un modelo `User` con `username` y `email` únicos, un `password_hash` persistido, un flag `is_admin` con valor por defecto `False` y un timestamp `created_at` simple en UTC. `username` DEBE aceptar solo 3–30 caracteres compuestos por letras, números o `_`. El modelo DEBERÁ exponer comportamiento seguro para definir/verificar contraseña y un `__repr__` seguro.

#### Escenario: Crear un usuario válido
- DADO un usuario nuevo con username único, email único y contraseña válida
- CUANDO el registro de usuario se persiste
- ENTONCES la contraseña DEBERÁ almacenarse como hash y no como texto plano
- Y `created_at` e `is_admin=False` DEBERÁN establecerse automáticamente

#### Escenario: Rechazar un username inválido
- DADO un usuario nuevo con un username fuera del formato o longitud permitidos
- CUANDO el modelo se valida para persistencia
- ENTONCES el sistema DEBE rechazar el registro

### Requisito: modelo de dominio Game

El sistema DEBE proporcionar un modelo `Game` que almacene los campos documentados del catálogo, incluyendo `api_id` único, `description` obligatoria, `screenshots` en JSON y `cached_at` simple en UTC. El modelo DEBERÍA preservar los campos de metadatos opcionales sin promoverlos a estado obligatorio.

#### Escenario: Persistir un juego completo
- DADO un payload de juego con `api_id` único y `description` no vacía
- CUANDO el juego se persiste
- ENTONCES los datos del catálogo DEBERÁN almacenarse en la tabla `games`
- Y `screenshots` DEBERÁ poder representarse en una única columna JSON

#### Escenario: Rechazar ausencia de description
- DADO un payload de juego sin `description`
- CUANDO el modelo se valida para persistencia
- ENTONCES el sistema DEBE rechazar el registro

### Requisito: modelo de dominio Review

El sistema DEBE proporcionar un modelo `Review` vinculado a un `User` y a un `Game`. `rating` DEBE estar entre 1 y 5, `text` DEBE ser obligatorio con longitud 10–1000, y el par `(user_id, game_id)` DEBE ser único. El modelo DEBERÁ mantener timestamps simples `created_at` y `updated_at` en UTC.

#### Escenario: Crear una reseña válida
- DADO un usuario y juego existentes sin reseña previa para ese par
- CUANDO se persiste una reseña con rating 1–5 y texto de longitud 10–1000
- ENTONCES la reseña DEBERÁ almacenarse con ambas claves foráneas y timestamps

#### Escenario: Rechazar reseña duplicada o inválida
- DADO que ya existe una reseña para el mismo `user_id` y `game_id`, o que el rating/texto son inválidos
- CUANDO se valida otra reseña para persistencia
- ENTONCES el sistema DEBE rechazar el registro

### Requisito: modelo de dominio UserLibrary

El sistema DEBE proporcionar un modelo `UserLibrary` vinculado a un `User` y a un `Game`. `status` DEBE almacenarse como `String` y DEBE permitir solo `want_to_play`, `playing` o `played`. El par `(user_id, game_id)` DEBE ser único y el modelo DEBERÁ mantener un timestamp `created_at` simple en UTC.

#### Escenario: Añadir un juego a la biblioteca de un usuario
- DADO un usuario y un juego existentes que todavía no están vinculados en la biblioteca
- CUANDO se persiste un registro de biblioteca con un estado permitido
- ENTONCES el registro DEBERÁ almacenarse con el estado seleccionado

#### Escenario: Rechazar estado inválido en biblioteca
- DADO un registro de biblioteca con un estado fuera del conjunto permitido
- CUANDO el modelo se valida para persistencia
- ENTONCES el sistema DEBE rechazar el registro

### Requisito: relaciones ORM y creación de tablas

El sistema DEBE definir las relaciones del modelo con `back_populates` explícito y NO DEBE depender de `backref` para estas cuatro entidades de dominio. `create_app()` DEBE importar los modelos antes de entrar en `app.app_context()` y DEBE ejecutar `db.create_all()` dentro de ese contexto para que puedan crearse las cuatro tablas.

#### Escenario: Inicializar la aplicación
- DADO que la aplicación arranca con acceso disponible a la base de datos
- CUANDO `create_app()` finaliza el bootstrap
- ENTONCES los metadatos de los modelos DEBERÁN cargarse antes de ejecutar `db.create_all()`
- Y las cuatro tablas de dominio DEBERÁN existir sin errores de bootstrap

### Requisito: definición de done para verificación del esquema

El change DEBE considerarse terminado solo después de que una verificación manual del esquema en PostgreSQL confirme las columnas esperadas, claves foráneas, restricciones únicas y nullability relevante para `users`, `games`, `reviews` y `user_library`.

#### Escenario: Validar el esquema real de PostgreSQL
- DADO que la aplicación ya creó tablas en PostgreSQL
- CUANDO el esquema se inspecciona manualmente
- ENTONCES el esquema observado DEBE coincidir con las constraints de dominio aprobadas
