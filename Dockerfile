FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv sync --locked --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["celery", "-A", "workers.celery_app", "worker", "-l", "INFO", "-P", "prefork", "-c", "2"]
