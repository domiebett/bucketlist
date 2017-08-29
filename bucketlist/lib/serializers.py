from flask_restplus import fields
from bucketlist import api

registration_input = api.model('Registration', {
    'name' : fields.String(required=True, description="User Name"),
    'email' : fields.String(required=True, description="User Email"),
    'password' : fields.String(required=True, description="User password"),
})

log_in_input = api.model('Login', {
    'email' : fields.String(required=True, description="User Name"),
    'password' : fields.String(required=True, description="User Password")
})

bucket_list_input = api.model('bucket-edit', {
    'name' : fields.String(required=True, description="Name of bucketlist")
})

bucket_item_input = api.model('edit-edit', {
    'name': fields.String(required=True, description='name of bucket list item'),
    'done': fields.Boolean(required=True, description='status of the bucketlist item'),
})

bucket_list_items = api.model('bucket_list_items',{
    'id': fields.Integer(readOnly=True, description='identifier for bucketlist item'),
    'name': fields.String(required=True, description='name for bucketlist item'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean(required=True, description='status of bucketlist item'),
})

bucket_list = api.model('bucketlist', {
    'id': fields.Integer(readOnly=True,
                         description='identifier for the bucketlis'),
    'name': fields.String(required=True, description='name of the bucket lis'),
    'items': fields.List(fields.Nested(bucket_list_items),
                         description='Bucketlist items'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(required=True,
                                description='user email for the bucketlist owner')
})

links = api.model('links', {
    'text': fields.String(readOnly=True,
                        description="Previous button"),
    'id': fields.String(readOnly=True,
                          description="Next button")
})

bucket_lists = api.model('bucketlists', {
    'bucketlists': fields.List(fields.Nested(bucket_list),
                              description='All Bucketlists'),
    'links': fields.List(fields.Nested(links))
})