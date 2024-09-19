from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services import tourist_point_service

tourist_point_api_blueprint = Blueprint('tourist_point_api', __name__)
api = Api(tourist_point_api_blueprint)

class TouristPointResource(Resource):
    def get(self, id):
        tourist_point = tourist_point_service.get_tourist_point_by_id(id)
        if tourist_point:
            return tourist_point  # El objeto ya está serializado
        return {'message': 'Tourist point not found'}, 404

    def put(self, id):
        data = request.get_json()
        # Extraer datos de las imágenes si existen
        images = data.pop('images', [])
        for image in images:
            image['data'] = image.get('data')
            image['filename'] = image.get('filename')

        updated_tourist_point = tourist_point_service.update_tourist_point(id, data)
        if updated_tourist_point:
            return updated_tourist_point  # El objeto ya está serializado
        return {'message': 'Tourist point not found'}, 404

class TouristPointListResource(Resource):
    def get(self):
        tourist_points = tourist_point_service.get_all_tourist_points()
        return tourist_points

    def post(self):
        data = request.get_json()
        # Extraer datos de las imágenes si existen
        # images = data.pop('images', [])
        # for image in images:
        #     image['data'] = image.get('data')
        #     image['filename'] = image.get('filename')
        
        tourist_point = tourist_point_service.create_tourist_point(data)
        return tourist_point.serialize(), 201  

class ImageResource(Resource):
    def post(self, id):
        data = request.get_json()
        # Manejo de la imagen usando ImageManager
        image = tourist_point_service.add_image(id, data['image'])
        return image, 201 

class RatingResource(Resource):
    
    def get(self, id):
        """
        Obtener todas las valoraciones de un punto turístico específico.
        """
        ratings = tourist_point_service.get_ratings_by_tourist_point(id)
        if not ratings:
            return {'message': 'No ratings found for this tourist point.'}, 404
        return jsonify([rating.serialize() for rating in ratings])
    
    def post(self, id):
        data = request.get_json()
        rating = tourist_point_service.add_rating(id, data['tourist_id'], data['rating'], data.get('comment'))
        return rating

class RatingDetailResource(Resource):
    def delete(self, rating_id):
        success = tourist_point_service.delete_rating(rating_id)
        if success is None:
            return {'message': 'Rating not found'}, 404
        return {'message': 'Rating deleted successfully'}, 200  # Mensaje de confirmación

    def put(self, rating_id):
        data = request.get_json()
        rating = tourist_point_service.update_rating(rating_id, data)
        if rating is None:
            return {'message': 'Rating not found'}, 404
        return rating

class AverageRatingResource(Resource):
    def get(self, id):
        avg_rating = tourist_point_service.get_average_rating(id)
        return avg_rating, 200


api.add_resource(TouristPointResource, '/tourist_points/<int:id>')
api.add_resource(TouristPointListResource, '/tourist_points')
api.add_resource(ImageResource, '/tourist_points/<int:id>/images')
api.add_resource(RatingResource, '/tourist_points/<int:id>/ratings')
api.add_resource(RatingDetailResource, '/ratings/<int:rating_id>')
api.add_resource(AverageRatingResource, '/tourist_points/<int:id>/average_rating')
