# Propuesta — `backend-authentication`

## Estado
draft

## Título
Implementar autenticación SSR base y visibilidad coherente de sesión

## Intención

Cerrar la autenticación mínima del producto con registro, login y logout seguros, más un contrato SSR explícito para `login.html`, `register.html` y navbar autenticada, sin adelantar flujos privados del Change 4.

## Problema

La app ya tiene catálogo público SSR y wiring parcial de Flask-Login, pero `app/routes/auth.py` sigue en placeholder, `register_routes()` no registra auth y la navbar no refleja sesión. Sin este change no existe acceso autenticado verificable ni base consistente para futuras rutas con `@login_required`.

## Alcance

Incluye: `GET|POST /registro` con validación robusta TFG, unicidad explícita de email/username y redirect a login tras éxito; `GET|POST /login` solo por email, errores específicos de campos/formato y mensaje genérico para credenciales inválidas, respetando `next` válido; `POST /logout` con CSRF; redirección a home si usuario autenticado entra a `/login` o `/registro`; configuración operativa de `login_manager` (`login_view`, `login_message`); contrato SSR explícito de `app/templates/auth/login.html`, `app/templates/auth/register.html` y `app/templates/partials/navbar.html` mostrando `username` autenticado.

## Fuera de alcance

CRUD de reseñas, biblioteca, perfil, UI/admin visible, CTAs pasivos a acciones futuras, endurecimiento global de errores y cualquier expansión funcional reservada para el Change 4.

## Criterios de aceptación

1. Registro exige `username`, `email`, `password` mínima de 8 y confirmación; informa por separado email o username ya usados.
2. Login autentica solo por email; errores de campos/formato son específicos y las credenciales inválidas usan mensaje genérico.
3. Usuario autenticado que visita `/login` o `/registro` es redirigido a `/`.
4. Logout ocurre solo por `POST` protegido con CSRF.
5. Navbar SSR muestra `username` cuando hay sesión activa y no expone UI especial de admin.
6. Queda explícito el contrato Jinja mínimo de `login.html`, `register.html` y navbar autenticada para soportar `@login_required` futuro.

## Riesgos

- Medio: mezclar auth con áreas privadas puede invadir el alcance del Change 4.
- Medio: manejo incorrecto de `next` puede abrir redirecciones inseguras o UX inconsistente.
- Bajo: desalineación entre mensajes flash/errores y el contrato SSR esperado.

## Justificación

Este recorte habilita identidad y sesión, que son prerequisitos del backend privado, pero preserva una frontera nítida: autenticar y hacer visible el estado autenticado, SIN implementar todavía acciones privadas del usuario.

## Rollback plan

Revertir blueprint auth, wiring en `register_routes()`/`create_app()`, contrato de templates auth y variante autenticada de navbar; mantener intactas las rutas públicas SSR y la configuración de modelos/extensiones ya existente.

## Artefactos

- Archivo: `openspec/changes/backend-authentication/proposal.md`
- Módulos/paquetes afectados: `app/routes/auth.py`, `app/routes/__init__.py`, `app/__init__.py`, `app/extensions.py`, `app/templates/auth/login.html`, `app/templates/auth/register.html`, `app/templates/partials/navbar.html`, `app/templates/base.html`, parciales de flash si hiciera falta al contrato.

## Siguiente paso recomendado

- `sdd-spec`
- `sdd-design`

## Resolución de skills

- fallback-path
