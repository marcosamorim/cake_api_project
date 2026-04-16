from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db import get_db
from app.models import Cake, CakeCreate, CakeResponse, ErrorResponse

router = APIRouter(tags=["cakes"])


@router.get(
    "/cakes",
    response_model=list[CakeResponse],
    summary="List all cakes",
    description="Returns all cakes ordered by `id` in ascending order.",
    responses={
        200: {"description": "Cakes returned successfully."},
        422: {"description": "Invalid request parameters."},
    },
)
def list_cakes(db: Session = Depends(get_db)) -> list[Cake]:
    return db.exec(select(Cake).order_by(Cake.id)).all()


@router.post(
    "/cakes",
    response_model=CakeResponse,
    status_code=201,
    summary="Create a cake",
    description="Creates a new cake. If `id` already exists, returns `409`.",
    responses={
        201: {"description": "Cake created successfully."},
        409: {"description": "Cake with the same id already exists.", "model": ErrorResponse},
        422: {"description": "Validation error in request body."},
    },
)
def add_cake(payload: CakeCreate, db: Session = Depends(get_db)) -> Cake:
    if db.get(Cake, payload.id):
        raise HTTPException(status_code=409, detail="Cake with this id already exists")

    cake = Cake.model_validate(payload)
    db.add(cake)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        message = str(exc).lower()
        if "unique" in message or "primary key" in message:
            raise HTTPException(
                status_code=409, detail="Cake with this id already exists"
            ) from exc
        raise HTTPException(status_code=400, detail="Invalid cake data") from exc

    db.refresh(cake)
    return cake


@router.delete(
    "/cakes/{cake_id}",
    status_code=204,
    summary="Delete a cake",
    description="Deletes a cake by id. Returns `404` when the cake is not found.",
    responses={
        204: {"description": "Cake deleted successfully."},
        404: {"description": "Cake not found.", "model": ErrorResponse},
        422: {"description": "Invalid cake id."},
    },
)
def delete_cake(cake_id: int, db: Session = Depends(get_db)) -> Response:
    cake = db.get(Cake, cake_id)
    if cake is None:
        raise HTTPException(status_code=404, detail="Cake not found")

    db.delete(cake)
    db.commit()
    return Response(status_code=204)
