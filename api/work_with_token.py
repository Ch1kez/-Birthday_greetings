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

        with db.__database_connection as cursor:
            result = cursor.execute('SELECT * FROM api_tokens WHERE token = ?', (token,)).fetchone()
            if not result:
                return jsonify({'error': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated
