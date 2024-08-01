from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.favorite_service import FavoriteService

favorite_api_blueprint = Blueprint('favorite_api', __name__)
api = Api(favorite_api_blueprint)

class FavoriteResource(Resource):
    def post(self):
        data = request.get_json()
        favorite = FavoriteService.add_favorite(data['user_id'], data['promotion_id'])
        if favorite is None:
            return jsonify({'message': 'Favorite already exists'})
        return jsonify(favorite.serialize())

    def delete(self):
        data = request.get_json()
        success = FavoriteService.remove_favorite(data['user_id'], data['promotion_id'])
        if success:
            return jsonify({'message': 'Favorite removed'})
        return jsonify({'message': 'Favorite not found'})

class TouristFavoritesResource(Resource):
    def get(self, user_id):
        favorites = FavoriteService.get_favorites_by_tourist(user_id)
        return jsonify([fav.serialize() for fav in favorites])

class PromotionFavoritesResource(Resource):
    def get(self, promotion_id):
        favorites = FavoriteService.get_favorites_by_promotion(promotion_id)
        return jsonify([fav.serialize() for fav in favorites])

api.add_resource(FavoriteResource, '/favorites')
api.add_resource(TouristFavoritesResource, '/users/<int:user_id>/favorites')
api.add_resource(PromotionFavoritesResource, '/promotions/<int:promotion_id>/favorites')