from ma import ma
from models.store import StoreModel
from models.item import ItemModel  # type: ignore
from schemas.item import ItemSchema


SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema


class StoreSchema(SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:  # type: ignore
        model = StoreModel
        dump_only = ("id",)
        load_instance = True
        include_fk = True
