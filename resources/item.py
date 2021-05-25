from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from typing import Any, Union
from models.item import ItemModel

from schemas.item import ItemSchema

NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ADMIN_REQUIRED = "Admin privilege required."
MORE_DATA_AVAILABLE = "More data available if you login"

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

JSONResponseType = tuple[dict[str, str], int]
# JWT - JSON Web Token

# 400 - bad request
# 404 - item not found
# 201 - create success
# 202 - accepted, but will create success only after a long time
class Item(Resource):
    # Authorization - JWT {token}
    @classmethod
    def get(cls, name: str) -> Union[Any, JSONResponseType]:
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)

        return {"error_message": ITEM_NOT_FOUND}, 404

    # except StopIteration:
    # return {"error_message": "Item not found"}, 404
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str) -> Union[tuple[Any, int], JSONResponseType]:
        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        # Only parse for price
        item_json = request.get_json()
        item_json["name"] = name

        item: ItemModel = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {
                "error_message": ERROR_INSERTING
            }, 500  # Internal Server Error

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str) -> JSONResponseType:
        # Get claims from jwt
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"message": ADMIN_REQUIRED}, 401

        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": ITEM_NOT_FOUND}, 400

        item.delete_from_db()

        return {"message": ITEM_DELETED}, 200

    @classmethod
    def put(cls, name: str) -> Union[tuple[Any, int], JSONResponseType]:
        item_json = request.get_json()
        item: Union[ItemModel, None] = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name
            item: Union[ItemModel, None] = item_schema.load(item_json)

        if item:
            item.save_to_db()

            return item_schema.dump(item), 200
        
        return {"message": ITEM_NOT_FOUND}, 400


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls) -> tuple[Any, int]:
        user_id = get_jwt_identity()
        items = item_list_schema.dump(ItemModel.find_all())

        if user_id:
            return items, 200

        return {
            "items": [item["name"] for item in items],
            "messsage": MORE_DATA_AVAILABLE,
        }, 200
        # return list(map(lambda item: item.json(), ItemModel.query.all())), 200
        # return [item.json() for item in ItemModel.find_all()], 200
