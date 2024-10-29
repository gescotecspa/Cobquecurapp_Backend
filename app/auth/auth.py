from flask import Blueprint, request, jsonify, make_response, current_app, render_template
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

    # Verificar si se envían los datos requeridos
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400

    # Obtener el usuario por email
    user = UserService.get_user_by_email(data['email'])
    
    # Si el usuario no existe
    if not user:
        return jsonify({'message': 'No existe el usuario'}), 404

    # Verificar la contraseña
    if check_password_hash(user.password, data['password']):
        # Generar el token JWT
        token = jwt.encode(
            {'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            current_app.config['SECRET_KEY']
        )
        # Devolver el token y los datos del usuario
        return jsonify({'token': token, 'user': user.serialize()}), 200

    # Si la contraseña es incorrecta
    return jsonify({'message': 'Password inválido'}), 401

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Extraer datos de la imagen si existen
    image_data = data.pop('image_data', None)
    
    try:
        user = UserService.create_user(**data, image_data=image_data)
        return jsonify(user.serialize()), 201
    except ValueError as e:
        return {'message': str(e)}, 400

@auth_blueprint.route('/signup-partner', methods=['POST'])
def signup_partner():
    data = request.get_json()
    
    # Extraer datos de la imagen si existen
    image_data = data.pop('image_data', None)
    
    try:
        user = UserService.create_user_partner(**data)
        return jsonify(user.serialize()), 201
    except ValueError as e:
        return {'message': str(e)}, 400

@auth_blueprint.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    return jsonify(current_user.serialize())

@auth_blueprint.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    data = request.get_json()
    
    # Extraer datos de la imagen si existen
    image_data = data.pop('image_data', None)
    
    user = UserService.update_user(user_id, **data, image_data=image_data)
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
    # print("usuario",user)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    reset_code = generate_reset_code()
    user.reset_code = reset_code
    user.reset_code_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    db.session.commit()

    # URL donde se restablecerá la contraseña app-cobquecura.vercel.app
    reset_url = "https://cobquecura.vercel.app/reset_password"

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

@auth_blueprint.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = UserService.get_all_users()
    return jsonify([user.serialize() for user in users])

@auth_blueprint.route('/signup/bulk', methods=['POST'])
@token_required
def create_bulk_users(current_user):
    data = request.get_json()

    if not isinstance(data, list):
        return {'message': 'Invalid data format. Expected a list of users.'}, 400

    created_users = []
    errors = []

    for user_data in data:
        image_data = user_data.pop('image_data', None)
        try:
            user = UserService.create_user(**user_data, image_data=image_data)
            created_users.append(user.serialize())
        except ValueError as e:
            errors.append({'user_data': user_data, 'error': str(e)})

    if errors:
        return jsonify({'created_users': created_users, 'errors': errors}), 207
    return jsonify({'created_users': created_users}), 201

@auth_blueprint.route('/signup-partners/bulk', methods=['POST'])
def signup_partners():
    data = request.get_json()

    if not isinstance(data, list):
        return {'message': 'Invalid data format. Expected a list of partners.'}, 400

    created_users = []
    errors = []

    for partner_data in data:
        try:
            user = UserService.create_user_partner(**partner_data)
            created_users.append(user.serialize())
        except ValueError as e:
            errors.append({'partner_data': partner_data, 'error': str(e)})

    if errors:
        return jsonify({
            'created_users': created_users,
            'errors': errors
        }), 400

    return jsonify({
        'created_users': created_users
    }), 201