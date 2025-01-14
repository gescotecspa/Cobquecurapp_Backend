from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.services.app_version_service import AppVersionService

app_version_api_blueprint = Blueprint('app_version_api', __name__)
api = Api(app_version_api_blueprint)

class AppVersionResource(Resource):
    def get(self, version_id):
        version = AppVersionService.get_version_by_id(version_id)
        if version:
            return jsonify(version.serialize())
        return {'message': 'Version not found'}, 404

    def put(self, version_id):
        data = request.get_json()
        version = AppVersionService.update_version(version_id, **data)
        if version:
            return jsonify(version.serialize())
        return {'message': 'Version not found'}, 404

    def delete(self, version_id):
        if AppVersionService.delete_version(version_id):
            return {'message': 'Version deleted'}, 200
        return {'message': 'Version not found'}, 404


class AppVersionListResource(Resource):
    def get(self):
        versions = AppVersionService.get_all_versions()
        return jsonify([version.serialize() for version in versions])

    def post(self):
        data = request.get_json()
        version = AppVersionService.create_version(**data)
        return jsonify(version.serialize()), 201


class ActiveAppVersionResource(Resource):
    def get(self, platform):
        version = AppVersionService.get_active_version(platform)
        if version:
            return jsonify(version.serialize())
        return {'message': f'No active version found for platform {platform}'}, 404


api.add_resource(AppVersionResource, '/versions/<int:version_id>')
api.add_resource(AppVersionListResource, '/versions')
api.add_resource(ActiveAppVersionResource, '/versions/active/<string:platform>')