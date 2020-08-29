from bcrypt import hashpw, gensalt
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from apps import db
from apps.messages import MSG_NO_DATA, MSG_RESOURCE_CREATED
from apps.responses import resp_data_invalid, resp_exception, resp_ok, resp_already_exists
from apps.users.models import User
from apps.users.schemas import UserSchema, UserRegistrationSchema


def register_user(payload):
    if payload is None:
        return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

    schema = UserRegistrationSchema()

    password = payload.get('password', None)
    try:
        data = schema.load(payload)
    except ValidationError as error:
        return resp_data_invalid('Users', error.messages)

    payload['password'] = hashpw(password.encode('utf-8'), gensalt(12))
    payload['email'] = data['email'].lower()
    try:
        full_name, password, email = data['full_name'], data['password'], data['email']
        user = User(full_name=full_name, password=password, email=email)
        save_changes(user)

    except IntegrityError:
        return resp_already_exists('Users', "usuário")

    except Exception as e:
        return resp_exception('Users', description=e)

    schema = UserSchema()
    result = schema.dump(user)

    return resp_ok(
        'Users', MSG_RESOURCE_CREATED.format('Usuário'), data=result,
    )


def save_changes(data):
    db.session.add(data)
    db.session.commit()
