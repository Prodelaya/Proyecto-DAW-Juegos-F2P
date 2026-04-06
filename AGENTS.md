# AGENTS.md

This file defines repo-level instructions for any coding agent working in this repository.

## Project Overview

**f2p-catalog** is a server-rendered web application for browsing free-to-play games, writing reviews, and managing a personal library. Games are fetched from the FreeToGame API and cached locally in PostgreSQL.

## Documentation Source of Truth

- Treat `docs/` as the functional and architectural source of truth.
- Start with:
  - `docs/01-Arquitectura.md`
  - `docs/02-Estructura-y-archivos.md`
  - `docs/03-Roadmap-backend.md`
- Use `README.md` for quickstart and local run commands.
- If docs conflict, do **not** assume. Verify against code/docs and call out the discrepancy explicitly.
- When a discovery/change closes with new decisions, align the affected documentation.

## Tech Stack

- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy, PostgreSQL 15
- **Auth:** Flask-Login + Flask-Bcrypt
- **CSRF:** Flask-WTF (`CSRFProtect`)
- **Frontend:** Jinja2 templates, Bootstrap (CDN), vanilla JavaScript
- **Infra:** Docker + Docker Compose

## Architecture Rules

- Use the Flask **Application Factory** pattern in `app/__init__.py` via `create_app()`.
- Instantiate shared Flask extensions only in `app/extensions.py`.
- Keep the dependency flow one-way:

```text
.env -> config.py -> create_app() -> extensions -> decorators/models -> routes -> templates/static
```

- The app is MVC-style with Flask Blueprints and server-rendered pages.
- There is no public JSON API in project scope.

## Closed Domain Decisions

- The database has 4 tables: `users`, `games`, `reviews`, `user_library`.
- `Game.description` is **required**.
- `Game.screenshots` is stored as JSON in a single column.
- `Review.text` is **required** and constrained to 10-1000 characters.
- A review is unique per `(user_id, game_id)` but remains editable as product behavior.
- `UserLibrary.status` is stored as `String`, not SQLAlchemy `Enum`.
- Allowed library states are: `want_to_play`, `playing`, `played`.
- Library status is validated in routes/forms and in the model.
- Model relationships use `back_populates`, not `backref`.
- Timestamps (`created_at`, `updated_at`, `cached_at`) use a simple UTC strategy.
- Models should expose useful `__repr__` values without leaking sensitive data.
- For Change 1 / backend domain models, “done” includes manual PostgreSQL schema verification.

## Security and Validation

- Every POST route that changes state must use CSRF protection.
- Do not rely only on frontend validation; keep server-side validation.
- Passwords must always be hashed with bcrypt.
- Admin access is controlled with `is_admin=True` plus `@admin_required`.
- Prefer POST for state-changing actions. If docs disagree on a route shape, verify before changing behavior.

## Data and Seeds

- Seeds must be **idempotent**.
- `seeds/seed_all.py` orchestrates games -> users -> reviews -> library demo entries.
- Admin credentials come from `.env` (`ADMIN_EMAIL`, `ADMIN_PASSWORD`).
- `app/services/freetogame.py` must handle external API errors gracefully and return `None`/empty results instead of crashing the app.

## Agent Operating Rules

- Verify technical claims against code/docs before stating them as facts.
- Do not make cosmetic-only changes unless explicitly requested.
- Do not run tests or builds unless the user explicitly asks for them.
- If you find inconsistencies between docs, report them instead of inventing a version.
- Keep instructions repo-specific; avoid duplicating large sections of general project docs here.
- Write all project documentation and OpenSpec artifacts in Spanish unless the user explicitly requests another language.

## Useful Commands

```bash
# Start with Docker
docker-compose up

# Rebuild containers after dependency changes
docker-compose up --build

# Run seed inside the containerized app
docker-compose exec web python seeds/seed_all.py

# Install dependencies locally
pip install -r requirements.txt

# Run seed locally (outside Docker)
python seeds/seed_all.py
```

## Relevant Files

- `README.md`
- `docs/01-Arquitectura.md`
- `docs/02-Estructura-y-archivos.md`
- `docs/03-Roadmap-backend.md`
- `app/extensions.py`
- `app/decorators.py`
- `app/services/freetogame.py`
