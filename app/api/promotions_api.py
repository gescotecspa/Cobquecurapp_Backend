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
    
class PromotionImageResource(Resource):
    def post(self):
        data = request.get_json()
        image_ids = data.get('image_ids', [])
        print(image_ids)
        if PromotionService.delete_promotion_images(image_ids):
            return {'message': 'Images deleted'}, 200
        return {'message': 'Images not found'}, 404    

class PromotionByPartnerResource(Resource):
    def get(self, partner_id):
        promotions = PromotionService.get_promotions_by_partner(partner_id)
        if promotions:
            return jsonify([promotion.serialize(include_user_info=False) for promotion in promotions])
        print(promotions)
        return promotions, 200

class PromotionBulkDeleteResource(Resource):
    def put(self):
        data = request.get_json()
        promotion_ids = data.get('promotion_ids', [])
        status_id = data.get('status_id')  # Suponiendo que 'status_id' es el valor que indica que la promoción fue eliminada

        # Verificar si se recibió el arreglo de IDs de promociones y el status_id
        if not promotion_ids or not status_id:
            return {'message': 'Missing promotion_ids or status_id'}, 400

        # Llamamos al servicio para actualizar las promociones
        updated_promotions = PromotionService.bulk_update_promotions_status(promotion_ids, status_id)
        
        if updated_promotions:
            return {'message': 'Promotions updated successfully'}, 200
        return {'message': 'Failed to update promotions'}, 500
    
api.add_resource(PromotionResource, '/promotions/<int:promotion_id>')
api.add_resource(PromotionListResource, '/promotions')
api.add_resource(PromotionImageResource, '/promotion_images/delete')
api.add_resource(PromotionByPartnerResource, '/partners/<int:partner_id>/promotions')
api.add_resource(PromotionBulkDeleteResource, '/promotions/bulk_delete')