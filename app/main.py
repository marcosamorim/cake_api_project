from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routes import router as cake_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Cake API",
    version="1.0.0",
    description=(
        "Simple Cake CRUD API. "
        "Use `GET /cakes` to list cakes, `POST /cakes` to create a cake, "
        "and `DELETE /cakes/{cake_id}` to remove a cake."
    ),
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Cake API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(cake_router)
