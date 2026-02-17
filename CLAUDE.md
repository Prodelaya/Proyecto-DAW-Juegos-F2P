# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**f2p-catalog** — A free-to-play game catalog web application (TFG/final project). Users can browse games, write reviews, and manage a personal library. Games are cached locally from the FreeToGame API.

**Status:** Project is being built from design docs in `docs/`. Refer to those for detailed specs.

## Tech Stack

- **Backend:** Python 3.11, Flask (Application Factory pattern), SQLAlchemy (Flask-SQLAlchemy), PostgreSQL 15
- **Auth:** Flask-Login + Flask-Bcrypt
- **CSRF:** Flask-WTF (CSRFProtect) — every POST form must include a CSRF token
- **Frontend:** Jinja2 templates, Bootstrap (CDN), vanilla JS
- **Infra:** Docker + Docker Compose

## Commands

```bash
# Start the application (Flask + PostgreSQL)
docker-compose up

# Rebuild after dependency changes
docker-compose up --build

# Seed the database (games from API + demo users + sample reviews)
python seeds/seed_all.py

# Clean restart
docker-compose down -v && docker-compose up --build

# Install dependencies locally (outside Docker)
pip install -r requirements.txt
```

## Architecture

**Pattern:** MVC with Flask Blueprints. Application Factory in `app/__init__.py` (`create_app()`).

**Dependency flow (never reversed):**
```
.env → config.py → __init__.py (create_app)
                        ↓
extensions.py (db, login_manager, bcrypt, csrf) — shared singletons, avoids circular imports
    ↓
decorators.py (@admin_required)
    ↓
models/ (User, Game, Review, UserLibrary)
    ↓
routes/ (Flask Blueprints, registered via routes/__init__.py → register_routes(app))
    ↓
templates/ (Jinja2, all extend base.html) → static/ (css, js, img)
```

**Key files:**
- `app/extensions.py` — Single source of truth for `db`, `login_manager`, `bcrypt`, `csrf`. Models and routes import from here.
- `app/decorators.py` — `@admin_required` decorator (used with `@login_required`)
- `app/services/freetogame.py` — HTTP client for FreeToGame API (`fetch_all_games()`, `fetch_game_detail(api_id)`). Returns None/empty list on error, never raises.
- `seeds/` — Idempotent seed scripts. `seed_all.py` orchestrates: games → users → reviews.

## Database

4 tables, no migrations (`db.create_all()` only):

| Table | Key constraints |
|-------|----------------|
| `users` | username unique (3-30 chars, alphanumeric + underscores), email unique |
| `games` | api_id unique (FreeToGame ID) |
| `reviews` | UniqueConstraint(user_id, game_id), rating 1-5, text 10-1000 chars |
| `user_library` | UniqueConstraint(user_id, game_id), status in ['want_to_play', 'playing', 'played'] |

## Roles & Permissions

Two roles only: regular user (`is_admin=False`) and admin (`is_admin=True`).
- Anonymous: browse catalog, view game details and reviews
- Logged in: write/edit/delete own reviews, manage personal library, view profile
- Admin: delete any review, access `/admin/resenas` panel, trigger manual catalog update (30s cooldown)

## Routes (all server-rendered, no JSON API)

Blueprints: `main_bp`, `auth_bp`, `games_bp`, `reviews_bp`, `library_bp`, `profile_bp`, `admin_bp`. Catalog pagination is 20 per page, default sort alphabetical A-Z.

## Conventions

- All Flask extensions are instantiated in `extensions.py`, initialized in `create_app()`
- Every POST route must have CSRF protection (`{{ csrf_token() }}` in forms)
- Seeds must be idempotent (check existence before insert, safe to re-run)
- Admin credentials come from `.env` (`ADMIN_EMAIL`, `ADMIN_PASSWORD`)
- Service functions handle their own errors (return None/empty, never crash the app)
- Templates use Jinja2 inheritance from `base.html` and `{% include %}` for partials (navbar, footer, game_card, flash_messages, pagination)
- Server-side validation on all user input (see validation rules in `docs/01-Arquitectura.md` §6)

## Environment Variables

```
DATABASE_URL=postgresql://...
SECRET_KEY=...
FLASK_ENV=development
FREETOGAME_API_URL=https://www.freetogame.com/api
ADMIN_EMAIL=...
ADMIN_PASSWORD=...
```
