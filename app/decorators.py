import traceback
from functools import wraps

from flask import make_response, jsonify

def api_view(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except Exception:
            result = {"message": "Something went wrong!"}
            traceback.print_exc()
        return make_response(jsonify(result))
    return wrapper
