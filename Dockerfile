ARG PY_IMAGE=python:3.13-slim
ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.4.20

# -------- build stage --------
FROM ${PY_IMAGE} AS build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /app

COPY --from=${UV_IMAGE} /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev \
 && rm -rf /tmp/uv-cache

# -------- production stage --------
FROM ${PY_IMAGE} AS prod
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN adduser --disabled-password --gecos "" --home /app appuser

COPY --from=build /app/.venv /app/.venv

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD []