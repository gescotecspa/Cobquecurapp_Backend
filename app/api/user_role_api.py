from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.user_role_service import UserRoleService

user_role_api_blueprint = Blueprint('user_role_api', __name__)
api = Api(user_role_api_blueprint)

class UserRoleResource(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        role_id = data.get('role_id')
        if user_id is None or role_id is None:
            return {'message': 'Missing user_id or role_id'}, 400

        result = UserRoleService.add_role_to_user(user_id, role_id)
        if result:
            return {'message': 'Role assigned to user successfully'}, 201
        else:
            return {'message': 'Failed to assign role'}, 400

api.add_resource(UserRoleResource, '/assign_role_to_user')