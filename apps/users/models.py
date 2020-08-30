from flask_user import UserMixin
from sqlalchemy_utils import EmailType

from apps.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(
        'is_active', db.Boolean(), nullable=False, server_default='1')

    password = db.Column(db.String(255), nullable=False, server_default='')
    email = db.Column(EmailType, unique=True, nullable=False)
    email_confirmed_at = db.Column(db.DateTime())
    full_name = db.Column(db.String(255), nullable=False, server_default='')

    def __repr__(self):
        return '<User %r>' % self.email
