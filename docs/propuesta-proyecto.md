# Propuesta de Proyecto

**Asunto:** `PROYECTO + [DNI Alumno 1] y [DNI Alumno 2] + 2º DAW`

---

Buenos días, Alejandro.

Nos ponemos en contacto para comunicarle el tema elegido para nuestro proyecto de módulo.

**Título del proyecto:** Catálogo Web de Juegos Free-to-Play (F2P Catalog)

**Tipo de proyecto:** Proyecto de ejecución/realización (tipo 3) — diseño y desarrollo de un producto web funcional, aplicando las competencias del ciclo.

## Problema que resuelve

Actualmente existen cientos de juegos gratuitos (free-to-play) dispersos en múltiples plataformas (Steam, Epic Games, navegador, etc.). Un jugador que busca un nuevo juego F2P tiene que navegar entre distintas tiendas, consultar reseñas en diferentes sitios y no dispone de una forma centralizada de descubrir, filtrar y valorar estos juegos.

Nuestra aplicación web resuelve esta necesidad ofreciendo un **catálogo unificado de juegos F2P** con buscador, filtros por género y plataforma, fichas detalladas con requisitos del sistema y capturas, y un sistema de usuarios donde cada jugador puede gestionar su biblioteca personal, escribir reseñas y valorar juegos, creando así una pequeña comunidad de referencia.

## Stack tecnológico previsto

- **Backend:** Python con Flask (patrón MVC), PostgreSQL, SQLAlchemy
- **Frontend:** HTML5, CSS3 (Bootstrap), JavaScript vanilla, Jinja2
- **Datos:** API externa FreeToGame (fuente del catálogo, cacheada en base de datos local)
- **Seguridad:** bcrypt para contraseñas, CSRF con Flask-WTF, control de roles (usuario/admin)

## Funcionalidades principales

- Catálogo navegable con búsqueda, filtros y paginación
- Fichas de juego con información detallada (requisitos, capturas, descripción)
- Sistema de registro, login y perfiles de usuario
- Biblioteca personal con estados (quiero jugar, jugando, jugado)
- Sistema de reseñas y valoraciones (1-5 estrellas)
- Panel de administración para moderación de reseñas y actualización del catálogo

---

Quedamos a su disposición para cualquier orientación o ajuste que considere necesario.

Un saludo,
[Nombre Alumno 1] y [Nombre Alumno 2]
