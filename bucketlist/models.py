import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), index=True, default="Unknown")
    email = db.Column(db.String(50), index=True, unique=True)
    _password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    bucketlists = db.relationship('BucketList', backref='owner', lazy='dynamic',
                                  cascade='all, delete-orphan')

    # Initialise User model.
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self._set_password(password)

    def __repr__(self):
        return "<User {}".format(self.email)

    def _set_password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BucketList(db.Model):

    __tablename__ = "bucketlist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), default="My BucketList")
    created_by = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('ListItem', backref='bcktlst', lazy='dynamic',
                            cascade='all, delete-orphan')

    def modify_name(self, name):
        self.name = name
        self.date_modified = datetime.datetime.utcnow()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ListItem(db.Model):

    __tablename__ = "listitem"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    date_created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    done = db.Column(db.Boolean(), default=False)
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def modify_name(self, name):
        self.name = name
        self.date_modified = datetime.datetime.utcnow()
        self.save()

    def complete_activity(self):
        self.done = True
        self.modified = datetime.datetime.utcnow()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
