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

bucket_list_input = api.model('Login', {
    'name' : fields.String(required=True, description="User Name")
})

bucket_item_input = api.model('edit', {
    'name': fields.String(required=True, description='name of bucketlist or bucket item'),
    'done': fields.Boolean(required=True, description='status of the bucketlist item'),
})
