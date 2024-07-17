from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import uuid
from ..models.user import User
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
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, data['password']):
        token = jwt.encode(
            {'public_id': user.public_id, 'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            current_app.config['SECRET_KEY']
        )
        return jsonify({'token': token, 'user': user.serialize()})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validar datos obligatorios
    required_fields = ['password', 'nombre', 'apellido', 'pais', 'ciudad', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es obligatorio'}), 400

    # Verificar si el email ya está en uso
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'El email ya está en uso'}), 400

    # Validar datos opcionales y proporcionar valores predeterminados si es necesario
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        password=hashed_password,
        nombre=data['nombre'],
        apellido=data['apellido'],
        pais=data['pais'],
        ciudad=data['ciudad'],
        email=data['email'],
        nro_telefono=data.get('nro_telefono'),
        sexo=data.get('sexo'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        suscrito_newsletter=data.get('suscrito_newsletter', False),
        estado='activo',
        image_url=data.get('image_url')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Successfully registered!'}), 201

@auth_blueprint.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    return jsonify(current_user.serialize())

@auth_blueprint.route('/user', methods=['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()

    # Actualizar solo los campos que se pasan en el cuerpo de la solicitud
    if 'password' in data:
        current_user.password = generate_password_hash(data['password'])
    if 'nombre' in data:
        current_user.nombre = data['nombre']
    if 'apellido' in data:
        current_user.apellido = data['apellido']
    if 'pais' in data:
        current_user.pais = data['pais']
    if 'ciudad' in data:
        current_user.ciudad = data['ciudad']
    if 'nro_telefono' in data:
        current_user.nro_telefono = data['nro_telefono']
    if 'sexo' in data:
        current_user.sexo = data['sexo']
    if 'fecha_nacimiento' in data:
        current_user.fecha_nacimiento = data['fecha_nacimiento']
    if 'suscrito_newsletter' in data:
        current_user.suscrito_newsletter = data['suscrito_newsletter']
    if 'image_url' in data:
        current_user.image_url = data['image_url']    

    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': current_user.serialize()})

