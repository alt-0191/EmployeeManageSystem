from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import db, User

modUsers = Blueprint('user', __name__)


@modUsers.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize())


@modUsers.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, is_admin=is_admin)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@modUsers.route('/api/delUsers/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    password = data.get('password')
    is_admin = data.get('is_admin')

    if password:
        user.set_password(password)

    if is_admin is not None:
        user.is_admin = is_admin

    db.session.commit()

    return jsonify({'message': 'User updated successfully'})


@modUsers.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
