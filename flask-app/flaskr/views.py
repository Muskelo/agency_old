from flask import render_template

class User():
    def __init__(self) -> None:
        self.is_authenticated = False

def add_views(app):

    @app.route("/")
    def home_view():

        return render_template("home.html", current_user=User())


