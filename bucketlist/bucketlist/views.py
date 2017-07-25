from flask import request, jsonify
from flask_restplus import Resource
from bucketlist.models import User, BucketList, ListItem
from bucketlist.lib.serializers import api
from bucketlist.lib.tools import get_user, bucketlist_data,\
    doesnt_exist, item_data
from bucketlist.lib.serializers import bucket_list_input,\
    bucket_item_input

ns = api.namespace('bucketlists', description='Bucketlist related operations')

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
    @api.expect(bucket_list_input)
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
    @api.expect(bucket_list_input)
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
    @api.expect(bucket_item_input)
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
    @api.expect(bucket_item_input)
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

            if put_data['name']:
                item.modify_name(put_data['name'])
            if put_data['done']:
                item.complete_activity()
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
