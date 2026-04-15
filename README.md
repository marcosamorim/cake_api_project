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
