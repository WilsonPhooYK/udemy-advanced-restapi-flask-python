# from marshmallow import Schema, fields
from ma import ma
from models.user import UserModel

SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema

class UserSchema(SQLAlchemyAutoSchema):
    class Meta: # type: ignore
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True

    # id = fields.Int()
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)