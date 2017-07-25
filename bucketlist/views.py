from flask import request, jsonify
from flask import Flask
from flask_restplus import Api, Resource
from config import config
from bucketlist.models import db, User, BucketList, ListItem

def create_app(config_name):
    from .lib.tools import get_user, bucketlist_data,\
        doesnt_exist, item_data

    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @api.route('/auth/register')
    class Register(Resource):

        """Registers a user"""

        @api.expect('name', required=True)
        @api.expect('email', required=True)
        @api.expect('password', required=True)
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

    @api.route('/auth/login')
    class Login(Resource):

        """Logs in a user"""

        @api.expect('email', required=True)
        @api.expect('password', required=True)
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

    @api.route('/bucketlists/')
    class BucketLists(Resource):

        @api.header('Authorization', 'JWT Token', required=True)
        def get(self):

            """Receives get request and returns all bucketlists
            that belong to logged in user"""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                bucketlists = user.bucketlists.all()
                bukt = BucketList.query.all()
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
        @api.expect('name', required=True)
        def post(self):

            """Receives post request with bucketlist name and
            adds a bucketlist with given name. Returns the added
            bucketlist"""

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

            """Receives get request with a bucketlist id and returns the
            bucketlist"""

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
        @api.expect('name', required=True)
        def put(self, id):

            """Receives a put request with bucketlist id, updates the
            bucketlist and returns the bucketlist."""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                put_data = request.get_json()
                bucketlist = user.bucketlists.filter_by(id=id).first()

                if not bucketlist:
                    return doesnt_exist("BucketList"), 404
                bucketlist.modify_name(put_data['name'])
                bucketlist = user.bucketlists.filter_by(id=id).first()
                return jsonify(bucketlist_data(bucketlist))

            else:
                return user, 404

        @api.header('Authorization', 'JWT Token', required=True)
        def delete(self, id):

            """Receives a delete request with a bucketlist id and
            deletes the bucketlist. Returns message is succesful"""
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
        @api.expect('name', required=True)
        def post(self, id):

            """Receives post request with bucketlist id and item name.
            Adds a bucketlist item and returns it."""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                post_data = request.get_json()
                bucketlist = user.bucketlists.filter_by(id=id).first()
                if not bucketlist:
                    return doesnt_exist("BucketList"), 404
                list_item = ListItem(name=post_data.get('name'), bcktlst=bucketlist)
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
        def put(self, id, item_id):

            """Receives put request with id, item id and item name.
            Modifies the item and returns it."""

            auth_token = request.headers.get("Authorization")
            user = get_user(auth_token)

            if isinstance(user, User):
                put_data = request.get_json()
                bucketlist = user.bucketlists.filter_by(id=id).first()
                if not bucketlist:
                    return doesnt_exist("BucketList"), 404
                item = bucketlist.items.filter_by(id=item_id).first()
                if not item:
                    return doesnt_exist("Item"), 404
                item.modify_name(put_data['name'])
                item = bucketlist.items.filter_by(id=item_id).first()
                return jsonify(item_data(item))


        @api.header('Authorization', 'JWT Token', required=True)
        def delete(self, id, item_id):

            """Recieves delete request with bucketlist id and bucket item
            id. Deletes the item."""

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
                }
                return jsonify(response_obj)

            else:
                return user

    return app
