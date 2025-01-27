from marshmallow import Schema, EXCLUDE
from marshmallow.fields import Email, Str

from apps.messages import MSG_FIELD_REQUIRED


class LoginSchema(Schema):
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    password = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )

    class Meta:
        unknown = EXCLUDE
