import random

from flask import render_template, redirect, url_for, request, flash
from sqlalchemy.exc import IntegrityError

from flaskr.utils import generate_random_text
from flaskr.resources import ObjectResource, RequestResource, UserResource
from flaskr.decorators import anonym_user_required, login_required, role_required

class User():
    def __init__(self) -> None:
        self.id = random.randint(1, 1000)
        self.name = generate_random_text(1, 3)
        self.number = random.randint(10**11, 10**12-1)
        self.is_authenticated = False
        self.role = "admin"

    def has_role(self, role):
        return self.role == role


class Object():
    def __init__(self) -> None:
        self.id = random.randint(1, 1000)
        self.title = generate_random_text(max_len=6)
        self.description = generate_random_text()
        self.image_name = "image.webp"


class Request():
    def __init__(self) -> None:
        self.id = random.randint(1, 1000)
        self.status = bool(random.randint(0, 1))
        self.user = User()
        self.object = Object()


def add_object_views(app):
    @app.route("/object/<id>")
    def object_view(id):
        object_ = ObjectResource.get_(id=id)

        return render_template("object.html", object=object_)

    @app.route("/object/edit/<id>", methods=['GET', 'POST'])
    @role_required('admin')
    def edit_object_view(id):
        if request.method == "POST":

            ObjectResource.update_(
                id, request.form, request.files.get('image'))

            return redirect(url_for("object_view", id=id))

        object_ = ObjectResource.get_(id=id)

        return render_template("object-edit.html",  object=object_)

    @app.route("/object/delete/<id>")
    @role_required('admin')
    def delete_object_view(id):
        ObjectResource.delete_(id)

        return redirect(url_for('home_view'))

    @app.route("/object/create/", methods=['POST'])
    @role_required('admin')
    def create_object_view():
        object_ = ObjectResource.create_(request.form, request.files['image'])

        return redirect(url_for('object_view', id=object_.id))

def add_auth_views(app):
    @app.route("/login", methods=["POST"])
    @anonym_user_required
    def login_view():
        UserResource.login(request.form)

        return redirect(request.referrer or "home_view")

    @app.route("/logout")
    @login_required
    def logout_view():
        UserResource.logout()

        return redirect(url_for("home_view"))

    @app.route("/register", methods=["POST"])
    @anonym_user_required
    def register_view():
        try:
            user = UserResource.create_(request.form)
        except IntegrityError as e:
            flash("Не удалось совершить регистрацию,\
                    возможно такой номер телефона уже занят.", "error")

        return redirect(request.referrer or "home_view")

    @app.route("/users/delete/<id>")
    @role_required('admin')
    def delete_user_view(id):
        UserResource.delete_(id)

        return redirect(request.referrer)

    @app.route("/users/edit/<id>", methods=['POST'])
    @role_required('admin')
    def edit_user_view(id):
        UserResource.update_(id, request.form)

        return redirect(request.referrer)



def add_request_views(app):
    @app.route("/request/create/")
    @login_required
    def create_request_view():
        data = {
            'user_id': request.args['user_id'],
            'object_id': request.args['object_id']
        }
        try:
            RequestResource.create_(data)
        except IntegrityError as e:
            flash("Не удалось подать заявку,\
                    вероятно вы уже подавали ее.", "error")
        return redirect(request.referrer)

    @app.route("/request/delete/<id>")
    @role_required('admin')
    def delete_request_view(id):
        RequestResource.delete_(id)

        return redirect(request.referrer)

def add_views(app):
    @app.route("/")
    def home_view():
        return render_template("home.html", objects=ObjectResource.get_all_())

    @app.route("/admin/")
    @role_required('admin')
    def admin_view():
        return render_template("admin.html", requests=RequestResource.get_all_(), users=UserResource.get_all_())

    add_object_views(app)
    add_auth_views(app)
    add_request_views(app)
