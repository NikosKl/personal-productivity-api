# Personal Productivity & Analytics API

A FastAPI-based REST API for managing tasks and habits, with authentication, analytics and rate limiting.

Built with **FastAPI**, **PostgreSQL** and **SQLAlchemy**. This API allows users to:
- Manage tasks and track completion
- Build daily or weekly habits
- Track habit streaks
- View productivity analytics

The project demonstrates backend engineering practices including authentication, database migrations, automated testing, CI pipelines, rate limiting and production development.

---

## Live API

https://personal-productivity-api.onrender.com

Interactive documentation: 

/docs

Alternative documentation:

/redoc

---

## Features

### Authentication
- User registration
- JWT login authentication
- Protected endpoints
- Rate limiting on authentication routes

### Tasks
- Create, update and delete tasks
- Mark tasks as completed or reset
- Pagination and filtering
- Task productivity statistics

### Habits
- Create, daily or weekly habits
- Log habit completions
- Prevent duplicate logs
- Calculate habit streaks

### Analytics
- Task productivity summary
- Habit analytics
- Combined productivity dashboard

### Infrastructure
- PostgreSQL database
- Alembic database migrations
- Automated testing with Pytest
- CI pipeline with GitHub actions
- Production deployment on Render

---

## Tech Stack

**Framework**
- FastAPI

**Database**
- PostgreSQL

**ORM**
- SQLalchemy 2.0

**Migrations**
- Alembic

**Authentication**
- JWT

**Testing**
- Pytest

**CI/CD**
- GitHub Actions

**Deployment**
- Render

---

## Local Setup

### Clone the repository
```bash
git clone https://github.com/NikosKl/personal-productivity-api.git
cd personal-productivity-api
```

### Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate # on macOS/Linux
venv\Scripts\activate # on Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```
### Configure environment variables

```bash
cp .env.example .env
```

### Run database migrations

```bash
alembic upgrade head
```

### Start the development server

```bash
fastapi dev app/main.py
```
