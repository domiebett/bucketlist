from flask import request, jsonify
from flask_restplus import Resource
from bucketlist.models import User
from bucketlist.lib.serializers import api
from bucketlist.lib.tools import invalid_email, get_user
from bucketlist.lib.serializers import registration_input,\
    log_in_input

ns = api.namespace('auth', description='Operations related to user authentication')

@ns.route('/register')
class Register(Resource):

    """Registers a user"""

    @api.expect(registration_input)
    def post(self):

        """Receives post request and registers user."""
        try:
            # Retrieve emai, name and password
            post_data = request.get_json()
            if not post_data.get('email'):

                return jsonify({
                    'status': 'fail',
                    'message': 'Please enter an email to proceed'
                })

            # Validate email
            if invalid_email(post_data.get('email')):
                return jsonify({
                    'status': 'fail',
                    'message': 'Please enter a valid email'
                })

            # Check if user already exists.
            user = User.query.filter_by(email=post_data.get('email')).first()
            if user:
                response = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return jsonify(response)

            # Add user with the details to the db.
            name = post_data.get('name')
            email = post_data.get('email')
            password = post_data.get('password')
            user = User(name, email, password)
            user.save()

            # Generate an auth_token and return it in response.
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

@ns.route('/login')
class Login(Resource):

    """Logs in a user"""

    @api.expect(log_in_input)
    def post(self):

        """Receives email, password and logs returns auth_token
        for user to login to program with."""

        post_data = request.get_json()

        try:
            # Search for user with email.
            email = post_data.get('email')
            password = post_data.get('password')
            user = User.query.filter_by(
                email=email).first()

            # Validate that user exists and password is correct.
            if user and user.is_correct_password(password):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode(),
                        'user': user.username

                    }
                    return jsonify(responseObject)
            else:
                return jsonify({
                    'status': 'fail',
                    "message": "Invalid email or password. Please"
                               " confirm the data entered and try again"
                })
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'There was an error with your login.'
                           'Please check that all fields are correct'
            }
            return jsonify(responseObject)

@ns.route('/test_login')
class TestLogin(Resource):
    def get(self):
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)
        if isinstance(user, User):
            response_obj = {
                'status': 'success',
                'message': 'User is logged in',
            }
            return response_obj, 200

        else:
            response_obj = {
                'status': 'fail',
                'message': 'user is not logged in'
            }
            return response_obj, 401

