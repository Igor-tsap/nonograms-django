# Nonograms

A full-stack pet project for creating, solving, and managing Nonogram puzzles.

## Overview

This repository includes:

- `backend/`: FastAPI backend with MySQL database support and puzzle CRUD APIs.
- `frontend/`: Next.js application for browsing puzzles, creating new puzzles, and editing user-owned puzzles.
- `src/`: Shared backend service code for puzzles, users, and attempts.

## Features

- Create and edit Nonogram puzzles.
- Browse public puzzles and view details.
- User authentication and puzzle ownership.
- Track solve attempts and puzzle metadata.

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic
- Frontend: Next.js, TypeScript, React
- Database: MySQL setup via Docker / Docker Compose

## Getting Started

### Backend

1. Activate the virtual environment:

```bash
source backend/env/bin/activate
```

2. Install dependencies if needed:

```bash
pip install -r backend/requirements.txt
```

3. Run the backend locally:

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Run the frontend:

```bash
npm run dev
```

## Notes

This project is intended as a personal showcase for building a puzzle application with a modern web stack.
