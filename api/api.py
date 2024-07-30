import hashlib
from app import app, db
from flask import request, jsonify

from work_with_token import generate_token, require_token


@app.route('/api/get_token', methods=['get'])
def get_token():
    print(request.json)
    username = request.form['username']
    password = request.form['password']
    user = db.check_user(username)

    if user and user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
        token = generate_token(user['id'])
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/protected_endpoint', methods=['GET'])
@require_token
def protected_endpoint():
    return jsonify({'message': 'This is a protected API endpoint.'})