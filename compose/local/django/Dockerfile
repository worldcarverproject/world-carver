FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

COPY ./apps/api/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

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