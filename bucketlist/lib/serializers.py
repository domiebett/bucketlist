from bucketlist import jsonify
from flask_restplus import fields
from bucketlist import api

registration_input = api.models('Registration', {
    'name' : fields.String(required=True, description="User Name"),
    'email' : fields.String(required=True, description="User Email"),
    'password' : fields.String(required=True, description="User password"),
})

log_in_input = api.models('Login', {
    'email' : fields.String(required=True, description="User Name"),
    'password' : fields.String(required=True, description="User Password")
})

bucket_list_input = api.models('Login', {
    'name' : fields.String(required=True, description="User Name")
})

bucket_item_input = api.model('edit', {
    'name': fields.String(required=True, description='name of bucketlist or bucket item'),
    'done': fields.Boolean(required=True, description='status of the bucketlist item'),
})

bucket_list_items = api.model('BucketListItem', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of an item'),
    'name': fields.String(required=True, description='item name'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.String(required=True, description='status of the item'),
})

bucket_list = api.model('Bucketlists', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a bucketlist'),
    'name': fields.String(required=True, description='Bucketlist name'),
    'items': fields.List(fields.Nested(bucket_list_items),
                         description='Bucketlist items'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(required=True, description='Bucketlist owner'),
})

bucket_item = api.model('item', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of an item'),
    'name': fields.String(required=True, description='item name'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.String(required=True, description='status of the item'),
})

