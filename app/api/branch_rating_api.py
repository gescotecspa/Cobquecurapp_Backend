from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.branch_rating_service import BranchRatingService

branch_rating_api_blueprint = Blueprint('branch_rating_api', __name__)
api = Api(branch_rating_api_blueprint)

class BranchRatingResource(Resource):
    def post(self, branch_id):
        data = request.get_json()
        user_id = data.get('user_id')
        rating = data.get('rating')
        comment = data.get('comment')

        if not user_id or not rating:
            return {'message': 'user_id and rating are required'}, 400

        rating = BranchRatingService.create_rating(branch_id, user_id, rating, comment)
        if rating:
            return rating.serialize(), 201
        return {'message': 'Rating already exists for this branch and user'}, 400

class BranchRatingUpdateResource(Resource):
    def put(self, rating_id):
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment')

        if rating is None:
            return {'message': 'Rating is required'}, 400

        updated_rating = BranchRatingService.update_rating(rating_id, rating, comment)
        if updated_rating:
            return updated_rating.serialize(), 200
        return {'message': 'Rating not found'}, 404

    def delete(self, rating_id):
        deleted_rating = BranchRatingService.delete_rating(rating_id)
        if deleted_rating:
            return {'message': 'Rating deleted'}, 200
        return {'message': 'Rating not found'}, 404

class BranchRatingsListResource(Resource):
    def get(self, branch_id):
        ratings_with_names = BranchRatingService.get_all_ratings_for_branch(branch_id)
        if not ratings_with_names:
            return {'message': 'No ratings found for this branch'}, 404

        avg_rating = BranchRatingService.get_average_rating_for_branch(branch_id)
        
        response = {
            'ratings': [rating.serialize(first_name) for rating, first_name in ratings_with_names],
            'average_rating': avg_rating
        }
        return response, 200

class BranchAverageRatingResource(Resource):
    def get(self, branch_id):
        avg_rating = BranchRatingService.get_average_rating_for_branch(branch_id)
        return jsonify({'average_rating': avg_rating}), 200

api.add_resource(BranchRatingResource, '/branches/<int:branch_id>/ratings')
api.add_resource(BranchRatingUpdateResource, '/branches/ratings/<int:rating_id>')
api.add_resource(BranchRatingsListResource, '/branches/<int:branch_id>/ratings/all')
api.add_resource(BranchAverageRatingResource, '/branches/<int:branch_id>/average_rating')

