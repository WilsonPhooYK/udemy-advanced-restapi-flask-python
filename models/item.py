from dataclasses import dataclass
from db import db
from typing import TypedDict, Optional

ItemModelType = TypedDict(
    "ItemModelType",
    {
        "name": str,
        "price": float,
        "store_id": int,
        "id": int,
    },
)

Model = db.Model


@dataclass
class ItemModel(Model):
    __tablename__ = "items"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(80), nullable=False, unique=True)
    price: float = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    # Matches store_id to Store
    store = db.relationship("StoreModel")

    @classmethod
    def find_by_name(cls, name: str) -> Optional["ItemModel"]:
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "ItemModel":
        # SELECT * FROM items WHERE id=_id LIMIT 1
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> list["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
