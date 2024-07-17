from flask import Blueprint

categories_blueprint = Blueprint('categories', __name__)

# Aquí puedes definir tus rutas para las categorías
@categories_blueprint.route('/categories', methods=['GET'])
def get_categories():
    # Lógica para obtener las categorías
    return "Lista de categorías"