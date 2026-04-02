# 🏀 Pick-Up Hoops API

A service for coordinating pick-up basketball games. Built with FastAPI and SQLModel.

---

## Tech Stack

- **Python 3.12** (managed with `uv`)
- **FastAPI** — API layer
- **SQLModel + SQLite** — ORM and local database
- **Pytest** — testing

---

## Setup

**1. Install dependencies**
```bash
uv sync
```

**2. Run the development server**
```bash
uvicorn main:app --reload
```

**3. Open the interactive API docs**
```
http://localhost:8000/docs
```

---





## Running Tests

To run the automated test suite using an in-memory database:
uv run python -m pytest

---

## Project Structure

```
.
├── main.py          # FastAPI app and route definitions
├── models.py        # SQLModel entity definitions
├── database.py      # DB engine and session management
├── pyproject.toml   # Project metadata and dependencies
└── database.db      # Auto-generated SQLite file (local only)
```