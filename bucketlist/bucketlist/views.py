from flask import request, abort
from flask_restplus import Resource
from bucketlist.models import User, BucketList, ListItem
from bucketlist.lib.serializers import api
from bucketlist.lib.tools import get_user, bucket_content
from bucketlist.lib.serializers import bucket_list_input,\
    bucket_item_input, bucket_list_items, bucket_list
from bucketlist.lib.parsers import paginate_or_search

ns = api.namespace('bucketlists', description='Bucketlist related operations')

@ns.route('/')
@api.doc(params={'q': 'search string'})
@api.doc(params={'limit': 'search limit'})
class BucketLists(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(404, 'bucketlist not found')
    @api.response(401, 'Unauthorised access')
    @api.marshal_list_with(bucket_list)
    def get(self):

        """Receives get request and returns all bucketlists
        that belong to logged in user"""

        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)
        if not isinstance(user, User):
            abort(401, user)

        args = paginate_or_search.parse_args(request)
        page = args.get('page', 1)
        limit = args.get('limit')
        q = args.get('q')
        if q:
            bucketlists = user.bucketlists.filter(
                BucketList.name.ilike('%'+q+'%'))\
                .paginate(page, limit, False)
        else:
            bucketlists = user.bucketlists.paginate(page, limit, False)

        if not bucketlists:
            abort(404)

        response = []
        for bucketlist in bucketlists.items:
            items = [item for item in bucketlist.items.all()]
            resp = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'items': items,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                'created_by': bucketlist.created_by
            }
            response.append(resp)
        return response, 200

    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(bucket_list)
    @api.response(401, 'Unauthorised access')
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
            items = [item for item in bucketlist.items.all()]
            response = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'items': items,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                'created_by': bucketlist.created_by
            }
            return response, 201

        else:
            abort(401, user)


@ns.route('/<int:id>')
class SingleBucketList(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(404, 'bucketlist doesnt exist')
    @api.response(401, 'Unauthorised access')
    @api.marshal_with(bucket_list)
    def get(self, id):

        """Receives get request with a bucketlist id and returns the
        bucketlist"""

        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404)

            return bucket_content(bucketlist), 200

        else:
            return user, 401

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(404, 'Bucketlist doesnt exist')
    @api.marshal_with(bucket_list)
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
                abort(404)
            bucketlist.modify_name(put_data['name'])
            bucketlist = user.bucketlists.filter_by(id=id).first()
            return bucket_content(bucketlist), 201

        else:
            return user, 401

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(401, 'Unauthorised access')
    @api.response(404, 'Bucketlist doesnt exist')
    def delete(self, id):

        """Receives a delete request with a bucketlist id and
        deletes the bucketlist. Returns message is succesful"""
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404)
            bucketlist.delete()

            response = {
                'status': 'success',
                'message': 'Successfully deleted.',
                'id': bucketlist.id,
            }
            return response, 410

        else:
            abort(401, user)

@ns.route('/<int:id>/items')
class BucketListItem(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(bucket_list_items)
    @api.response(404, 'Bucketlist doesnt exist')
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
                abort(404)
            list_item = ListItem(name=post_data.get('name'), bcktlst=bucketlist)
            list_item.save()

            return list_item, 201

        else:
            return user, 401

@ns.route('/<int:id>/items/<item_id>')
class BucketListItems(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(bucket_list_items)
    @api.response(401, 'Unauthorised access')
    @api.response(404, 'Bucketlist or item doesnt exist')
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
                abort(404, "Bucketlist doesnt exist")
            item = bucketlist.items.filter_by(id=item_id).first()
            if not item:
                abort(404, "Item doesnt exist")

            if put_data['name']:
                item.modify_name(put_data['name'])
            if put_data['done']:
                item.complete_activity()
            item = bucketlist.items.filter_by(id=item_id).first()
            return item, 201
        else:
            abort(401, user)

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(401, 'Unauthorised access')
    @api.response(404, 'Bucketlist or Item doesnt exist')
    def delete(self, id, item_id):

        """Recieves delete request with bucketlist id and bucket item
        id. Deletes the item."""

        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404, "Bucketlist doesnt exist")
            item = bucketlist.items.filter_by(id=item_id).first()
            if not item:
                abort(404, "Item doesnt exist")
            item.delete()

            response_obj = {
                'status': 'success',
                'message': 'Successfully deleted.',
            }
            return response_obj, 410

        else:
            abort(401, user)
