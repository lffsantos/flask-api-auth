from flask import request

from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from bcrypt import checkpw
from marshmallow import ValidationError

from apps.users.business import get_user_by_email
from apps.users.models import User
from apps.users.schemas import UserSchema
from apps.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.responses import resp_ok, resp_data_invalid, resp_notallowed_user, resp_authenticated_user

from .schemas import LoginSchema


class AuthResource(Resource):

    def post(self, *args, **kwargs):

        payload = request.get_json() or None

        login_schema = LoginSchema()
        schema = UserSchema()

        if payload is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        try:
            data = login_schema.load(payload)
        except ValidationError as error:
            return resp_data_invalid('Users', error.messages)

        user = get_user_by_email(data.get('email'))

        # if not instance of User return response error
        if not isinstance(user, User):
            return user

        if not user.is_active:
            return resp_notallowed_user('Auth')

        # trick for test pass
        password = user.password
        if isinstance(password, str):
            password = password.encode('utf-8')

        if checkpw(data.get('password').encode('utf-8'), password):

            extras = {
                'token': create_access_token(identity=user.email),
                'refresh': create_refresh_token(identity=user.email)
            }

            result = schema.dump(user)

            return resp_ok('Auth', MSG_TOKEN_CREATED, data=result, **extras)

        return resp_authenticated_user('Auth')


class RefreshTokenResource(Resource):

    @jwt_refresh_token_required
    def post(self, *args, **kwargs):
        """
        Refresh a token that expired.
        """
        extras = {'token': create_access_token(identity=get_jwt_identity())}

        return resp_ok('Auth', MSG_TOKEN_CREATED, **extras)
