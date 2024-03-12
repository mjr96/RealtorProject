from functools import wraps
from flask import g, request, redirect, url_for

#Function created to make sure the user remains logged in the system.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function