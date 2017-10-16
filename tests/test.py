from unittest import TestCase
import json
from bucketlist import create_app
from bucketlist.models import db

class BaseTestCase(TestCase):

    def setUp(self):

        self.app = create_app('test')
        self.client = self.app.test_client
        app_context = self.app.app_context()
        app_context.push()
        db.create_all()

    def register(self, name, email):

        response = self.client().post(
            '/auth/register',
            data=json.dumps({
                'name': name,
                'email': email,
                'password': 'password'
            }),
            content_type='application/json'
        )
        return response

    def login(self, email):
        response = self.client().post(
            '/auth/login',
            data=json.dumps({
                'email': email,
                'password': 'password'
            }),
            content_type='application/json'
        )
        return response

    def get_auth_token(self):
        self.register('John', 'john@example.com')
        login_response = self.login('john@example.com')
        data = json.loads(login_response.data.decode())
        return data['auth_token']

    def add_bucketlist(self, name):
        auth_token = self.get_auth_token()
        response = self.client().post(
            '/bucketlists/',
            data=json.dumps({
                'name': name
            }),
            headers={
                'Authorization': auth_token
            },
            content_type='application/json'
        )
        return response

    def retrieve_bucketlist(self, login=False, id=None):
        auth_token = ''
        if login:
            auth_token = self.get_auth_token()
        if id:
            request = '/bucketlists/{}'.format(id)
        else:
            request = '/bucketlists/'
        response = self.client().get(
            request,
            headers={
                'Authorization': auth_token,
            },
        )
        return response

    def update_bucketlist(self, id, name):
        auth_token = self.get_auth_token()
        request = '/bucketlists/{}'.format(id)
        response = self.client().put(
            request,
            data=json.dumps({
                'name': name,
            }),
            headers={
                'Authorization': auth_token
            },
            content_type='application/json'
        )
        return response

    def delete_bucketlist(self, login=False, id=None):
        auth_token = ''
        if login:
            auth_token = self.get_auth_token()
        request = '/bucketlists/{}'.format(id)
        response = self.client().delete(
            request,
            headers={
                'Authorization': auth_token
            },
            content_type='application/json'
        )
        return response

    def add_bucketlist_item(self, id, name):
        auth_token = self.get_auth_token()
        request = '/bucketlists/{}/items'.format(id)
        response = self.client().post(
            request,
            data = json.dumps({
                'name': name,
            }),
            headers = {
                'Authorization': auth_token
            },
            content_type='application/json'
        )
        return response

    def delete_bucketlist_item(self, id, item_id):
        auth_token = self.get_auth_token()
        request = '/bucketlists/{}/items/{}'.format(id, item_id)
        response = self.client().delete(
            request,
            headers = {
                'Authorization': auth_token
            },
            content_type='application/json'
        )
        return response

    def update_bucketlist_item(self, id, item_id, name):
        auth_token = self.get_auth_token()
        request = '/bucketlists/{}/items/{}'.format(id, item_id, name)
        response = self.client().put(
            request,
            headers = {
                'Authorization': auth_token
            },
            data= json.dumps({
                'name': name,
                'done' : False
            }),
            content_type = 'application/json'
        )
        return response

    def paginate(self, limit):
        auth_token = self.get_auth_token()
        request = '/bucketlists?limit={}'.format(limit)
        response = self.client().get(
            request,
            headers = {
                'Authorization' : auth_token
            }
        )
        return response

    def search(self):
        auth_token = self.get_auth_token()
        request = '/bucketlists/?q=search'
        response = self.client().get(
            request,
            headers = {
                'Authorization' : auth_token
            }
        )
        print(response.data)
        return response

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
