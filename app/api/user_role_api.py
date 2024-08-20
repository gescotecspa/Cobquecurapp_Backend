from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.user_role_service import UserRoleService

user_role_api_blueprint = Blueprint('user_role_api', __name__)
api = Api(user_role_api_blueprint)

class UserRoleResource(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        role_ids = data.get('role_ids')

        if user_id is None or not role_ids:
            return {'message': 'Missing user_id or role_ids'}, 400

        UserRoleService.clear_roles_for_user(user_id)
        
        failed_roles = []
        for role_id in role_ids:
            result = UserRoleService.add_role_to_user(user_id, role_id)
            if not result:
                failed_roles.append(role_id)

        if failed_roles:
            return {
                'message': 'Some roles failed to assign',
                'failed_roles': failed_roles
            }, 400
        else:
            return {'message': 'Roles updated successfully'}, 201

api.add_resource(UserRoleResource, '/assign_roles_to_user')
