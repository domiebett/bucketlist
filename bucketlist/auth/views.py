from flask import request, jsonify
from flask import Flask
from flask_restplus import Api, Resource
from bucketlist.models import User
from bucketlist.lib.serializers import api
from bucketlist.lib.serializers import registration_input,\
    log_in_input

ns = api.namespace('auth', description='Operations related to user authentication')

@ns.route('/register')
class Register(Resource):

    """Registers a user"""

    @api.expect(registration_input)
    def post(self):

        """Receives post request with name, password and email, registers user
        and returns auth_token"""

        post_data = request.get_json()
        if not post_data.get('email'):
            return jsonify({
                'status': 'fail',
                'message': 'Please enter an email to proceed'
            })

        user = User.query.filter_by(email=post_data.get('email')).first()
        if user:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return jsonify(response)

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

@ns.route('/login')
class Login(Resource):

    """Logs in a user"""

    @api.expect(log_in_input)
    def post(self):

        """Receives email, password and logs returns auth_token
        for user to login to program with."""

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
