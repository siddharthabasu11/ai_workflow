# Atlas

Atlas is a full-stack AI codebase analysis platform that takes a GitHub repository, computes structural code metrics, and generates an engineering report using the OpenAI API.

## Features

* Clone and analyze GitHub repositories
* Compute file count, lines of code, language distribution, and largest files
* Generate AI-written engineering reports from repository metrics and source-code context
* Process repositories asynchronously with Celery and Redis
* Store repository and analysis data in PostgreSQL
* Display live analysis status and results in a React/TypeScript frontend

## Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, Alembic, Celery, Redis, GitPython, OpenAI API

**Frontend:** React, TypeScript, Vite

## Pipeline

```text
GitHub Repository
      ↓
FastAPI
      ↓
Celery + Redis
      ↓
Clone Repository
      ↓
Codebase Analysis
      ↓
OpenAI Engineering Report
      ↓
PostgreSQL + React Frontend
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/siddharthabasu11/ai_workflow.git
cd ai_workflow
```

Install the backend dependencies and configure PostgreSQL, Redis, and the required environment variables.

Start the API:

```bash
cd backend
uvicorn app.main:app --reload
```

Start the Celery worker in another terminal:

```bash
cd backend
celery -A app.core.celery_app.celery_app worker --loglevel=info
```

Start the frontend:

```bash
cd frontend
npm install
npm run dev
```
