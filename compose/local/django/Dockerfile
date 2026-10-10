FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY ./apps/api/pyproject.toml ./apps/api/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

COPY ./apps/api/ ${APP_HOME}/

COPY ./compose/local/django/entrypoint.sh /entrypoint.sh
COPY ./compose/local/django/start /start

COPY ./compose/local/django/celery/worker/start /start-worker
COPY ./compose/local/django/celery/beat/start /start-beat
COPY ./compose/local/django/celery/flower/start /start-flower

RUN sed -i 's/\r$//g' \
  /entrypoint.sh \
  /start \
  /start-worker \
  /start-beat \
  /start-flower

RUN chmod +x \
  /entrypoint.sh \
  /start \
  /start-worker \
  /start-beat \
  /start-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]