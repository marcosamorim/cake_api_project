# Cake API (FastAPI + SQLModel)

Simple API for listing, creating, and deleting cakes.

## Requirements

- Python 3.12+
- `uv` (optional) or a regular virtual environment

## Run Locally

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000`.

## Run With Docker

Build image:

```bash
docker build -t cake-api .
```

Run container:

```bash
docker run --rm -p 8000:8000 cake-api
```

Optional: persist SQLite data between runs:

```bash
mkdir -p .docker-data
docker run --rm -p 8000:8000 \
  -e CAKE_DB_URL=sqlite:////data/cakes.db \
  -v "$(pwd)/.docker-data:/data" \
  cake-api
```

## API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Endpoints

- `GET /cakes` list all cakes
- `POST /cakes` create one cake
- `DELETE /cakes/{id}` delete one cake

### Example Create Request

```bash
curl -X POST "http://127.0.0.1:8000/cakes" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Chocolate Cake",
    "comment": "Rich and moist",
    "imageUrl": "https://example.com/chocolate-cake.jpg",
    "yumFactor": 5
  }'
```
