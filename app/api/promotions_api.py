from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.promotion_service import PromotionService

promotion_api_blueprint = Blueprint('promotion_api', __name__)
api = Api(promotion_api_blueprint)

class PromotionResource(Resource):
    def get(self, promotion_id):
        promotion = PromotionService.get_promotion_by_id(promotion_id)
        if promotion:
            return jsonify(promotion.serialize())
        return {'message': 'Promotion not found'}, 404

    def put(self, promotion_id):
        data = request.get_json()
        promotion = PromotionService.update_promotion(promotion_id, **data)
        if promotion:
            return jsonify(promotion.serialize())
        return {'message': 'Promotion not found'}, 404

    def delete(self, promotion_id):
        if PromotionService.delete_promotion(promotion_id):
            return {'message': 'Promotion deleted'}, 200
        return {'message': 'Promotion not found'}, 404

class PromotionListResource(Resource):
    def get(self):
        promotions = PromotionService.get_all_promotions()
        return jsonify([promotion.serialize() for promotion in promotions])

    def post(self):
        data = request.get_json()
        promotion = PromotionService.create_promotion(**data)
        return jsonify(promotion.serialize())

api.add_resource(PromotionResource, '/promotions/<int:promotion_id>')
api.add_resource(PromotionListResource, '/promotions')
