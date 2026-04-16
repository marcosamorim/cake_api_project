from sqlmodel import Field, SQLModel


class CakeBase(SQLModel):
    name: str = Field(max_length=30)
    comment: str = Field(max_length=200)
    imageUrl: str
    yumFactor: int = Field(ge=1, le=5)


class Cake(CakeBase, table=True):
    __tablename__ = "cakes"
    id: int = Field(primary_key=True, index=True)


class CakeCreate(CakeBase):
    id: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Chocolate Cake",
                "comment": "Rich and moist",
                "imageUrl": "https://example.com/chocolate-cake.jpg",
                "yumFactor": 5,
            }
        }
    }


class CakeResponse(CakeBase):
    id: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Chocolate Cake",
                "comment": "Rich and moist",
                "imageUrl": "https://example.com/chocolate-cake.jpg",
                "yumFactor": 5,
            }
        }
    }


class ErrorResponse(SQLModel):
    detail: str
    model_config = {
        "json_schema_extra": {"example": {"detail": "Cake with this id already exists"}}
    }
