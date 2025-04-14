# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')  # 'user' or 'seller'
    if role not in ['user', 'seller']:
        return jsonify({'message': 'Invalid role'}), 400
    if User.register(db.session, username, password, email, role):
        return jsonify({'message': 'Registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.login(db.session, username, password)
    if user:
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': token, 'role': user.role}), 200
    return jsonify({'message': 'Invalid credentials'}), 401