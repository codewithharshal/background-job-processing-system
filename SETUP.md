# Setup and Testing

## Requirements

- Docker Desktop with the Docker engine running.
- Python 3.14 or later.
- `uv` installed and available on the command line.

## Start MySQL, Redis, and Celery

From the project root:

```bash
docker compose up --build --force-recreate
```

The services use these internal addresses:

```text
MySQL: mysql:3306
Redis: redis:6379
```

MySQL is published to the host as `localhost:3307` so it does not conflict with a local MySQL installation.

Check service state:

```bash
docker compose ps
docker compose logs -f celery-worker
```

Check MySQL readiness:

```bash
docker compose exec mysql mysqladmin ping -h localhost -padmin123
```

Expected output contains:

```text
mysqld is alive
```

## Run migrations

The API runs on the host, so Alembic uses the published MySQL port:

```bash
uv run alembic upgrade head
```

Create a migration only after the database is at the current head:

```bash
uv run alembic revision --autogenerate -m "describe schema change"
```

## Start the API

In a second terminal:

```bash
uv run uvicorn main:app --reload
```

The API uses:

```text
MySQL: localhost:3307
Redis: localhost:6379
```

## Submit a job

Immediate execution:

```powershell
$body = @{ a = 5; b = 7 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/jobs" -ContentType "application/json" -Body $body
```

Delayed execution:

```powershell
$body = @{ a = 5; b = 7; delay_seconds = 30 } | ConvertTo-Json
$job = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/jobs" -ContentType "application/json" -Body $body
$job
```

The delayed task should remain `QUEUED` until the countdown expires. Celery may receive the scheduled message before the execution time.

## Poll the job

```powershell
Invoke-RestMethod "http://localhost:8000/jobs/$($job.job_id)"
```

Expected lifecycle:

```text
QUEUED -> PROCESSING -> COMPLETED
```

For a retryable failure:

```text
PROCESSING -> RETRY -> PROCESSING -> COMPLETED
```

After the configured maximum attempts:

```text
PROCESSING -> RETRY -> FAILED
```

## Verify the worker task is registered

```bash
docker compose exec celery-worker celery -A workers.celery_app inspect registered
```

The output should include:

```text
jobs.process_job
```

## Troubleshooting

### The task runs immediately

- Confirm the request includes `delay_seconds` greater than zero.
- Restart the API after changing `apis/jobs.py`.
- Recreate the worker with `docker compose up --build --force-recreate`.
- A `Task received` log can appear before the countdown expires. Check when the job changes to `PROCESSING`.

### MySQL connection errors

- From a Docker container, use `mysql:3306`.
- From the host, use `localhost:3307`.
- Do not use `mysql:3307` inside Docker.

### Jobs remain queued

Check the worker logs and verify that Redis and MySQL are healthy:

```bash
docker compose ps
docker compose logs --tail=100 celery-worker
```

Do not use `docker compose down -v` unless deleting the MySQL data volume is intentional.
