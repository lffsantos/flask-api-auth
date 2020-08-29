from flask import request

from flask_restful import Resource

from apps.users.business import register_user


class SignUp(Resource):

    def post(self, *args, **kwargs):
        payload = request.get_json()
        response = register_user(payload)
        return response
