import random

from flask import render_template, redirect, url_for, request

from flaskr.utils import generate_random_text

class User():
    def __init__(self) -> None:
        self.id = random.randint(1, 1000)
        self.name = generate_random_text(1,3)
        self.number = random.randint(10**11,10**12-1)
        self.is_authenticated = True
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

        return render_template("object.html", current_user=User(), object=Object())

    @app.route("/object/edit/<id>", methods=['GET', 'POST'])
    def edit_object_view(id):

        if request.method == "POST":
            return redirect(url_for("object_view", id=id))

        return render_template("object-edit.html", current_user=User(), object=Object())

    @app.route("/object/delete/<id>")
    def delete_object_view(id):

        return redirect(url_for('home_view'))

    @app.route("/object/create/")
    def create_object_view():

        return redirect(url_for('object_view', id=id))

def add_auth_views(app):

    @app.route("/login")
    def login_view():

        return redirect(request.referrer or "home_view")

    @app.route("/logout")
    def logout_view():

        return redirect(url_for("home_view"))

    @app.route("/register")
    def register_view():

        return redirect(request.referrer or "home_view")

def add_request_views(app):

    @app.route("/request/create/")
    def create_request_view():

        return redirect(request.referrer)

    @app.route("/request/delete/<id>")
    def delete_request_view(id):

        return redirect(request.referrer)

def add_views(app):

    @app.route("/")
    def home_view():

        return render_template("home.html", current_user=User(), objects=[Object() for i in range(20)])

    @app.route("/admin/")
    def admin_view():

        return render_template("admin.html", current_user=User(), requests=[Request() for x in range(10)])

    add_object_views(app)

    add_auth_views(app)

    add_request_views(app)
