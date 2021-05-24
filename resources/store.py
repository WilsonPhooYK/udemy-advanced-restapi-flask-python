from typing import Union
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.store import StoreModel, StoreModelType

JSONResponseType = tuple[dict[str, str], int]

NAME_ALREADY_EXISTS = "An store with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."

class Store(Resource):
    # Authorization - JWT {token}
    @classmethod
    @jwt_required()
    def get(cls, name: str) -> Union[StoreModelType, JSONResponseType]:
        print('CRASH')
        # Returns the current user row
        item = StoreModel.find_by_name(name)
        if item:
            return item.json()

        return {"error_message": STORE_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str) -> Union[tuple[StoreModelType, int], JSONResponseType]:
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {
                "error_message": ERROR_INSERTING
            }, 500  # Internal Server Error

        return store.json(), 201

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
        return [store.json() for store in StoreModel.find_all()], 200
