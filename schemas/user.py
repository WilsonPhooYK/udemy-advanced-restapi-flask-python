# from marshmallow import Schema, fields
from typing import Any
from marshmallow import pre_dump
from ma import ma
from models.user import UserModel

SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        include_relationships = True
        load_instance = True

    # id = fields.Int()
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)
    
    @pre_dump
    def _pre_dump(self, user: UserModel, **kwargs: Any):
        user.confirmation = [user.most_recent_confirmation]
        return user
