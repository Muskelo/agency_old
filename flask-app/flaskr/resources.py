import os
import re
from flask import flash, session, g, current_app
from passlib.hash import pbkdf2_sha256

from flaskr.models import ObjectModel, UserModel, RequestModels
from flaskr.utils import save_in_db


class BaseResource():
    @classmethod
    def create_(cls, data):
        object_ = cls(**data)

        save_in_db([object_])

        return object_

    @classmethod
    def get_(cls, **kwargs):
        object_ = cls.query

        object_ = object_.filter_by(**kwargs).first()

        return object_

    @classmethod
    def get_all_(cls, **kwargs):
        object_ = cls.query

        object_ = object_.filter_by(**kwargs).all()

        return object_


    @classmethod
    def update_(cls, id, data):
        object_ = cls.query.filter_by(id=id)

        # clean empty data from dict
        data = {k:v for k, v in data.items() if v}

        if not data:
            return object_

        object_.update(data)

        save_in_db()

        return object_

    @classmethod 
    def delete_(cls, id):
        object_ = cls.query.filter_by(id=id)

        object_.delete()

        save_in_db()

class AnonymUser(object):
    is_authenticated = False

    def has_role(self, role):
        return False

class UserResource(UserModel, BaseResource):
    is_authenticated = True

    def has_role(self, role):
        return self.role == role

    @classmethod
    def create_(cls, data):
        if not data["password"] == data["password_verify"]:
            flash("Пароли не совпадают", "error")
            return

        password_hash = pbkdf2_sha256.hash(data['password'])

        if data['name'] == "admin":
            role = "admin"
        else:
            role = "user"

        user = super().create_({
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

        session["user_id"] = user.id

    @classmethod
    def logout(cls):
        session.pop("user_id")

    @classmethod
    def load_user(cls):
        if 'user_id' in session:
            g.user = cls.get_(id=session['user_id'])
        else:
            g.user = AnonymUser()

class ObjectResource(ObjectModel, BaseResource):
    @classmethod
    def save_image(cls, image, object_id):
        if image.filename == '':
            flash('No selected file')
            return 
        if image:
            new_imagename = f"obj_{object_id}__{image.filename}"
            image.save(os.path.join(current_app.config["IMAGE_PATH"], new_imagename))

        cls.update_(object_id, {"image_name":new_imagename})
       
    @classmethod
    def delete_image(cls, object_id):
        object_ = cls.get_(id=object_id)
        try:
            os.remove(os.path.join(current_app.config["IMAGE_PATH"], object_.image_name))
        except:
            flash("Не удалось удалить изображение", "error")

    @classmethod
    def create_(cls, data, image):
        
        object_ = super().create_(data)

        cls.save_image(image, object_.id)

        return object_

    @classmethod
    def delete_(cls, id):

        cls.delete_image(id)    

        super().delete_(id)

    @classmethod
    def update_(cls, id, data, image=None):

        if image:
            cls.delete_image(id)
            cls.save_image(image, id)

        if data:
            super().update_(id, data)

class RequestResource(RequestModels, BaseResource):
    pass

