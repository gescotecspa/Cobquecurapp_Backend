from flask import Blueprint, request, jsonify, make_response, current_app,render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import uuid
from ..models.user import User
from ..services.user_service import UserService
from app import db
import random
import string
from ..common.email_utils import send_email

auth_blueprint = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            print(request.headers['Authorization'].split())
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            current_user = User.query.filter_by(email=data['email']).first()
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


# Reestablecer contraseña

def generate_reset_code(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

@auth_blueprint.route('/reset_password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')

    user = UserService.get_user_by_email(email)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    reset_code = generate_reset_code()
    user.reset_code = reset_code
    user.reset_code_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    db.session.commit()

    # URL donde se restablecerá la contraseña
    reset_url = "https://app-turismo-cl-web.vercel.app/reset_password"

    subject = "Password Reset Requested"
    recipients = [email]
    html_body = render_template('email/reset_password.html', reset_code=reset_code, reset_url=reset_url)

    send_email(subject, recipients, html_body)

    return jsonify({'message': 'Password reset email sent'}), 200

@auth_blueprint.route('/reset_password/new_password', methods=['PUT'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('password')

    user = UserService.get_user_by_email(email)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.reset_code != code or user.reset_code_expiration < datetime.datetime.utcnow():
        return jsonify({'message': 'Invalid or expired reset code'}), 400

    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    user.reset_code = None
    user.reset_code_expiration = None
    db.session.commit()

    return jsonify({'message': 'Password has been reset'}), 200
