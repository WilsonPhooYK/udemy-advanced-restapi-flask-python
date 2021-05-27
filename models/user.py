from flask import request, url_for
from dataclasses import dataclass
from typing import TypedDict
from requests import Response
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel
from db import db

Model = db.Model

FROM_TITLE = "Stores REST API"
FROM_EMAIL = "postmaster@sandbox8db07137bf6d4f179cc5885b8f5c8778.mailgun.org"

UserModelType = TypedDict(
    "UserModelType",
    {
        "id": int,
        "username": str,
        "password": str,
        "email": str,
    },
)


@dataclass
class UserModel(Model):
    __tablename__ = "users"
    # Must have id to authenticate
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), nullable=False, unique=True)
    password: str = db.Column(db.String(80), nullable=False)
    email: str = db.Column(db.String(80), nullable=False, unique=True)

    confirmation = db.relationship(
        # all, delete-orphan - Delete all confirmation related to use
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )
    
    # lazy dynamic
    # user = UserModel(...)
    # confirmation = ConfirmationModel(...)
    # confirmation.save_to_db()
    # print(user.confirmation)

    # def __init__(self, username: str, password: str) -> None:
    #     # Must have id to authenticate
    #     self.username = username
    #     self.password = password
    
    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expired_at)).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        # SELECT * FROM items WHERE username=username LIMIT 1
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        # SELECT * FROM items WHERE email=email LIMIT 1
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        # SELECT * FROM items WHERE id=_id LIMIT 1
        return cls.query.filter_by(id=_id).first()
    
    def send_confirmation_email(self) -> Response:
        # http://127.0.0.1:5000/user_confirm/1
        # confirmation - match lowercase of the resource
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)
        subject = "Registration confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'
        
        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
