from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import uuid
from ..models.user import User
from ..services.user_service import UserService
from app import db

auth_blueprint = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return make_response('Could not verify - Missing Data', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    print(data['password'])
    #user = User.query.filter_by(email=data['email']).first()
    user = UserService.get_user_by_email(data['email'])
    print(user.password)

    if not user:
        return make_response('Could not verify - User not exist', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, data['password']):
        token = jwt.encode(
            {'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            current_app.config['SECRET_KEY']
        )
        return jsonify({'token': token, 'user': user.serialize()})

    return make_response('Could not verify - Invalid Password', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
        data = request.get_json()
        try:
            user = UserService.create_user(**data)
            return jsonify(user.serialize()), 201
        except ValueError as e:
             return {'message': str(e)}, 400

@auth_blueprint.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    return jsonify(current_user.serialize())

@auth_blueprint.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(self, user_id):
        data = request.get_json()
        user = UserService.update_user(user_id, **data)
        if user:
            return jsonify(user.serialize())
        return {'message': 'User not found'}, 404
