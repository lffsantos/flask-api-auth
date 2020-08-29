from flask import request

from flask_restful import Resource

from apps.users.business import save_new_user


class SignUp(Resource):

    def post(self, *args, **kwargs):
        payload = request.get_json()
        response = save_new_user(payload)
        return response
