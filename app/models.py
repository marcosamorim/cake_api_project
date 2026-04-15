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


class CakeResponse(CakeBase):
    id: int


class ErrorResponse(SQLModel):
    detail: str
