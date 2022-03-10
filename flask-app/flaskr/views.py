import random

from flask import render_template, redirect, url_for, request

from flaskr.utils import generate_random_text

class User():
    def __init__(self) -> None:
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

def add_views(app):
    @app.route("/")
    def home_view():

        return render_template("home.html", current_user=User(), objects=[Object() for i in range(20)])

    @app.route("/object/<id>")
    def object_view(id):

        return render_template("object.html", current_user=User(), object=Object())

    @app.route("/object/edit/<id>")
    def edit_object_view(id):

        return render_template("object-edit.html", current_user=User(), object=Object())

    @app.route("/object/delete/<id>")
    def delete_object_view(id):

        return redirect(url_for('home_view'))

    @app.route("/object/create/")
    def create_object_view():

        return redirect(url_for('object_view', id=id))

    @app.route("/login")
    def login_view():

        return redirect(request.referrer or "home_view")

    @app.route("/register")
    def register_view():

        return redirect(request.referrer or "home_view")
