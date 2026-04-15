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
- Health endpoint: `http://127.0.0.1:8000/health`

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
- Health check endpoint exposed:
  - `GET /health`
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

- Cloud deployment example (AWS ECS Fargate):
  - Build/push image to ECR.
  - Run service behind an Application Load Balancer.
  - Move persistence to managed PostgreSQL (RDS).
  - Pass config via environment variables/secrets manager.
- Scaling:
  - Run multiple API replicas behind load balancer.
  - Use CPU/memory autoscaling policies.
  - Keep API stateless and externalize DB.
- Resilience / failure modes:
  - Use `GET /health` for liveness/readiness checks.
  - Enable container restarts and rolling deployments.
  - Add DB backup/restore strategy.
  - Set timeouts and retry strategy at load balancer level.
- Future product/API evolution:
  - Migrate to PostgreSQL + Alembic migrations.
  - Add authentication/authorization.
  - Add pagination/filtering/sorting on `GET /cakes`.
  - Add API versioning strategy for backward compatibility.
