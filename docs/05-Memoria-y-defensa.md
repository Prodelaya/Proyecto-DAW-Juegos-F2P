# Memoria del TFG y Defensa en Vídeo

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Roadmap Frontend](04-Roadmap-frontend.md)

---

## 1. CONTENIDO DE LA MEMORIA (40-50 páginas)

| Cap | Título | Págs | Quién escribe |
|-----|--------|------|--------------|
| 1 | Portada (título, nombres, ciclo, curso, convocatoria) | 1 | Ambos |
| 2 | Índice | 1 | Auto |
| 3 | Introducción y motivación — Problema que resuelve, contexto del mercado F2P, por qué es útil | 2-3 | Tú |
| 4 | Objetivos — Generales y específicos | 1-2 | Tú |
| 5 | Estado del arte — Comparar Steam, FreeToGame web, MMOBomb. Tabla comparativa. Qué hace bien cada uno, qué falta, hueco que llenamos | 3-4 | Compi |
| 6 | Análisis de requisitos — Lista RF01-RF15 funcionales, RNF01-RNF05 no funcionales. Diagrama de casos de uso (anónimo, usuario, admin) | 4-5 | Compi |
| 7 | Diseño de la arquitectura — Diagrama MVC, flujo de petición, patrón Application Factory, blueprints | 3-4 | Tú |
| 8 | Diseño de la base de datos — Modelo E-R (diagrama), modelo relacional, descripción de cada tabla y campo, decisiones (por qué cachear, por qué constraint unique, por qué is_admin booleano) | 3-4 | Tú |
| 9 | Diseño de la interfaz — Wireframes de todas las pantallas, paleta de colores, tipografía, decisiones UX | 3-4 | Compi |
| 10 | Tecnologías utilizadas — Flask, Jinja2, SQLAlchemy, Flask-WTF (CSRF), Bootstrap, PostgreSQL, Docker. Cada una con descripción breve y justificación | 2-3 | Tú |
| 11 | API externa: FreeToGame — Documentación de la API, endpoints usados, estructura de datos, limitaciones, estrategia de cacheo en BD local, actualización manual del catálogo | 3-4 | Tú |
| 12 | Desarrollo backend — Estructura de carpetas, modelos, rutas, servicios, decoradores, seed, paginación. Fragmentos de código relevantes con explicación | 4-5 | Tú |
| 13 | Sistema de roles y permisos — Rol usuario vs admin, decorador @admin_required, panel de moderación, botón actualizar catálogo, justificación del diseño | 1-2 | Tú |
| 14 | Desarrollo frontend — Vistas Jinja2, layout, partials, responsive. Fragmentos de templates y CSS con explicación | 4-5 | Compi |
| 15 | Autenticación y seguridad — Registro, login, bcrypt, sesiones, CSRF, protección de rutas, validación de inputs, prevención de accesos no autorizados | 2-3 | Compi |
| 16 | Pruebas — Tabla de pruebas manuales: caso, entrada, resultado esperado, resultado obtenido, estado (OK/FAIL). Mínimo 15-20 casos | 2-3 | Compi |
| 17 | Manual de despliegue — Requisitos, clonar, configurar .env, docker-compose up, ejecutar seed. Con capturas de terminal | 2-3 | Tú |
| 18 | Manual de usuario — Capturas de pantalla de cada funcionalidad con explicación paso a paso | 3-4 | Compi |
| 19 | Conclusiones y trabajo futuro — Qué se ha aprendido, qué se mejoraría, posibles ampliaciones | 1-2 | Ambos |
| 20 | Bibliografía/Webgrafía — Todas las fuentes: documentación Flask, FreeToGame API, Bootstrap docs, artículos, tutoriales usados | 1-2 | Ambos |
| | **TOTAL ESTIMADO** | **42-52** | |

---

## 2. CONTENIDO DE LA DEFENSA EN VÍDEO

### Tú — Backend (5 minutos)

| Min | Contenido |
|-----|-----------|
| 0:00-0:30 | Presentación: nombre, proyecto, qué problema resuelve |
| 0:30-1:30 | Diapositiva de arquitectura MVC: diagrama del flujo cliente→Flask→BD→API. Explicar por qué se cachean los juegos en BD local |
| 1:30-2:30 | Diapositiva de modelo de BD: diagrama E-R, explicar las 4 tablas, relaciones y constraints |
| 2:30-3:30 | Demo en vivo: mostrar el seed ejecutándose, mostrar datos en PostgreSQL, hacer una búsqueda en el catálogo con paginación y explicar qué pasa internamente |
| 3:30-4:15 | Diapositiva de roles: explicar usuario vs admin, mostrar el decorador, demo rápida del panel admin eliminando una reseña y pulsando "Actualizar catálogo" |
| 4:15-5:00 | Conclusión: qué he aprendido (Flask, SQLAlchemy, Docker, consumo de APIs, CSRF), qué mejoraría |

### Tu compi — Frontend (5 minutos)

| Min | Contenido |
|-----|-----------|
| 0:00-0:30 | Presentación: nombre, proyecto, mi parte |
| 0:30-1:30 | Demo navegación: home → catálogo → filtrar por género → buscar → paginar → ficha de juego. Explicar decisiones de diseño |
| 1:30-2:30 | Demo auth: registro → login → ver navbar cambiado. Explicar validaciones y seguridad (bcrypt, sesiones, CSRF) |
| 2:30-3:30 | Demo CRUD: añadir juego a biblioteca → cambiar estado → escribir reseña → editarla → eliminarla. Mostrar responsive en móvil |
| 3:30-4:15 | Diapositiva de diseño: wireframes vs resultado final, paleta de colores, decisiones UX |
| 4:15-5:00 | Conclusión: qué he aprendido (Jinja2, Bootstrap, maquetación, trabajo en equipo), qué mejoraría |
