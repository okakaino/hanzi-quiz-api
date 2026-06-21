# Hanzi Quiz API

A REST API backend for a Mandarin Chinese **picture-quiz** learning app. It shows a picture and asks the user to identify the Chinese character (汉字) and its pinyin pronunciation from multiple-choice options.

Built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, containerized with **Docker**, and deployed on Render.

## Live demo

- API: `https://hanzi-quiz-api.onrender.com`
- Interactive docs: `https://hanzi-quiz-api.onrender.com/docs`

## Features

- Full CRUD for vocabulary items (character, pinyin, English, image)
- Multiple-choice quiz generation (1 correct + 2 distractors)
- **Server-side answer validation** — the correct answer is never sent to the client
- PostgreSQL persistence via the SQLAlchemy ORM
- Automated tests with pytest
- Fully containerized with Docker

## Tech stack

FastAPI · PostgreSQL · SQLAlchemy 2.0 · Pydantic · Docker · pytest · uv

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET    | `/items` | List all vocabulary items |
| POST   | `/items` | Create a new item |
| GET    | `/items/{id}` | Get a single item |
| GET    | `/quiz` | Get a quiz question (image + shuffled options) |
| POST   | `/quiz/check` | Submit answers and get correctness |

## Running locally

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/), and PostgreSQL.

```bash
git clone git@github.com:okakaino/hanzi-quiz-api.git
cd hanzi-quiz-api
uv sync

createdb hanzi                # create the database
cp .env.example .env          # then set DATABASE_URL in .env

uv run fastapi dev src/hanzi_quiz_api/main.py
```

Open http://127.0.0.1:8000/docs

## Running with Docker

```bash
docker build -t hanzi-quiz-api .
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg://USER@host.docker.internal:5432/hanzi" \
  hanzi-quiz-api
```

## Running tests

```bash
createdb hanzi_test
uv run pytest
```

## Notes & limitations

- Images currently use placeholder URLs.
- A quiz requires at least 3 items in the database.