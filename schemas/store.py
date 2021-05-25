from ma import ma
from models.store import StoreModel # type: ignore
from models.item import ItemModel 
from schemas.item import ItemSchema


SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema

class StoreSchema(SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)
    class Meta: # type: ignore
        model = ItemModel
        dump_only = ("id",)
        load_instance = True
        include_fk = True
