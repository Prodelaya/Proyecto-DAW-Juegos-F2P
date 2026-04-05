# Arquitectura del Proyecto — Catálogo de Juegos Free-to-Play

> **Documentación relacionada:** [Estructura y archivos](02-Estructura-y-archivos.md) · [Roadmap Backend](03-Roadmap-backend.md) · [Roadmap Frontend](04-Roadmap-frontend.md) · [Memoria y defensa](05-Memoria-y-defensa.md)

---

## 1. PATRÓN: MVC (Modelo-Vista-Controlador) con Flask

```
┌─────────────────────────────────────────────────────────┐
│                      NAVEGADOR                          │
│              (HTML + CSS + JS vanilla)                   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP (GET/POST)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   FLASK (Servidor)                       │
│                                                         │
│  ┌─────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Routes  │───▶│ Controllers  │───▶│   Services    │  │
│  │ (URLs)  │    │ (lógica de   │    │ (API externa  │  │
│  │         │    │  cada ruta)  │    │  + caché BD)  │  │
│  └─────────┘    └──────┬───────┘    └───────────────┘  │
│                        │                                │
│                  ┌─────┴──────┐                         │
│                  │ Decorators │                         │
│                  │ @login_req │                         │
│                  │ @admin_req │                         │
│                  └─────┬──────┘                         │
│                        ▼                                │
│               ┌────────────────┐                        │
│               │    Models      │                        │
│               │ (SQLAlchemy)   │                        │
│               └────────┬───────┘                        │
│                        │                                │
│                        ▼                                │
│               ┌────────────────┐    ┌───────────────┐  │
│               │  PostgreSQL    │    │   Jinja2       │  │
│               │  (datos)       │    │  (templates    │  │
│               │                │    │   HTML)        │  │
│               └────────────────┘    └───────────────┘  │
└─────────────────────────────────────────────────────────┘
                       │
                       │ requests (HTTP)
                       ▼
              ┌─────────────────┐
              │  FreeToGame API │
              │  (externa)      │
              └─────────────────┘
```

---

## 2. FLUJO DE UNA PETICIÓN TÍPICA (ejemplo: ver catálogo)

1. El usuario entra a `/catalogo` en su navegador
2. Flask recibe la petición y la enruta al controlador correspondiente
3. El controlador consulta los juegos en la base de datos local (ya cacheados)
4. Los datos se paginan (20 juegos por página) y se pasan a la plantilla Jinja2
5. Jinja2 genera el HTML con los datos insertados
6. Flask devuelve el HTML al navegador
7. El navegador muestra la página con Bootstrap y JS vanilla

---

## 3. FLUJO DE LA CARGA INICIAL DE DATOS (seed)

1. Se ejecuta `seed_all.py` una única vez (o se re-ejecuta manualmente desde el panel admin)
2. Paso 1: llama a la API FreeToGame y cachea los ~400 juegos en la tabla `games`
3. Paso 2: crea usuarios demo (5 normales + 1 admin) con contraseñas hasheadas
4. Paso 3: genera ~50-80 reseñas realistas repartidas entre usuarios demo y juegos populares
5. Paso 4: crea algunas entradas de biblioteca para los usuarios demo con estados variados para reforzar la demo de perfil y biblioteca
6. A partir de ahí, la app tiene datos para funcionar y verse completa

---

## 4. FLUJO DE PERMISOS Y ROLES

```
Usuario anónimo ──► Ve catálogo, fichas, reseñas de otros
                    NO puede: escribir reseña, biblioteca, perfil

Usuario logueado ──► Todo lo anterior +
                     Escribir/editar/eliminar SUS reseñas
                     Gestionar SU biblioteca
                     Ver SU perfil

Admin (is_admin) ──► Todo lo anterior +
                     Eliminar CUALQUIER reseña
                     Panel /admin/resenas con listado global
                     Botón "Actualizar catálogo" (re-seed manual)
```

---

## 5. PAGINACIÓN

El catálogo muestra **20 juegos por página** con paginación server-side (Flask-SQLAlchemy `paginate()`). El template muestra controles de paginación (Anterior / Siguiente / números de página).

**Orden por defecto** (sin filtro seleccionado): los juegos se muestran por **orden alfabético** (A-Z). El usuario puede cambiar a ordenar por popularidad (más reseñas/mejor valorados) desde el selector de ordenación.

---

## 6. SEGURIDAD

### Protección CSRF

Todos los formularios POST incluyen un **token CSRF** generado por Flask-WTF (`CSRFProtect`). Se inicializa en `extensions.py` y se inyecta en cada formulario con `{{ csrf_token() }}` o `{{ form.hidden_tag() }}`. Esto incluye acciones que cambian estado como crear/editar/eliminar contenido o cerrar sesión. Peticiones POST sin token válido devuelven 400 Bad Request.

### Validaciones server-side

| Campo | Regla |
|-------|-------|
| `username` | 3–30 caracteres, solo alfanuméricos y guiones bajos, único |
| `email` | Formato email válido, único |
| `password` | Mínimo 8 caracteres |
| `review.text` | 10–1000 caracteres |
| `review.rating` | Entero entre 1 y 5 |
| `library.status` | Valor de la lista: `want_to_play`, `playing`, `played` |

### Rate-limit en actualización de catálogo

La ruta `POST /admin/actualizar-juegos` tiene un **cooldown de 30 segundos**. En servidor se verifica el `cached_at` del último juego actualizado para rechazar peticiones demasiado frecuentes. En frontend se puede añadir una cuenta atrás visual, pero es una mejora opcional y no un requisito funcional.

### Contraseñas

Se hashean con **bcrypt** (vía Flask-Bcrypt). Nunca se almacenan en texto plano.

---

## 7. MAPA DE DEPENDENCIAS

```
.env ──────────────► config.py ──────────────► __init__.py (create_app)
                                                    │
                     extensions.py ◄────────────────┤
                     (db, login_manager,            │
                      bcrypt, csrf)                  │
                          │                          │
                     decorators.py                   │
                     (@admin_required)               │
                          │                          │
            ┌─────────────┼─────────────┐           │
            ▼             ▼             ▼           │
        models/       models/       models/         │
        user.py       game.py      review.py        │
            │             │         library.py       │
            │             │             │           │
            └──────┬──────┴─────────────┘           │
                   ▼                                │
              routes/*.py ◄─────────────────────────┘
              (incluido admin.py)        (registra blueprints)
                   │
                   ▼
            templates/*.html ──► partials/*.html
                   │
                   ▼
              static/ (css, js, img)

seeds/seed_all.py ──► seeds/seed_games.py ──► services/freetogame.py
                  ──► seeds/seed_users.py     models/game.py
                  ──► seeds/seed_reviews.py    models/user.py
                       (todos necesitan)       models/review.py
                       app/__init__.py         config.py
                       (contexto Flask)
```

**Regla simple:** los archivos de abajo dependen de los de arriba. Nunca al revés.

---

## 8. DECISIONES TÉCNICAS

| Decisión | Justificación |
|----------|---------------|
| **Cachear juegos en BD local** | La API FreeToGame no es fiable (puede caer). Tener los datos locales garantiza que la app funciona siempre |
| **`db.create_all()` sin migraciones** | Es un MVP para aprobar. No se prevén cambios de esquema en producción. Flask-Migrate añadiría complejidad innecesaria |
| **`is_admin` como booleano** | Solo hay 2 roles (usuario y admin). Un sistema de roles/permisos sería sobreingeniería |
| **Contraseñas con bcrypt** | Estándar de la industria, no SHA/MD5 |
| **CSRF con Flask-WTF** | Protección estándar contra ataques CSRF en formularios |
| **Sin tests automatizados** | Pruebas manuales documentadas en la memoria. Alcance ajustado al MVP del TFG |
| **Actualización de catálogo manual** | No es cron ni automático. Un botón admin simple demuestra que se pensó en el mantenimiento de datos |
