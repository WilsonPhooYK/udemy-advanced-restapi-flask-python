from ma import ma
from models.item import ItemModel
from models.store import StoreModel  # type: ignore

SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True
