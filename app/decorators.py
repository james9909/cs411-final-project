import traceback
from functools import wraps

from flask import make_response, jsonify, session, redirect, url_for

def api_view(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if not isinstance(result, dict):
                return result
        except Exception:
            result = {"message": "Something went wrong!"}
            traceback.print_exc()
        status = result.pop("status", 200)
        return make_response(jsonify(result), status)
    return wrapper

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "uid" not in session:
            return redirect(url_for("views.index"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not session["is_admin"]:
            return redirect(url_for("views.index"))
        return f(*args, **kwargs)
    return wrapper
