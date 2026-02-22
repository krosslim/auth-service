# auth-service

Сервис аутентификации на FastAPI с поддержкой Telegram WebApp `init_data`, выпуском пары токенов (`access` + `refresh`) и ротацией refresh-токенов.

## Что делает сервис

- Аутентифицирует пользователя через провайдера (сейчас: `telegram`)
- Хранит пользователей и identity в PostgreSQL
- Выдает:
  - `access_token` (JWT, `RS256`)
  - `refresh_token` (случайный токен, хранится в БД как HMAC-SHA256 hash)
- Поддерживает:
  - обновление токенов (`/v1/refresh`)
  - отзыв refresh-токена (`/v1/revoke`)

## Технологии

- Python 3.13+
- FastAPI
- SQLAlchemy (async) + asyncpg
- Alembic
- Dishka (DI)
- uv (управление зависимостями и запуск)
- PostgreSQL 18 (в `docker-compose`)

## Структура проекта

```text
src/
  api/            # роуты, схемы запросов/ответов, обработчики ошибок
  app/            # конфигурация и создание FastAPI приложения
  domain/         # use cases, модели, исключения, провайдеры
  ioc/            # DI-провайдеры
  storage/        # база данных: engine, модели, репозитории
migrations/       # Alembic migrations
tests/            # интеграционные тесты
```

## Переменные окружения

Создай `.env` на основе шаблона:

```bash
cp .env.example .env
```

Минимально заполни:

- `POSTGRES_HOST` (например, `localhost`)
- `POSTGRES_PORT` (для docker-compose: `5433`)
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_INIT_DATA_LIFETIME` (например, `3600`)
- `REFRESH_TOKEN_HMAC_SECRET`
- `REFRESH_TOKEN_TTL_SECONDS` (например, `2592000`)
- `ACCESS_TOKEN_PRIVATE_KEY_PATH` (например, `private.pem`)
- `ACCESS_TOKEN_PUBLIC_KEY_PATH` (например, `public.pem`)
- `ACCESS_TOKEN_TTL_SECONDS` (например, `3600`)

Остальные параметры можно оставить пустыми, тогда будут использованы дефолты из `src/app/config.py`.

## Генерация ключей

### RSA-пара для access token (`RS256`)

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

### HMAC ключ для refresh token

```bash
openssl rand -base64 32
```

Скопируй результат в `REFRESH_TOKEN_HMAC_SECRET`.

## Локальный запуск (без Docker)

1. Установи зависимости:

```bash
uv sync
```

2. Подними PostgreSQL (любым удобным способом) или запусти только БД из compose:

```bash
docker compose up -d postgres
```

3. Примени миграции:

```bash
uv run alembic upgrade head
```

4. Запусти приложение:

```bash
uv run uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Документация будет доступна по адресу: `http://127.0.0.1:8000/docs`

## Запуск через Docker Compose

```bash
docker compose up --build
```

При старте контейнер приложения автоматически выполняет:

```text
alembic upgrade head
uv run uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

## API

### `POST /v1/auth`
Аутентификация через провайдера.

Тело запроса:

```json
{
  "provider": "telegram",
  "init_data": "query_id=...&user=...&auth_date=...&hash=..."
}
```

Ответ `200`:

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<token>",
  "token_type": "Bearer"
}
```

### `POST /v1/refresh`
Обновить пару токенов по refresh-токену.

Тело запроса:

```json
{
  "refresh_token": "<token>"
}
```

### `POST /v1/revoke`
Отозвать refresh-токен.

Тело запроса:

```json
{
  "refresh_token": "<token>"
}
```

Ответ: `204 No Content`.

## Примеры curl

```bash
curl -X POST 'http://127.0.0.1:8000/v1/auth' \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": "telegram",
    "init_data": "query_id=...&user=...&auth_date=...&hash=..."
  }'
```

```bash
curl -X POST 'http://127.0.0.1:8000/v1/refresh' \
  -H 'Content-Type: application/json' \
  -d '{"refresh_token":"<token>"}'
```

```bash
curl -X POST 'http://127.0.0.1:8000/v1/revoke' \
  -H 'Content-Type: application/json' \
  -d '{"refresh_token":"<token>"}'
```

## Миграции

Создать новую миграцию:

```bash
uv run alembic revision --autogenerate -m "your message"
```

Применить миграции:

```bash
uv run alembic upgrade head
```

Откатить на 1 шаг:

```bash
uv run alembic downgrade -1
```

## Тесты

Запуск всех тестов:

```bash
uv run pytest
```

Запуск только интеграционных:

```bash
uv run pytest -m integration
```

## Линтинг

```bash
uv run ruff check .
```

## OpenAPI экспорт

Сгенерировать OpenAPI JSON/YAML в `docs/`:

```bash
uv run python -m src.utils.docs_gen
```
