from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate



# Instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Crear una instancia de Flask
    app = Flask(__name__)
    print("creo la app")
    # Configuración de la aplicación
    app.config.from_object('config.Config')
    
    # # Inicializar SQLAlchemy con la aplicación Flask
    db.init_app(app)
    
    # Inicializar Flask-Migrate con la aplicación Flask y la instancia de SQLAlchemy
    migrate = Migrate(app, db)
    
    # # Habilitar CORS si es necesario
    CORS(app, resources={r"*": {"origins": "*"}})

    # # Importar e inicializar las rutas de la API

    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.api.categorias_api import categories_blueprint
    app.register_blueprint(categories_blueprint)
   # Importar modelos para asegurarse de que se reconocen al crear la base de datos
    from app.models import user, category
    # # Importar e inicializar los manejadores de errores
    #from app.common import error_handlers
    #error_handlers.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
