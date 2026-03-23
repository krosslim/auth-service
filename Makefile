APP = src.app.main:app
HOST = 0.0.0.0
PORT = 8000

.PHONY: help run lint format test run-prod

help:
	@echo "Available targets:"
	@echo "  make run       - Local run"
	@echo "  make lint      - Ruff check with fixes"
	@echo "  make format    - Ruff format"
	@echo "  make test      - Run pytest"
	@echo "  make run-prod  - Production run"

run:
	uv run uvicorn $(APP) --reload

lint:
	uv run ruff check src --fix

format:
	uv run ruff format src

test:
	uv run pytest

run-prod:
	uv run uvicorn $(APP) --host $(HOST) --port $(PORT)
