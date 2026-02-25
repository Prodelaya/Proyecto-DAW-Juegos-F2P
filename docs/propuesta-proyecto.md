# Propuesta de Proyecto

**Asunto:** `PROYECTO - [DNI Alumno 1] - [DNI Alumno 2] - 2º DAW`

---

Buenos días, Alejandro.

Te escribimos para confirmarte el tema que hemos elegido para nuestro proyecto final de módulo.

**Título del proyecto:** Catálogo Web de Juegos Free-to-Play (F2P Catalog)

**Tipo de proyecto:** Proyecto de ejecución/realización (tipo 3) — diseño y desarrollo de un producto web funcional, donde aplicaremos de forma práctica todo lo que hemos visto en el ciclo (backend, frontend, bases de datos, seguridad y despliegue).

## 1. Problema que resuelve


Actualmente existen cientos de juegos gratuitos (free-to-play) dispersos en múltiples plataformas (Steam, Epic Games, navegador, etc.). Un jugador que busca un nuevo juego F2P tiene que navegar entre distintas tiendas, consultar reseñas en diferentes sitios y no dispone de una forma centralizada de descubrir, filtrar y valorar estos juegos.

Nuestra aplicación web resuelve esta necesidad ofreciendo un **catálogo unificado de juegos F2P** con buscador, filtros por género y plataforma, fichas detalladas con requisitos del sistema y capturas, y un sistema de usuarios donde cada jugador puede gestionar su biblioteca personal, escribir reseñas y valorar juegos, creando así una pequeña comunidad de referencia.

## 2. Stack tecnológico previsto

- **Backend:** Python con Flask (patrón Application Factory y MVC), PostgreSQL, SQLAlchemy (ORM).
- **Frontend / UI:** HTML5, CSS3 (Bootstrap), JavaScript vanilla, motor de plantillas Jinja2. Diseñado de forma _responsive_ (_Mobile First_).
- **Datos y caché:** Consumo de la API externa _FreeToGame_ con estrategia de cacheo en base de datos local para garantizar el rendimiento y disponibilidad.
- **Seguridad y RGPD:** _Hashing_ de contraseñas con bcrypt, protección contra ataques CSRF (Flask-WTF), validación de entradas (Backend + Frontend) y control de roles (Usuario / Administrador). Cumplimiento básico RGPD informando de la finalidad de la recogida de datos y ofreciendo mecanismos de eliminación de cuentas.
- **Despliegue:** Contenerización con Docker y Docker Compose para el entorno de producción en un VPS (Linux) utilizando Nginx como proxy inverso.

## 3. Alcance y responsabilidades

El desarrollo se ha acotado a un MVP (Producto Mínimo Viable) funcional, estableciendo la siguiente división equitativa del trabajo para la memoria y la evaluación:

- **Pablo Laya (Backend y Sistemas):** Diseño de la base de datos (E-R), desarrollo de la API y rutas con Flask, implementación de la caché de _FreeToGame_, Dockerización y despliegue en servidor VPS.
- **Pablo Pérez (Frontend y Calidad):** Diseño de interfaces (UX/UI y Wireframes), maquetación con Bootstrap y Jinja2, implementación visual de autenticación y filtros de catálogo, validación y plan de pruebas de la aplicación (15-20 casos de prueba).

## 4. Funcionalidades principales

- Catálogo navegable con búsqueda, filtros cruzados y paginación en servidor.
- Fichas de juego con información detallada (requisitos, capturas, descripción).
- Sistema de registro, _login_ y perfiles de usuario.
- Biblioteca personal con gestión de estados (quiero jugar, jugando, jugado).
- Sistema de reseñas y valoraciones (1-5 estrellas) por modelo asimétrico (una reseña por juego).
- Panel de administración para la moderación de reseñas y actualización manual del catálogo cacheados de la API.

---

Un saludo,
Pablo Laya y Pablo Pérez
