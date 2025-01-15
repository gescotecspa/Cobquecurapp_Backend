from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from ..services.favorite_service import FavoriteService
from ..auth.auth import token_required  # Asegúrate de importar el decorador

favorite_api_blueprint = Blueprint('favorite_api', __name__)
api = Api(favorite_api_blueprint)

class FavoriteResource(Resource):
    @token_required
    def post(self, current_user):
        from app.models.tourist import Tourist  # Importar el modelo de turista
        try:
            data = request.get_json()

            # Validar campos requeridos
            if 'user_id' not in data or 'promotion_id' not in data:
                return {'message': 'Missing required fields: user_id or promotion_id'}, 400

            # Llamar al servicio para agregar favorito
            favorite = FavoriteService.add_favorite(data['user_id'], data['promotion_id'])
            if favorite is None:
                return {'message': 'Favorite already exists'}, 400

            return favorite.serialize(), 201

        except ValueError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            print(f"Error interno: {str(e)}")  # Depuración
            return {'message': 'Internal server error'}, 500


    @token_required
    def delete(self, current_user):
        data = request.get_json()
        success = FavoriteService.remove_favorite(data['user_id'], data['promotion_id'])
        if success:
            return jsonify({'message': 'Favorite removed'})
        return jsonify({'message': 'Favorite not found'})

class TouristFavoritesResource(Resource):
    @token_required
    def get(self, current_user, user_id):
        favorites = FavoriteService.get_favorites_by_tourist(user_id)
        return jsonify([fav.serialize() for fav in favorites])

class PromotionFavoritesResource(Resource):
    @token_required
    def get(self, current_user, promotion_id):
        favorites = FavoriteService.get_favorites_by_promotion(promotion_id)
        return jsonify([fav.serialize() for fav in favorites])

api.add_resource(FavoriteResource, '/favorites')
api.add_resource(TouristFavoritesResource, '/users/<int:user_id>/favorites')
api.add_resource(PromotionFavoritesResource, '/promotions/<int:promotion_id>/favorites')