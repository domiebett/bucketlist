from flask import request, jsonify
from flask import Flask
from flask_restplus import Api, Resource
from config import config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name):
    from .models import User, BucketList, ListItem

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
        def get(self):

            """Return all bucketlists in the system."""
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            if auth_token:
                user_id = User.decode_auth_token(auth_token)
                if not isinstance(user_id, str):
                    response_obj = []
                    user = User.query.filter_by(id=user_id).first()
                    bucketlists = user.bucketlists.all()

                    for bucketlist in bucketlists:
                        itemscontent = [{'id': item.id,
                                         'name': item.name,
                                         'date_created': item.date_created,
                                         'date_modified': item.date_modified,
                                         'done': False, }
                                        for item in bucketlist.items.all()]
                        resp = {
                            'id' : bucketlist.id,
                            'name' : bucketlist.name,
                            'items' : itemscontent,
                            'date_created' : bucketlist.date_created,
                            'date_modified' : bucketlist.date_modified,
                            'created_by' : bucketlist.created_by
                        }
                        response_obj.append(resp)
                    return jsonify(response_obj)

                response_obj = {
                    'status': 'fail',
                    'message': user_id
                }
                return jsonify(response_obj)
            else:
                response_obj = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return jsonify(response_obj)

        def post(self):

            """Adds a bucketlist."""

            auth_header = request.headers.get("Authorization")
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ""

            if auth_token:
                user_id = User.decode_auth_token(auth_token)
                if not isinstance(user_id, str):
                    post_data = request.get_json()
                    user = User.query.filter_by(id=user_id).first()
                    bucketlist = BucketList(name=post_data.get('name'), owner=user,
                                            created_by=user.email)
                    bucketlist.save()

                    response_obj = []
                    bucketlists = user.bucketlists.all()
                    for bucketlist in bucketlists:
                        itemscontent = [{'id': item.id,
                                         'name': item.name,
                                         'date_created': item.date_created,
                                         'date_modified': item.date_modified,
                                         'done': False, }
                                        for item in bucketlist.items.all()]
                        resp = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'items': itemscontent,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                        }
                        response_obj.append(resp)
                    return jsonify(response_obj)
                response_obj = {
                    'status': 'fail',
                    'message': user_id
                }
                return jsonify(response_obj)
            else:
                response_obj = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return jsonify(response_obj)


    @api.route('/bucketlists/<id>')
    class SingleBucketList(Resource):

        def get(self, id):

            """Returns a single bucket list with the id"""

            auth_header = request.headers.get('Authorization')

            if auth_header:
                auth_token = auth_header.split(" ")[1]

            else:
                auth_token = ''

            if auth_token:
                user_id = User.decode_auth_token(auth_token)

                if not isinstance(user_id, str):
                    user = User.query.filter_by(id=user_id).first()
                    bucketlist = user.bucketlists.filter_by(id=id).first()
                    itemscontent = [{'id':item.id,
                                     'name':item.name,
                                     'date_created':item.date_created,
                                     'date_modified':item.date_modified,
                                     'done': False,}
                                    for item in bucketlist.items.all()]

                    response_obj = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'items': itemscontent,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }

                    return jsonify(response_obj)

                response_obj = {
                    'status': 'fail',
                    'message': user_id
                }

                return jsonify(response_obj)
            else:
                response_obj = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return jsonify(response_obj)

        def delete(self, id):

            """Deletes bucketlist with the primary key of 'id'."""
            auth_header = request.headers.get('Authorization')

            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''

            if auth_token:
                user_id = User.decode_auth_token(auth_token)

                if not isinstance(user_id, str):
                    user = User.query.filter_by(id=user_id).first()
                    bucketlist = user.bucketlists.filter_by(id=id).first()
                    bucketlist.delete()

                    response_obj = {
                        'status': 'success',
                        'message': 'Successfully deleted.',
                        'id': bucketlist.id,
                    }
                    return jsonify(response_obj)

                response_obj = {
                    'status': 'fail',
                    'message': user_id
                }
                return jsonify(response_obj)

            else:
                response_obj = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return jsonify(response_obj)

    @api.route('/bucketlists/<id>/items')
    class BucketListItem(Resource):

        def post(self, id):

            """Adds item to bucketlist with the id"""

            auth_header = request.headers.get("Authorization")
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ""

            if auth_token:
                user_id = User.decode_auth_token(auth_token)

                if not isinstance(user_id, str):
                    post_data = request.get_json()
                    user = User.query.filter_by(id=user_id).first()
                    bucketlist = user.bucketlists.filter_by(id=id).first()
                    list_item = ListItem(name=post_data.get('content'), bcktlst=bucketlist)
                    list_item.save()

                    response_obj = {
                        'status': 'success',
                        'name': list_item.name,
                        'bucketlist_id': bucketlist.id,
                        'message': 'Item added successfully'
                    }
                    return jsonify(response_obj)

                response_obj = {
                    'status': 'fail',
                    'message': user_id
                }
                return jsonify(response_obj)

            else:
                response_obj = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return jsonify(response_obj)

    @api.route('/bucketlists/<id>/items/<item_id>')
    class BucketListItems(Resource):

        def delete(self, id, item_id):

            """Deletes items from bucketlists with id as item id."""

            auth_header = request.headers.get('Authorization')

            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''

            if auth_token:
                user_id = User.decode_auth_token(auth_token)

                if not isinstance(user_id, str):
                    user = User.query.filter_by(id=user_id).first()
                    bucketlist = user.bucketlists.filter_by(id=id).first()
                    item = bucketlist.items.filter_by(id=item_id).first()
                    item.delete()

                    response_obj = {
                        'status': 'success',
                        'message': 'Successfully deleted.',
                        'bucketlist_id': bucketlist.id,
                        'id': item.id,
                    }
                    return jsonify(response_obj)

                response_obj = {
                    'status': 'fail',
                    'message': user_id
                }
                return jsonify(response_obj)

            else:
                response_obj = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return jsonify(response_obj)

    return app
