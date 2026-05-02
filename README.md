# JobPilot

FastAPI backend for JobPilot: users, jobs, JWT auth, and email flows (verification / password reset).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — install from the official docs.
- Python **3.12+** (see `.python-version`; uv will respect it).
- **PostgreSQL** — connection string goes in `DATABASE_URL`.

## Setup

Clone the repo and from the project root:

```bash
uv sync
```

This installs dependencies from `pyproject.toml` using the locked versions in `uv.lock`.

## Environment

Create a `.env` file in the project root (it is gitignored). Minimum required for the API and database:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | SQLAlchemy URL, e.g. `postgresql://user:password@localhost:5432/jobpilot` |
| `SECRET_KEY` | Secret for signing JWTs |

Optional:

| Variable | Default / notes |
|----------|-----------------|
| `ALGORITHM` | `HS256` |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` / `SMTP_PASSWORD` | SMTP credentials |
| `SMTP_FROM` | Falls back to `SMTP_USER` or a placeholder |
| `FRONTEND_VERIFY_URL` | `http://localhost:3001/verify` |
| `FRONTEND_RESET_PASSWORD_URL` | `http://localhost:3001/reset-password` |

## Run the API

Development (auto-reload):

```bash
uv run uvicorn main:app --reload
```

By default the app is served at `http://127.0.0.1:8000`. Interactive docs: `http://127.0.0.1:8000/docs` (Swagger UI).

On startup, SQLAlchemy creates tables from the models (`Base.metadata.create_all`).

## Project layout

- `main.py` — FastAPI app, CORS, routers
- `routes/` — HTTP routers
- `services/` — business logic
- `repositories/` — data access
- `models/` — SQLAlchemy / domain models
- `schemas/` — Pydantic schemas
- `core/` — database session, security helpers

## License

Add your license here if applicable.
