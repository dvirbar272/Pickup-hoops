# 🏀 Pick-Up Hoops

A local service for coordinating pick-up basketball games. Built with FastAPI, SQLModel, and Streamlit.

> **This is Part 2 of a multi-part project.** This part adds a Streamlit dashboard that communicates with the Part 1 FastAPI backend. Both services must be running together for the app to work.

---

## Project Overview

| Part | Focus | Status |
|---|---|---|
| Part 1 | FastAPI CRUD backend + SQLite persistence | ✅ Done |
| Part 2 | Streamlit dashboard UI talking to the API | ✅ Done |
| Part 3 | Multi-service stack with dedicated persistence layer + runbook | 🔜 Upcoming |

---

## Tech Stack

- **Python 3.12** (managed with `uv`)
- **FastAPI** — REST API layer
- **SQLModel + SQLite** — ORM and local database
- **Streamlit** — interactive web dashboard
- **Pytest** — automated testing

---

## Setup & Running

at the moment,This project requires **two terminals running simultaneously** — one for the API, one for the dashboard.

**1. Install dependencies**
```bash
uv sync
```

**2. Start the API server** (Terminal 1)
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.  
Interactive API docs (Swagger UI): `http://localhost:8000/docs`

**3. Start the Streamlit dashboard** (Terminal 2)
```bash
streamlit run dashboard.py
```
The dashboard will open automatically at `http://localhost:8501`.

> ⚠️ The API must be running before you open the dashboard. If the API is not running, the dashboard will show connection errors.

---

## Dashboard Features

- **Courts** — add, update, and delete basketball courts
- **Players** — manage players and their skill levels
- **Games** — schedule games, update status, register players
- **Upcoming Games** — filtered view of open games scheduled in the future
- Data is cached per session with a manual **Refresh** button to reload

---

## Running Tests

Tests use an in-memory SQLite database — no setup required.

```bash
uv run python -m pytest
```

---

## Project Structure

```
.
├── main.py          # FastAPI app and all route definitions
├── models.py        # SQLModel entity definitions (Court, Player, Game)
├── database.py      # DB engine and session management
├── dashboard.py     # Streamlit dashboard (Part 2)
├── pyproject.toml   # Project metadata and dependencies
└── database.db      # Auto-generated SQLite file (local only, not committed)
```
