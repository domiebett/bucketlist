from flask import request, jsonify
from flask import Flask
from flask_restplus import Api, Resource
from config import config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name):
    from .models import User, BucketList, ListItem
    from .tools.tools import get_user, bucketlist_data,\
        doesnt_exist

    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @api.route('/auth/register')
    class Register(Resource):

        """Registers a user"""

        def post(self):

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

    @api.route('/auth/login')
    class Login(Resource):

        """Logs in a user"""

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

    @api.route('/bucketlists/')
    class BucketLists(Resource):

        @api.header('Authorization', 'JWT Token', required=True)
        def get(self):

            """Return all bucketlists in the system."""
            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                bucketlists = user.bucketlists.all()
                if not bucketlists:
                    return {
                        'message': 'User has no bucketlists',
                    }
                response_obj = []
                for bucketlist in bucketlists:
                    resp = bucketlist_data(bucketlist)
                    response_obj.append(resp)
                return jsonify(response_obj)

            else:
                return user, 404

        @api.header('Authorization', 'JWT Token', required=True)
        def post(self):

            """Adds a bucketlist."""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                post_data = request.get_json()
                bucketlist = BucketList(name=post_data.get('name'), owner=user,
                                        created_by=user.email)
                bucketlist.save()

                response_obj = []
                bucketlists = user.bucketlists.all()
                for bucketlist in bucketlists:
                    resp = bucketlist_data(bucketlist)
                    response_obj.append(resp)
                return jsonify(response_obj)

            else:
                return user, 404

    @api.route('/bucketlists/<id>')
    class SingleBucketList(Resource):

        @api.header('Authorization', 'JWT Token', required=True)
        def get(self, id):

            """Returns a single bucket list with the id"""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                bucketlist = user.bucketlists.filter_by(id=id).first()
                if not bucketlist:
                    return doesnt_exist("BucketList"), 404
                response_obj = bucketlist_data(bucketlist)
                return jsonify(response_obj)
            else:
                return user, 404

        @api.header('Authorization', 'JWT Token', required=True)
        def delete(self, id):

            """Deletes bucketlist with the primary key of 'id'."""
            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                bucketlist = user.bucketlists.filter_by(id=id).first()
                if not bucketlist:
                    doesnt_exist("BucketList"), 404
                bucketlist.delete()

                response_obj = {
                    'status': 'success',
                    'message': 'Successfully deleted.',
                    'id': bucketlist.id,
                }
                return jsonify(response_obj)

            else:
                return user, 404

    @api.route('/bucketlists/<id>/items')
    class BucketListItem(Resource):

        @api.header('Authorization', 'JWT Token', required=True)
        def post(self, id):

            """Adds item to bucketlist with the id"""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                post_data = request.get_json()
                bucketlist = user.bucketlists.filter_by(id=id).first()
                if not bucketlist:
                    return doesnt_exist("BucketList"), 404
                list_item = ListItem(name=post_data.get('content'), bcktlst=bucketlist)
                list_item.save()

                response_obj = {
                    'status': 'success',
                    'name': list_item.name,
                    'bucketlist_id': bucketlist.id,
                    'message': 'Item added successfully'
                }
                return jsonify(response_obj)

            else:
                return user

    @api.route('/bucketlists/<id>/items/<item_id>')
    class BucketListItems(Resource):

        @api.header('Authorization', 'JWT Token', required=True)
        def delete(self, id, item_id):

            """Deletes items from bucketlists with id as item id."""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                bucketlist = user.bucketlists.filter_by(id=id).first()
                if not bucketlist:
                    return doesnt_exist("BucketList"), 404
                item = bucketlist.items.filter_by(id=item_id).first()
                if not item:
                    return doesnt_exist("Item"), 404
                item.delete()

                response_obj = {
                    'status': 'success',
                    'message': 'Successfully deleted.',
                }, 200
                return jsonify(response_obj)

            else:
                return user

    return app
