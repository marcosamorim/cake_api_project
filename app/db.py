import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = os.getenv("CAKE_DB_URL", "sqlite:///./cakes.db")
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args)


def init_db() -> None:
    import app.models  # Ensure models are imported so SQLModel metadata is populated before create_all().

    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
