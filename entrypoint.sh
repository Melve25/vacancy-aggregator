set -e

echo "Running Alembic migrations..."
un run alembic upgrade head

echo "Starting bot..."
uv run uvicorn app.main:app --hots 0.0.0.0 --port 8000 --reload