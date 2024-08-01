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
    
    # Inicializar SQLAlchemy con la aplicación Flask
    db.init_app(app)
    
    # Inicializar Flask-Migrate con la aplicación Flask y la instancia de SQLAlchemy
    migrate = Migrate(app, db)
    
    # Habilitar CORS si es necesario
    CORS(app, resources={r"*": {"origins": "*"}})

    # Importar e inicializar las rutas de la API

    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.api.promotions_api import promotion_api_blueprint
    app.register_blueprint(promotion_api_blueprint)

    from app.api.category_api import category_api_blueprint
    app.register_blueprint(category_api_blueprint)

    from app.api.role_api import role_api_blueprint
    app.register_blueprint(role_api_blueprint)

    from app.api.funcionalty_api import functionality_api_blueprint
    app.register_blueprint(functionality_api_blueprint)

    from app.api.tourist_api import tourist_api_blueprint
    app.register_blueprint(tourist_api_blueprint)

    from app.api.partner_api import partner_api_blueprint
    app.register_blueprint(partner_api_blueprint)

    from app.api.favorite_api import favorite_api_blueprint
    app.register_blueprint(favorite_api_blueprint)
    
    from app.api.branches_api import branch_api_blueprint
    app.register_blueprint(branch_api_blueprint)

    # Importar modelos para asegurarse de que se reconocen al crear la base de datos
    from app.models import user, category, tourist, partner, promotion, branch, favorite

    # Importar e inicializar los manejadores de errores
    # from app.common import error_handlers
    # error_handlers.init_app(app)
    
    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
