from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.terms_and_conditions_service import TermsAndConditionsService

terms_and_conditions_api_blueprint = Blueprint('terms_and_conditions_api', __name__)
api = Api(terms_and_conditions_api_blueprint)

class TermsAndConditionsResource(Resource):
    def get(self, terms_id):
        terms = TermsAndConditionsService.get_terms_by_id(terms_id)
        if terms:
            return jsonify(terms.serialize())
        return {'message': 'Terms and conditions not found'}, 404

    def put(self, terms_id):
        data = request.get_json()
        terms = TermsAndConditionsService.update_terms(terms_id, data['content'], data['version'])
        if terms:
            return jsonify(terms.serialize())
        return {'message': 'Terms and conditions not found or update failed'}, 404

    def delete(self, terms_id):
        if TermsAndConditionsService.delete_terms(terms_id):
            return {'message': 'Terms and conditions deleted'}, 200
        return {'message': 'Terms and conditions not found'}, 404

class TermsAndConditionsListResource(Resource):
    #traer la ultima version de terminos y condiciones
    def get(self):
        terms_last_version = TermsAndConditionsService.get_latest_version()
        return jsonify(terms_last_version.serialize())

    def post(self):
        data = request.get_json()
        terms = TermsAndConditionsService.create_terms(data['content'], data['version'])
        return jsonify(terms.serialize())
   
# Para aceptar nuevos términos y condiciones, acepta el último disponible 
class AcceptTermsResource(Resource):
    
    def put(self, user_id):
        try:
            user = TermsAndConditionsService.accept_terms(user_id)
            return jsonify(user.serialize())
        except ValueError as e:
            return {'message': str(e)}, 400
        
api.add_resource(TermsAndConditionsResource, '/terms/<int:terms_id>')
api.add_resource(TermsAndConditionsListResource, '/terms')
api.add_resource(AcceptTermsResource, '/users/<int:user_id>/accept-terms')
