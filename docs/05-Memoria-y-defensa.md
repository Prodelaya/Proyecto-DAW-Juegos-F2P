# Memoria del TFG y Defensa en Vídeo

> **Documentación relacionada:** [Arquitectura](01-Arquitectura.md) · [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Roadmap Frontend](04-Roadmap-frontend.md)

---

## 1. ESTRUCTURA DE LA MEMORIA (40-60 páginas)

El documento final debe seguir estrictamente esta estructura, según la guía oficial del módulo de Proyecto DAW.

| Cap | Título | Págs | Quién escribe |
|-----|--------|------|--------------|
| 1 | **Portada** (título, nombres, ciclo, curso, convocatoria) | 1 | Ambos |
| 2 | **Índice** (automático) | 1 | Auto |
| 3 | **Resumen Ejecutivo** — Problema, solución, tecnologías usadas, resultados y posibles mejoras futuras (MVP). | 1 | Ambos |
| 4 | **1. Introducción** — Contexto del mercado F2P, problema actual (dispersión de juegos/información) y propuesta general de nuestra app. | 2-3 | Pablo Laya |
| 5 | **2. Justificación, objetivos y alcance** — Por qué es útil. Objetivo general y específicos. Tabla de "Alcance" y "Fuera de alcance" (ej. sin pasarela de pagos real). | 2-3 | Pablo Laya |
| 6 | **3. Análisis y planificación del proyecto** — Requisitos (RF/RNF), Historias de Usuario, Casos de Uso (UML), cronograma (texto/Gantt resumen de los roadmaps) y Gestión de Riesgos (tabla). | 6-8 | Ambos |
| 7 | **4. Diseño del sistema** — Arquitectura MVC (Flask), Modelo E-R (PostgreSQL), diseño de API (FreeToGame externa) y UI/UX (Wireframes, paleta). | 6-8 | Ambos |
| 8 | **5. Desarrollo e implementación** — Estructura del repositorio, decisiones técnicas (por qué cachear, uso de bcrypt). Fragmentos de código relevantes: Backend (rutas, seed) y Frontend (Jinja2, responsive). | 8-10 | Ambos |
| 9 | **6. Pruebas y validación** — Plan de pruebas. Tabla de pruebas manuales (ej. Login inválido, Reserva sin plazas -> añadir juego/reseña, validaciones CSRF). Mínimo 15 casos, con capturas. | 3-4 | Pablo Pérez |
| 10 | **7. Despliegue y puesta en producción** — Checklist de despliegue. Explicación de cómo se levantaría en un VPS usando Docker, configuración de `.env` para producción y Nginx/HTTPS. | 3-4 | Pablo Laya |
| 11 | **8. Seguridad y protección de datos** — Seguridad técnica (bcrypt, CSRF, protección de rutas) y RGPD básico (qué datos se guardan: email, y finalidad). | 2-3 | Pablo Pérez |
| 12 | **9. Manual de usuario** — Capturas explicadas paso a paso (Registro, buscar juego, añadir a biblioteca, dejar reseña). | 3-4 | Pablo Pérez |
| 13 | **10. Manual técnico** — Requisitos previos, clonar repo, variables `.env` locales, comandos de ejecución (`docker-compose up`, seeds). | 2-3 | Pablo Laya |
| 14 | **11. Conclusiones y líneas futuras** — Balance del proyecto, dificultades superadas (ej. consumir API rate-limited) y mejoras futuras. | 1-2 | Ambos |
| 15 | **Bibliografía/Webgrafía** — Enlaces a Flask docs, FreeToGame API, tutoriales de Bootstrap y recursos gráficos. | 1 | Ambos |
| | **TOTAL ESTIMADO** | **42-57** | *(Cumple el requisito de 40-60 páginas)* |

---

## 2. CONTENIDO DE LA DEFENSA EN VÍDEO (5 MINUTOS CADA UNO)

> **Nota:** La normativa prohíbe leer. Hay que usar una presentación (Canva/PPT) como apoyo visual mientras se explica a cámara (herramienta sugerida: Loom).

### Pablo Laya — Backend (5 minutos)

| Min | Contenido |
|-----|-----------|
| 0:00-0:30 | **Presentación:** Nombre, título del proyecto (Catálogo F2P) y el problema que venimos a resolver trabajando en equipo. |
| 0:30-1:30 | **Arquitectura y API:** Mostrar el diagrama de flujo MVC. Explicar brevemente cómo consumimos la API externa `FreeToGame` de forma controlada (el script `seed`). |
| 1:30-2:30 | **Base de Datos:** Mostrar el modelo Entidad-Relación. Explicar por qué tenemos 4 tablas (Usuarios, Juegos cacheados, Reseñas, Biblioteca) y cómo se relacionan. |
| 2:30-3:30 | **Demo de Backend:** Capturas o navegación rápida mostrando el paginador de juegos funcionando (consultas a base de datos) y la lógica de validación (qué pasa si intento meter un rating falso). |
| 3:30-4:15 | **Panel Admin:** Demostración en vivo de un usuario "Administrador". Mostrar la protección de rutas con el decorador personalizado `@admin_required` y la función de "Actualizar catálogo" o eliminar reseñas indeseadas. |
| 4:15-5:00 | **Conclusión Personal:** Qué ha sido lo más difícil (ej. manejar los rate-limits de la API, Flask-Login) y qué he aprendido. Despedida. |

### Pablo Pérez — Frontend y UX (5 minutos)

| Min | Contenido |
|-----|-----------|
| 0:00-0:30 | **Presentación:** Nombre, mención rápida al proyecto y mi responsabilidad (Frontend, UI/UX y Pruebas). |
| 0:30-1:30 | **Diseño y UX:** Mostrar algunos wireframes iniciales y compararlos con el resultado visual final. Explicar la elección de la paleta oscura/gaming y el uso de Bootstrap + Jinja2. |
| 1:30-2:30 | **Demo Navegación:** Recorrido por la web emulando a un usuario anónimo: buscar un juego, usar los filtros, ver una ficha detallada. Destacar el diseño *responsive* mostrando cómo se adapta a móvil. |
| 2:30-3:30 | **Demo Seguridad y Usuarios:** Proceso de registro (explicando mitigación CSRF visual) y login exitoso. Añadir un juego a "Mi biblioteca" y dejar una reseña (validación visual del formulario). |
| 3:30-4:15 | **Testing:** Mostrar un ejemplo de la tabla de casos de prueba manuales (ej. qué pasó al intentar enviar datos inválidos o contenido no esperado y cómo lo bloquean las validaciones server-side y el renderizado seguro de Jinja2). |
| 4:15-5:00 | **Conclusión Personal:** Dificultad principal (ej. adaptar componentes de Bootstrap, herencia en Jinja2) e impresiones del trabajo en equipo. Despedida. |
