import unittest

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.models import CakeCreate
from app.routes import add_cake, delete_cake, list_cakes


class CakeRoutesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()

    def test_list_cakes_starts_empty(self) -> None:
        self.assertEqual(list_cakes(db=self.session), [])

    def test_add_cake_and_list(self) -> None:
        payload = CakeCreate(
            id=1,
            name="Chocolate Cake",
            comment="Rich and moist",
            imageUrl="https://example.com/chocolate.jpg",
            yumFactor=5,
        )

        created = add_cake(payload=payload, db=self.session)
        self.assertEqual(created.id, 1)

        cakes = list_cakes(db=self.session)
        self.assertEqual(len(cakes), 1)
        self.assertEqual(cakes[0].name, "Chocolate Cake")

    def test_add_duplicate_id_returns_conflict(self) -> None:
        payload = CakeCreate(
            id=1,
            name="Chocolate Cake",
            comment="Rich and moist",
            imageUrl="https://example.com/chocolate.jpg",
            yumFactor=5,
        )
        add_cake(payload=payload, db=self.session)

        with self.assertRaises(HTTPException) as ctx:
            add_cake(payload=payload, db=self.session)

        self.assertEqual(ctx.exception.status_code, 409)

    def test_delete_existing_cake_returns_204(self) -> None:
        payload = CakeCreate(
            id=1,
            name="Chocolate Cake",
            comment="Rich and moist",
            imageUrl="https://example.com/chocolate.jpg",
            yumFactor=5,
        )
        add_cake(payload=payload, db=self.session)

        response = delete_cake(cake_id=1, db=self.session)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(list_cakes(db=self.session), [])

    def test_delete_missing_cake_returns_404(self) -> None:
        with self.assertRaises(HTTPException) as ctx:
            delete_cake(cake_id=999, db=self.session)

        self.assertEqual(ctx.exception.status_code, 404)

    def test_validation_rules(self) -> None:
        with self.assertRaises(ValidationError):
            CakeCreate(
                id=1,
                name="x" * 31,
                comment="ok",
                imageUrl="https://example.com/cake.jpg",
                yumFactor=5,
            )

        with self.assertRaises(ValidationError):
            CakeCreate(
                id=1,
                name="Valid",
                comment="x" * 201,
                imageUrl="https://example.com/cake.jpg",
                yumFactor=5,
            )

        with self.assertRaises(ValidationError):
            CakeCreate(
                id=1,
                name="Valid",
                comment="ok",
                imageUrl="https://example.com/cake.jpg",
                yumFactor=6,
            )


if __name__ == "__main__":
    unittest.main()
