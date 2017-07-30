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

    """Retrieves and adds bucketlists."""

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(404, 'bucketlist not found')
    @api.response(401, 'Unauthorised access')
    @api.marshal_list_with(bucket_list)
    def get(self):

        """Receives get request and returns all bucketlists"""

        # Gets authtoken to retrieve user if token is valid.
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)
        if not isinstance(user, User):
            abort(401, user)

        # Retrieves paginate, page or search arguments.
        args = paginate_or_search.parse_args(request)
        page = args.get('page', 1)
        limit = args.get('limit')
        q = args.get('q')

        # Returns paginated or paginated search results
        if q:
            bucketlists = user.bucketlists.filter(
                BucketList.name.ilike('%'+q+'%'))\
                .paginate(page, limit, False)
        else:
            bucketlists = user.bucketlists.paginate(page, limit, False)

        # 404 error if bucketlists dont exist for user
        if not bucketlists:
            abort(404)

        # returns a response with all bucketlists.
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

        """Receives post request and adds a bucketlist."""

        # Gets authtoken to retrieve user if token is valid.
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):

            # Fetches bucketlist name from request, and creates it.
            post_data = request.get_json()
            bucketlist = BucketList(name=post_data.get('name'), owner=user,
                                    created_by=user.email)
            bucketlist.save()

            #return single bucketlist made.
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

    """Operations dealing with manipulating single bucketlist."""

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(404, 'bucketlist doesnt exist')
    @api.response(401, 'Unauthorised access')
    @api.marshal_with(bucket_list)
    def get(self, id):

        """Receives get request and returns the single bucketlist"""

        # Get token and decode it to return user
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):

            # Return response with single bucketlist.
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

        """Receives a put request, updates the bucketlist"""

        # Decodes token to retrieve user.
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):

            # Retrieve bucketlist with the id.
            put_data = request.get_json()
            bucketlist = user.bucketlists.filter_by(id=id).first()

            if not bucketlist:
                abort(404)

            # Modify bucketlist name.
            bucketlist.modify_name(put_data['name'])
            bucketlist = user.bucketlists.filter_by(id=id).first()
            return bucket_content(bucketlist), 201

        else:
            return user, 401

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(401, 'Unauthorised access')
    @api.response(404, 'Bucketlist doesnt exist')
    def delete(self, id):

        """Receives a delete request and deletes a bucketlist."""

        # Decode auth_token to retrieve user.
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):

            # Retrieve bucketlist and delete it.
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404)
            bucketlist.delete()

            # Return success message.
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

    """Deal with addition of bucketlist item"""

    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(bucket_list_items)
    @api.response(404, 'Bucketlist doesnt exist')
    @api.expect(bucket_item_input)
    def post(self, id):

        """Receives post request adds a bucketlist item."""

        # Decode auth_token to get user.
        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):

            # Retrieve item name from request and create item.
            post_data = request.get_json()
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404)
            list_item = ListItem(name=post_data.get('name'),
                                 bcktlst=bucketlist)
            list_item.save()

            # Return the item created.
            return list_item, 201

        else:
            return user, 401

@ns.route('/<int:id>/items/<item_id>')
class BucketListItems(Resource):

    """Operations for manipulating single bucketlist items."""
    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(bucket_list_items)
    @api.response(401, 'Unauthorised access')
    @api.response(404, 'Bucketlist or item doesnt exist')
    @api.expect(bucket_item_input)
    def put(self, id, item_id):

        """Receives put request and modifies the item."""

        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):
            put_data = request.get_json()
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404, "Bucketlist doesnt exist")

            # Get bucketlist item to modify.
            item = bucketlist.items.filter_by(id=item_id).first()
            if not item:
                abort(404, "Item doesnt exist")

            # Modify bucketlist item.
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

        """Recieves delete request and deletes a bucketlist item."""

        auth_token = request.headers.get("Authorization")
        user = get_user(auth_token)

        if isinstance(user, User):

            # Retrieve bucketlist item and deletes it.
            bucketlist = user.bucketlists.filter_by(id=id).first()
            if not bucketlist:
                abort(404, "Bucketlist doesnt exist")
            item = bucketlist.items.filter_by(id=item_id).first()
            if not item:
                abort(404, "Item doesnt exist")
            item.delete()

            # Return success message.
            response_obj = {
                'status': 'success',
                'message': 'Successfully deleted.',
            }
            return response_obj, 410

        else:
            abort(401, user)
