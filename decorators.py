from functools import wraps
from flask import session,render_template,flash,request
from flask.helpers import url_for
from werkzeug.utils import redirect

def get_roles(roles):
    for i in session["role"]:
        for j in roles:
            if i in j:
                return True
            else:
                valid_role= False
    return valid_role

def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_roles(roles)==False:          
                user_role=",".join([str(i) for i in session["role"]])
                flash(f"You don't have the access to use this option , as your role are {user_role}   and required role are {roles}")
                return redirect(url_for("student.student_list"))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session and session["user"] is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function