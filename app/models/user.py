from app import db
import uuid

user_categories = db.Table('user_categories',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True, default=str(uuid.uuid4()))
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(50), default='Turista', nullable=False)
    
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    pais = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(120), nullable=False)
    fecha_nacimiento = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True, nullable=False)
    nro_telefono = db.Column(db.String(20))
    sexo = db.Column(db.String(10))
    estado = db.Column(db.String(20), default='activo', nullable=False)
    suscrito_newsletter = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(250), nullable=True) 
    categories = db.relationship('Category', secondary=user_categories, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "role": self.role,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "pais": self.pais,
            "ciudad": self.ciudad,
            "fecha_nacimiento": self.fecha_nacimiento,
            "email": self.email,
            "nro_telefono": self.nro_telefono,
            "sexo": self.sexo,
            "estado": self.estado,
            "suscrito_newsletter": self.suscrito_newsletter,
            "image_url": self.image_url,
            "categories": [category.serialize() for category in self.categories]
        }

    def __init__(self, password, nombre, apellido, pais, ciudad, email, role='Turista', fecha_nacimiento=None, nro_telefono=None, sexo=None, estado='activo', suscrito_newsletter=False, image_url=None):
        self.public_id = str(uuid.uuid4())
        self.password = password
        self.role = role
        self.nombre = nombre
        self.apellido = apellido
        self.pais = pais
        self.ciudad = ciudad
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.nro_telefono = nro_telefono
        self.sexo = sexo
        self.estado = estado
        self.suscrito_newsletter = suscrito_newsletter
        self.image_url = image_url

    def __repr__(self):
        return f"<User {self.email}>"
    
    @staticmethod
    def validate_role(role):
        valid_roles = ['Admin', 'Turista', 'Comercio']
        if role not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
