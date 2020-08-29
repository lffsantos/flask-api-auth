from flask_restful import Api, Resource

from apps.users.resources import SignUp


class Index(Resource):

    def get(self):
        return {'status': True}


api = Api()


def configure_api(app):
    api.add_resource(Index, '/')
    api.add_resource(SignUp, '/users')
    api.init_app(app)
