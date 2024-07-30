import uuid
from functools import wraps
from flask import request, jsonify
from app import db


def generate_token(user_id):
    token = uuid.uuid4().hex
    db.set_api_token(user_id, token)
    return token

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 403

        user = db.get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated
