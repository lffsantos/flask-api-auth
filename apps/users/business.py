from bcrypt import hashpw, gensalt
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from apps import db
from apps.messages import MSG_NO_DATA, MSG_RESOURCE_CREATED
from apps.responses import resp_data_invalid, resp_exception, resp_ok, resp_already_exists
from apps.users.models import User
from apps.users.schemas import UserSchema, UserRegistrationSchema


def save_new_user(payload):
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


def get_a_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    users_schema = UserSchema()
    return users_schema.dump(user)


def update_user(data, user_id):
    pass


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return None, 204
