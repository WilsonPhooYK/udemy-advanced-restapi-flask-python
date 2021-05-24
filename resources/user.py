from typing import Any, Union
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST

from models.user import UserModel, UserModelType

BLANK_ERROR = "'{}' cannot be blank."
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created siccessfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully lodded out."

JSONResponseType = tuple[dict[str, Any], int]

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help=BLANK_ERROR.format('username'),
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help=BLANK_ERROR.format('password'),
)


class UserRegister(Resource):
    @classmethod
    def post(cls) -> JSONResponseType:
        data: dict[str, str] = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"error_message": USER_ALREADY_EXISTS}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int) -> Union[JSONResponseType, UserModelType]:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error_message": USER_NOT_FOUND}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int) -> JSONResponseType:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error_message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls) -> JSONResponseType:
        # get data from parser
        data: dict[str, str] = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data["username"])

        # This is what the authenticate() dunction used to
        if user and safe_str_cmp(user.password, data["password"]):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        print(get_jwt())
        jti = get_jwt()["jti"]  # jti is 'JWT ID', a unique identifier for a jwt
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id=user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200