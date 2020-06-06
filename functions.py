from functools import wraps
from flask import session, redirect, render_template


""" Module with various utilities """
# Decorate routes to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def msg(template, message, mode):
    return render_template(template, msg=message, md=mode)


