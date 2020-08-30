from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Api, Resource

from apps.auth.resources import AuthResource, RefreshTokenResource
from apps.users.resources import SignUp


class Index(Resource):

    def get(self):
        return {'status': True}


class IndexProtected(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'user': current_user}


api = Api()


def configure_api(app):
    api.add_resource(Index, '/')
    api.add_resource(IndexProtected, '/protected')
    api.add_resource(SignUp, '/users')
    api.add_resource(AuthResource, '/auth')
    api.add_resource(RefreshTokenResource, '/auth/refresh')
    api.init_app(app)
