# Cake API

## Requirements

- Docker

## Run With Docker Compose

```bash
docker compose up --build
```

API:

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- Cakes endpoint: `http://127.0.0.1:8000/cakes`

`--build` is optional. Use it on first run or after Dockerfile/dependency changes.

SQLite data is persisted in `./db/cakes.db`.

Optional: run with plain Docker instead of compose:

```bash
docker build -t cake-api .
docker run --rm -p 8000:8000 \
  -v "$(pwd)/db:/db" \
  cake-api
```

## Run Tests With Docker Compose

```bash
docker compose -f docker-compose.test.yml up --build
```

`--build` is optional. Use it on first run or after Dockerfile/dependency changes.

## Criteria Checklist

- OpenAPI/Swagger exposed:
  - `GET /openapi.json`
  - `GET /docs`
- Cakes can be listed: `GET /cakes`
- Cakes can be added: `POST /cakes`
- Cakes can be deleted: `DELETE /cakes/{id}`
- Validation implemented:
  - `name` max 30 chars
  - `comment` max 200 chars
  - `yumFactor` between 1 and 5
- Docker runnable from a fresh clone:
  - `docker compose up --build`

## Future Extensions (Plus)

- PostgreSQL migration path:
  - Set `CAKE_DB_URL` to a Postgres URL.
  - Add Alembic migrations for schema evolution.
- Kubernetes:
  - Add `Deployment` + `Service` manifests.
  - Mount persistent volume for DB (or external managed DB).
- Resilience/scale:
  - Health probes (`/` or dedicated health endpoint).
  - Multiple API replicas behind a load balancer.
