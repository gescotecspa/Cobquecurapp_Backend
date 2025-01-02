from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.tourist_point_service import TouristPointService

tourist_point_api_blueprint = Blueprint('tourist_point_api', __name__)
api = Api(tourist_point_api_blueprint)

class TouristPointResource(Resource):
    def get(self, id):
        tourist_point = TouristPointService.get_tourist_point_by_id(id)
        if tourist_point:
            return tourist_point  # El objeto ya está serializado
        return {'message': 'Tourist point not found'}, 404

    def put(self, id):
        data = request.get_json()
        # Extraer datos de las imágenes si existen
        # images = data.pop('images', [])
        # for image in images:
        #     image['data'] = image.get('data')
        #     image['filename'] = image.get('filename')

        updated_tourist_point = TouristPointService.update_tourist_point(id, data)
        if updated_tourist_point:
            return updated_tourist_point  # El objeto ya está serializado
        return {'message': 'Tourist point not found'}, 404
    
    def delete(self, id):
        """Realiza un borrado lógico del punto turístico"""
        deleted_tourist_point = TouristPointService.delete_tourist_point(id)
        if deleted_tourist_point:
            return {'message': 'Tourist point deleted (logical delete)'}, 200
        return {'message': 'Tourist point not found'}, 404

class TouristPointListResource(Resource):
    def get(self):
        tourist_points = TouristPointService.get_all_tourist_points()
        return tourist_points

    def post(self):
        data = request.get_json()
        # Extraer datos de las imágenes si existen
        # images = data.pop('images', [])
        # for image in images:
        #     image['data'] = image.get('data')
        #     image['filename'] = image.get('filename')
        
        tourist_point = TouristPointService.create_tourist_point(data)
        return tourist_point.serialize(), 201  

class ImageResource(Resource):
    def post(self, id):
        data = request.get_json()
        # Manejo de la imagen usando ImageManager
        image = TouristPointService.add_image(id, data['image'])
        return image, 201 

class RatingResource(Resource):
    
    def get(self, id):
        """
        Obtener todas las valoraciones de un punto turístico específico.
        """
        ratings = TouristPointService.get_ratings_by_tourist_point(id)
        if not ratings:
            return {'message': 'No ratings found for this tourist point.'}, 404
        return jsonify([rating.serialize() for rating in ratings])
    
    def post(self, id):
        data = request.get_json()
        rating = TouristPointService.add_rating(id, data['tourist_id'], data['rating'], data.get('comment'))
        return rating

class RatingVersionedResource(Resource):
    
    def get(self, id, version):
        """
        Obtener todas las valoraciones de un punto turístico específico.
        """
        if version == 'v2':
            ratings = TouristPointService.get_ratings_by_tourist_point(id)
            if not ratings:
                return {'message': 'No ratings found for this tourist point.'}, 404
            
            average_rating = TouristPointService.get_average_rating(id)
            
            response = {
            'ratings': [rating.serialize() for rating in ratings],
            'average_rating': average_rating['average_rating']
            }
            return response, 200
        else:
            return {'message': 'API version not supported'}, 400

class AllTouristPointListResource(Resource):
    def get(self):
        """
        Obtener todos los puntos turísticos excepto aquellos con estado 'deleted'.
        """
        tourist_points = TouristPointService.get_all_except_deleted()
        return tourist_points, 200
    
class RatingDetailResource(Resource):
    def delete(self, rating_id):
        success = TouristPointService.delete_rating(rating_id)
        if success is None:
            return {'message': 'Rating not found'}, 404
        return {'message': 'Rating deleted successfully'}, 200  # Mensaje de confirmación

    def put(self, rating_id):
        data = request.get_json()
        rating = TouristPointService.update_rating(rating_id, data)
        if rating is None:
            return {'message': 'Rating not found'}, 404
        return rating

class AverageRatingResource(Resource):
    def get(self, id):
        avg_rating = TouristPointService.get_average_rating(id)
        return avg_rating, 200

class ImageDeleteResource(Resource):
    def post(self, id):
        data = request.get_json()
        image_ids = data.get('image_ids', [])
        
        if not image_ids:
            return {'message': 'No image IDs provided'}, 400

        success = TouristPointService.delete_tourist_point_images(image_ids)
        
        if success:
            return {'message': 'Images deleted successfully'}, 200
        else:
            return {'message': 'Failed to delete images'}, 500
        
api.add_resource(TouristPointResource, '/tourist_points/<int:id>')
api.add_resource(TouristPointListResource, '/tourist_points')
api.add_resource(ImageResource, '/tourist_points/<int:id>/images')
api.add_resource(RatingResource, '/tourist_points/<int:id>/ratings')
api.add_resource(RatingDetailResource, '/ratings/<int:rating_id>')
api.add_resource(AverageRatingResource, '/tourist_points/<int:id>/average_rating')
api.add_resource(ImageDeleteResource, '/tourist_points/<int:id>/images/delete')
api.add_resource(AllTouristPointListResource, '/tourist_points/active-inactive')
api.add_resource(RatingVersionedResource, '/<string:version>/tourist_points/<int:id>/ratings')