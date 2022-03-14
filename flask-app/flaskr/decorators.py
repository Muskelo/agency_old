from functools import wraps
from flask import g, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not g.user.is_authenticated:
            flash("Вы должны быть авторизованы для продолжения.", 'error')
            return redirect(url_for('home_view'))
        return f(*args, **kwargs)

    return wrapped

def anonym_user_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if g.user.is_authenticated:
            flash("Вы уже авторизованы.", 'error')
            return redirect(url_for('home_view'))
        return f(*args, **kwargs)

    return wrapped

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.user.has_role(role):
                flash("У вас не хватает прав для продолжения.", 'error')
                return redirect(url_for('home_view'))
            return f(*args, **kwargs)
        return wrapped
    return decorator


