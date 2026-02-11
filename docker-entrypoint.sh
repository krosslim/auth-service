#!/usr/bin/env sh
set -e

echo "==> Running migrations..."
alembic upgrade head

echo "==> Starting application..."
exec uv run uvicorn src.app.main:app --host 0.0.0.0 --port 8000