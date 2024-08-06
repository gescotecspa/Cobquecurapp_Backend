from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.tourist_rating_service import TouristRatingService

tourist_rating_api_blueprint = Blueprint('tourist_rating_api', __name__)
api = Api(tourist_rating_api_blueprint)

class TouristRatingResource(Resource):
    def post(self, tourist_id):
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        branch_id = data.get('branch_id')
        rating = data.get('rating')
        comment = data.get('comment')

        if branch_id is None or rating is None:
            return jsonify({'message': 'Missing branch_id or rating'}), 400

        new_rating, error_message = TouristRatingService.create_rating(
            tourist_id,
            branch_id,
            rating,
            comment
        )
        if new_rating:
            return new_rating.serialize(), 201
        return {'message': error_message}, 409
    
class TouristRatingUpdateResource(Resource):
    def put(self, rating_id):
        data = request.get_json()
        rating = TouristRatingService.update_rating(
            rating_id,
            data['rating'],
            data.get('comment')
        )
        if rating:
            return rating.serialize(), 200
        return {'message': 'Rating not found'}, 404

    def delete(self, rating_id):
        rating = TouristRatingService.delete_rating(rating_id)
        if rating:
            return rating.serialize(), 200
        return {'message': 'Rating not found'}, 404

class TouristRatingsListResource(Resource):
    def get(self, tourist_id):
        ratings = TouristRatingService.get_all_ratings_for_tourist(tourist_id)
        average_rating = TouristRatingService.get_average_rating_for_tourist(tourist_id)
        
        ratings_list = [rating.serialize() for rating in ratings]
        
        return {
            'ratings': ratings_list,
            'average_rating': average_rating
        }, 200

class TouristAverageRatingResource(Resource):
    def get(self, tourist_id):
        avg_rating = TouristRatingService.get_average_rating_for_tourist(tourist_id)
        return jsonify({'average_rating': avg_rating}), 200

api.add_resource(TouristRatingResource, '/tourists/<int:tourist_id>/ratings')
api.add_resource(TouristRatingUpdateResource, '/tourists/ratings/<int:rating_id>')
api.add_resource(TouristRatingsListResource, '/tourists/<int:tourist_id>/ratings/all')
api.add_resource(TouristAverageRatingResource, '/tourists/<int:tourist_id>/average_rating')
