from flask import request, jsonify
from flask import Flask
from flask_restplus import Api, Resource
from config import config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name):
    from .models import User, BucketList

    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @api.route('/auth/register')
    class Register(Resource):
        """
        User Registration Resource
        """

        def post(self):

            post_data = request.get_json()
            if not post_data.get('email'):
                return jsonify({'status': 'fail',
                                'message': 'Please enter an email to proceed'})
            user = User.query.filter_by(email=post_data.get('email')).first()
            if not user:
                try:
                    name = post_data.get('username')
                    email = post_data.get('email')
                    password = post_data.get('password')
                    user = User(name, email, password)
                    user.save()

                    auth_token = user.encode_auth_token(user.id)
                    response = {
                        'status': 'success',
                        'message': 'Successfully registered.',
                        'auth_token': auth_token.decode()
                    }
                    return jsonify(response)
                except Exception as e:
                    response = {
                        'status': 'fail',
                        'message': 'Some error occurred. Please try again.'
                    }
                    return jsonify(response)
            else:
                response = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return jsonify(response)

    @api.route('/auth/login')
    class Login(Resource):
        """
        User Login Resource
        """
        def post(self):
            # get the post data
            post_data = request.get_json()
            try:
                email = post_data.get('email')
                password = post_data.get('password')
                user = User.query.filter_by(
                    email=email).first()
                if user and user.is_correct_password(password):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode()
                        }
                        return jsonify(responseObject)
                else:
                    return jsonify({
                        'status': 'fail',
                        "message": "Access Denied. Login Again"
                    })
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Try again'
                }
                return jsonify(responseObject)
