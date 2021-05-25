from typing import Any, Union
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from schemas.store import StoreSchema

from models.store import StoreModel, StoreModelType

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

JSONResponseType = tuple[dict[str, str], int]

NAME_ALREADY_EXISTS = "An store with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."

class Store(Resource):
    # Authorization - JWT {token}
    @classmethod
    @jwt_required()
    def get(cls, name: str) -> Union[Any, JSONResponseType]:
        # Returns the current user row
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200

        return {"error_message": STORE_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str) -> Union[tuple[Any, int], JSONResponseType]:
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except:
            return {
                "error_message": ERROR_INSERTING
            }, 500  # Internal Server Error

        return store_schema.dump(store), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str) -> JSONResponseType:
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message": STORE_NOT_FOUND}, 400

        store.delete_from_db()

        return {"message": STORE_DELETED}, 200


class StoreList(Resource):
    @classmethod
    def get(cls) -> tuple[list[StoreModelType], int]:
        return store_list_schema.dump(StoreModel.find_all()), 200
