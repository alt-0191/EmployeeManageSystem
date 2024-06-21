from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from backend.models import User, db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        response = make_response(jsonify({
            'message': '登录成功',
            'is_admin': user.is_admin,
            'access_token': access_token
        }), 200)
        return response
    else:
        return jsonify({'message': '用户名或密码错误'}), 401


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # 接收 JSON 数据
    if not data:
        return jsonify({'message': '请求必须包含JSON数据'}), 400

    # 从请求中获取用户名和密码
    username = data.get('username')
    password = data.get('password')

    # 检查用户名和密码是否存在且不为空
    if not username or not password:
        return jsonify({'message': '用户名和密码是必填字段，并且不能为空'}), 400

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': '用户名已存在，请选择其他用户名'}), 400

    # 创建新用户，使用密码散列增加安全性
    hashed_password = generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '用户注册成功'}), 201


@auth.route('/check-auth', methods=['GET'])
@jwt_required()
def check_auth():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'isLoggedIn': True}), 200
    return jsonify({'isLoggedIn': False}), 401


@auth.route('/check-admin', methods=['GET'])
@jwt_required()
def check_admin():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if user and user.is_admin:
        return jsonify({'isAdmin': True}), 200
    return jsonify({'isAdmin': False}), 401
