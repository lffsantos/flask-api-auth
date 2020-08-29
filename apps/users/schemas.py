from marshmallow import Schema, EXCLUDE
from marshmallow.fields import Email, Str, Boolean, DateTime

from apps.messages import MSG_FIELD_REQUIRED


class UserRegistrationSchema(Schema):
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    password = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )

    class Meta:
        unknown = EXCLUDE


class UserSchema(Schema):
    id = Str()
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    active = Boolean()
    password = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email_confirmed_at = DateTime()
