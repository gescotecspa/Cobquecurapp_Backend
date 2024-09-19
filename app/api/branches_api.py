from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.branch_service import BranchService

branch_api_blueprint = Blueprint('branch_api', __name__)
api = Api(branch_api_blueprint)

class BranchResource(Resource):
    def get(self, branch_id):
        branch = BranchService.get_branch_by_id(branch_id)
        if branch:
            return jsonify(branch.serialize())
        return {'message': 'Branch not found'}, 404

    def put(self, branch_id):
        data = request.get_json()
        # Extraer datos de la imagen si existen
        image_data = data.pop('image_data', None)

        branch = BranchService.update_branch(branch_id, **data, image_data=image_data)
        if branch:
            return jsonify(branch.serialize())
        return {'message': 'Branch not found'}, 404

    def delete(self, branch_id):
        if BranchService.delete_branch(branch_id):
            return {'message': 'Branch deleted'}, 200
        return {'message': 'Branch not found'}, 404

class BranchListResource(Resource):
    def get(self):
        branches = BranchService.get_all_branches()
        return jsonify([branch.serialize() for branch in branches])

    def post(self):
        data = request.get_json()
        # Extraer datos de la imagen si existen
        image_data = data.pop('image_data', None)

        branch = BranchService.create_branch(**data, image_data=image_data)
        return jsonify(branch.serialize())
class PartnerBranchesResource(Resource):
    def get(self, partner_id):
        branches = BranchService.get_branches_by_partner_id(partner_id)
        if branches:
            return jsonify([branch.serialize() for branch in branches])
        return branches, 200
    
api.add_resource(BranchResource, '/branches/<int:branch_id>')
api.add_resource(BranchListResource, '/branches')
api.add_resource(PartnerBranchesResource, '/partners/<int:partner_id>/branches')
