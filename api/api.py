import hashlib
from flask import Blueprint, request, jsonify
from extensions import db
from .work_with_token import generate_token, require_token

api_bp = Blueprint('api', __name__)

@api_bp.route('/get_token', methods=['POST'])
def get_token():
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.check_user(username)

    if user and user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
        token = generate_token(user['id'])
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/protected_endpoint', methods=['GET'])
@require_token
def protected_endpoint():
    return jsonify({'message': 'This is a protected API endpoint.'})
