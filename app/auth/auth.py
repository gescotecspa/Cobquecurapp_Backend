import os
import jwt
import datetime
import uuid
import random
import string

from functools import wraps
from flask import Blueprint, request, jsonify, current_app, render_template
from flask_restful import abort as rest_abort
from werkzeug.security import generate_password_hash, check_password_hash

# Importaciones de tu proyecto (ajusta la ruta según corresponda)
from ..models.user import User
from ..services.user_service import UserService
from ..common.email_utils import send_email
from app import db

auth_blueprint = Blueprint('auth', __name__)

# =====================================
# DECORADOR
# =====================================
def token_required(f):
    """
    Decorador que maneja la necesidad de token según la variable `token_required` en .env:
    - Si en .env: token_required = "true"  => Se exige token (401 si no llega).
    - Si en .env: token_required = "false" => El token es opcional.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Leer variable del .env en minúsculas
        is_token_required = os.getenv("token_required", False)

        token = None
        # Verificar cabecera Authorization
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            # Si NO hay token
            if is_token_required == "True":

                # Si .env dice "true", exigimos token
                rest_abort(401, message="Token is missing!")
            else:
                # Si .env dice "false", no exigimos token
                kwargs['current_user'] = None
                return f(*args, **kwargs)

        # Si hay token, lo validamos
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            # Verificar si es un token de invitado
            if data.get("is_guest"):
                current_user = {"is_guest": True, "guest_id": data.get("guest_id")}
            else:
                # Token de usuario registrado
                current_user = User.query.filter_by(email=data.get('email')).first()
                if not current_user:
                    rest_abort(404, message="User not found!")
            
            kwargs['current_user'] = current_user

        except jwt.ExpiredSignatureError:
            rest_abort(401, message="Token has expired!")
        except jwt.InvalidTokenError as e:
            rest_abort(401, message=f"Token is invalid: {str(e)}")
        except Exception as e:
            rest_abort(500, message=f"Error al validar el token: {str(e)}")

        return f(*args, **kwargs)
    return decorated

# =====================================
# RUTAS DE AUTENTICACIÓN
# =====================================

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Debe ingresar email y contraseña'}), 400

    user = UserService.get_user_by_email(data['email'])
    if not user:
        return jsonify({'message': 'No existe el usuario'}), 404

    if check_password_hash(user.password, data['password']):
        try:
            token = jwt.encode(
                {
                    'email': user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                current_app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            return jsonify({'token': token, 'user': user.serialize()}), 200
        except Exception as e:
            return jsonify({'message': f'Error al generar el token: {str(e)}'}), 500

    return jsonify({'message': 'Contraseña inválida'}), 401


@auth_blueprint.route('/guest-login', methods=['POST'])
def guest_login():
    guest_id = str(uuid.uuid4())
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    payload = {
        "is_guest": True,
        "guest_id": guest_id,
        "exp": expiration_time
    }

    try:
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return jsonify({"guest_token": token}), 200
    except Exception as e:
        return jsonify({"message": f"Error al generar el token: {str(e)}"}), 500


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    image_data = data.pop('image_data', None)

    try:
        if not data.get('accept_terms'):
            return jsonify({'message': 'Debe aceptar los términos y condiciones'}), 400

        user = UserService.create_user(**data, image_data=image_data)
        return jsonify(user.serialize()), 201
    except ValueError as e:
        return {'message': str(e)}, 400


# =====================================
# RUTAS QUE DEPENDEN DE LA VARIABLE token_required
# =====================================

@auth_blueprint.route('/user', methods=['GET'])
@token_required
def get_user(current_user=None):
    """
    Si token_required = "true" y no envías token => 401
    Si token_required = "false" y no envías token => current_user=None
    """
    if current_user is None:
        # Sin token (cuando .env => "false")
        return jsonify({"message": "Versión antigua: no se ha enviado token"}), 200
    
    if isinstance(current_user, dict) and current_user.get("is_guest"):
        # Invitado
        return {"message": "Eres invitado, no puedes acceder a esta ruta de usuario registrado."}, 403
    
    # Usuario con token válido
    return jsonify(current_user.serialize()), 200


@auth_blueprint.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user=None):
    """
    - Si token_required = "false" y no envías token => current_user=None => lógica antigua
    - Si llega un token de invitado => dict con is_guest
    - Si llega token de usuario => current_user es User
    """
    if current_user is None:
        # Sin token (modo antiguo)
        return jsonify({"message": "Versión antigua: sin token, vista limitada de usuarios"}), 200
    
    if isinstance(current_user, dict) and current_user.get('is_guest'):
        return {"message": "Invitado no puede ver la lista completa de usuarios."}, 403
    
    # Usuario registrado con token
    users = UserService.get_all_users()
    return jsonify([user.serialize() for user in users]), 200


# =====================================
# RUTAS QUE REALMENTE REQUIEREN TOKEN
# (p.ej., acceso crítico)
# =====================================
@auth_blueprint.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """
    Si token_required = "false" en .env, este endpoint igual permite "pasar sin token"???
    - Con esta configuración actual, sí. Depende de lo que quieras hacer.
    - Si deseas forzar el token para ciertos endpoints aunque el .env diga "false",
      deberías cambiar la lógica o tener otro decorador.
    """
    if current_user is None:
        # Lógica si se permite sin token (solo cuando .env="false")
        return {"message": "No tienes token para actualizar usuario."}, 403

    data = request.get_json()
    image_data = data.pop('image_data', None)

    user = UserService.update_user(user_id, **data, image_data=image_data)
    if user:
        return jsonify(user.serialize())
    return {'message': 'User not found'}, 404


@auth_blueprint.route('/signup-partner', methods=['POST'])
@token_required
def signup_partner(current_user):
    if current_user is None:
        return {"message": "No token, acción no permitida"}, 403

    data = request.get_json()
    image_data = data.pop('image_data', None)
    
    try:
        user = UserService.create_user_partner(**data)
        return jsonify(user.serialize()), 201
    except ValueError as e:
        return {'message': str(e)}, 400


# =====================================
# BULK CREATION (también protegidas)
# =====================================
@auth_blueprint.route('/signup/bulk', methods=['POST'])
@token_required
def create_bulk_users(current_user):
    if current_user is None:
        return {"message": "No token, acción no permitida"}, 403

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
@token_required
def signup_partners(current_user):
    if current_user is None:
        return {"message": "No token, acción no permitida"}, 403

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


# =====================================
# RESTABLECER CONTRASEÑA (SIN TOKEN)
# =====================================
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

    reset_url = "https://www.cobquecurapp.cl/reset_password"
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