from .categorias_api import categories_blueprint


def init_api(app):
    app.register_blueprint(categories_blueprint, url_prefix='/api')