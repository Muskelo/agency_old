from flask import flash, session, g
from passlib.hash import pbkdf2_sha256

from flaskr.models import UserModel
from flaskr.utils import save_in_db


class BaseResource():

    @classmethod
    def create(cls, data):
        object_ = cls(**data)

        save_in_db([object_])

        return object_

    @classmethod
    def get(cls, **kwargs):
        object_ = cls.query


        object_ = object_.filter_by(**kwargs).first()

        return object_

class AnonymUser(object):
    is_authenticated = False

    def has_role(self, role):
        return False


class UserResource(UserModel, BaseResource):
    is_authenticated = True

    def has_role(self, role):
        return self.role == role

    @classmethod
    def create(cls, data):
        if not data["password"] == data["password_verify"]:
            flash("Пароли не совпадают", "error")
            return

        password_hash = pbkdf2_sha256.hash(data['password'])

        if data['name'] == "admin":
            role = "admin"
        else:
            role = "user"

        user = super().create({
            "name": data['name'],
            "number": data['number'],
            "password_hash": password_hash,
            "role": role
        })

        return user

    @classmethod
    def login(cls, data):
        user = cls.query.filter(cls.number==data['number']).first()

        if not user or not pbkdf2_sha256.verify(data['password'], user.password_hash):
            flash("Неверный логин или пароль", "error")
            return

        session["current_user.id"] = user.id

    @classmethod
    def logout(cls):
        session.pop("current_user.id")

    @classmethod
    def load_user(cls):
        if 'current_user.id' in session:
            g.user = cls.get(id=session['current_user.id'])
        else:
            g.user = AnonymUser()

