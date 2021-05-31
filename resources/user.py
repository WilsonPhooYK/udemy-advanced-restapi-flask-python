from libs.mailgun import MailGunException
import traceback
from typing import Any, Union
from flask import request # , make_response, render_template, redirect
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_restful import Resource
from blacklist import BLACKLIST

from libs.strings import gettext
from schemas.user import UserSchema
from models.user import UserModel, UserModelType
from models.confirmation import ConfirmationModel

JSONResponseType = tuple[Union[dict[str, Any], Any], int]

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls) -> JSONResponseType:
        user: UserModel = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"error_message": gettext("user_username_exists")}, 400
        
        if UserModel.find_by_email(user.email):
            return {"error_message": gettext("user_email_exists")}, 400

        try:
            # user = UserModel(**user_data)
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": gettext("user_registered")}, 201
        except MailGunException as e:
            user.delete_from_db()
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500

        


class User(Resource):
    @classmethod
    def get(cls, user_id: int) -> Union[JSONResponseType, UserModelType]:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error_message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int) -> JSONResponseType:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error_message": gettext("user_not_found")}, 404
        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls) -> JSONResponseType:
        user_data: UserModel = user_schema.load(request.get_json(), partial=("email", ))

        # find user in database
        user = UserModel.find_by_username(user_data.username)

        # This is what the authenticate() dunction used to
        if user and user_data.password and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                # create access token
                access_token = create_access_token(identity=user.id, fresh=True)
                # create refresh token
                refresh_token = create_refresh_token(user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200

            return {"message": gettext("user_not_confirmed").format(user.email)}, 400

        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        print(get_jwt())
        jti = get_jwt()["jti"]  # jti is 'JWT ID', a unique identifier for a jwt
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id=user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

class SetPassword(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        user_json = request.get_json()
        user_data: UserModel = user_schema.load(user_json) # username and new password
        user = UserModel.find_by_username(user_data.username)
        if not user:
            return {"error_message": gettext("user_not_found")}, 404
        
        user.password = user_data.password
        user.save_to_db()
        
        return {"message": gettext("user_password_updated")}, 201
        
# class UserConfirm(Resource):
#     @classmethod
#     def get(cls, user_id: int):
#         # find user in database
#         user = UserModel.find_by_id(user_id)

#         if not user:
#             return {"message": USER_NOT_FOUND}, 404

#         user.activated = True
#         user.save_to_db()
        
#         # return redirect('http://www.google.com', 302)
        
#         headers = {"Content-Type": "text/html"}
#         # folder must be same location as app.py and must be templates
#         return make_response(render_template("confirmation_page.html", email=user.username), 200, headers)
