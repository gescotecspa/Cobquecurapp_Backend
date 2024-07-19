from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.partner_service import PartnerService

partner_api_blueprint = Blueprint('partner_api', __name__)
api = Api(partner_api_blueprint)

class PartnerResource(Resource):
    def get(self, user_id):
        partner = PartnerService.get_partner_by_user_id(user_id)
        if partner:
            return jsonify(partner.serialize())
        return {'message': 'Partner not found'}, 404

    def put(self, user_id):
        data = request.get_json()
        partner = PartnerService.update_partner(user_id, **data)
        if partner:
            return jsonify(partner.serialize())
        return {'message': 'Partner not found'}, 404

    def delete(self, user_id):
        if PartnerService.delete_partner(user_id):
            return {'message': 'Partner deleted'}, 200
        return {'message': 'Partner not found'}, 404

class PartnerListResource(Resource):
    def get(self):
        partners = PartnerService.get_all_partners()
        return jsonify([partner.serialize() for partner in partners])

    def post(self):
        data = request.get_json()
        partner = PartnerService.create_partner(**data)
        return jsonify(partner.serialize())

api.add_resource(PartnerResource, '/partners/<int:user_id>')
api.add_resource(PartnerListResource, '/partners')