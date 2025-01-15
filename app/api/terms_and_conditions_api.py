from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.terms_and_conditions_service import TermsAndConditionsService
from app.auth.auth import token_required

terms_and_conditions_api_blueprint = Blueprint('terms_and_conditions_api', __name__)
api = Api(terms_and_conditions_api_blueprint)

class TermsAndConditionsResource(Resource):
    @token_required
    def get(self, current_user, terms_id):
        terms = TermsAndConditionsService.get_terms_by_id(terms_id)
        if terms:
            return terms.serialize(), 200
        return {'message': 'Terms and conditions not found'}, 404

    @token_required
    def put(self, current_user, terms_id):
        data = request.get_json()
        terms = TermsAndConditionsService.update_terms(terms_id, data['content'], data['version'])
        if terms:
            return terms.serialize(), 200
        return {'message': 'Terms and conditions not found or update failed'}, 404

    @token_required
    def delete(self, current_user, terms_id):
        if TermsAndConditionsService.delete_terms(terms_id):
            return {'message': 'Terms and conditions deleted'}, 200
        return {'message': 'Terms and conditions not found'}, 404

class TermsAndConditionsListResource(Resource):
    @token_required
    def get(self, current_user):
        terms_last_version = TermsAndConditionsService.get_latest_version()
        if terms_last_version:
            return terms_last_version.serialize(), 200
        return {'message': 'No terms and conditions found'}, 404

    @token_required
    def post(self):
        data = request.get_json()
        terms = TermsAndConditionsService.create_terms(data['content'], data['version'])
        return jsonify(terms.serialize())

class AcceptTermsResource(Resource):
    @token_required
    def put(self, current_user, user_id):
        try:
            user = TermsAndConditionsService.accept_terms(user_id)
            return jsonify(user.serialize())
        except ValueError as e:
            return {'message': str(e)}, 400

api.add_resource(TermsAndConditionsResource, '/terms/<int:terms_id>')
api.add_resource(TermsAndConditionsListResource, '/terms')
api.add_resource(AcceptTermsResource, '/users/<int:user_id>/accept-terms')
