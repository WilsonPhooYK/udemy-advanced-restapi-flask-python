from ma import ma
from models.order import OrderModel, ItemsInOrder
from schemas.item import ItemSchema
from marshmallow import fields as mFields
from marshmallow_sqlalchemy import fields

SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema

class ItemsInOrderSchema(SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = ItemsInOrder
        load_only = ("order", "id")
        load_instance = True
        include_relationships = True
        
    item = fields.Nested(ItemSchema)
    item_id = mFields.Integer(attribute="item_id")

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = OrderModel
        load_only = ("token",)
        dump_only = ("id", "status",)
        load_instance = True
        include_relationships = True
        exclude = ["id"]
        
    items = fields.Nested(ItemsInOrderSchema, many=True)
    order_id = mFields.Integer(attribute="id")
