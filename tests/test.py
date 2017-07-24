from unittest import TestCase
import json
from bucketlist.views import create_app
from bucketlist.models import db, User
from config import config


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

    def add_bucketlist(self, name):
        self.register('John', 'john@example.com')
        login_response = self.login('john@example.com')
        data = json.loads(login_response.data.decode())
        auth_token = data['auth_token']
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
        self.register('John', 'john@example.com')
        auth_token = ''
        if login:
            login_response = self.login('john@example.com')
            data = json.loads(login_response.data.decode())
            auth_token = data['auth_token']
        if id:
            request = '/bucketlists/{}'.format(id)
        else:
            request = '/bucketlists/'
        response = self.client().get(
            request,
            headers={
                'Authorization': auth_token
            },
            content_type='application/json'
        )
        return response

    def update_bucketlist(self, id, name):
        self.register('John', 'john@example.com')
        login_response = self.login('john@example.com')
        data = json.loads(login_response.data.decode())
        auth_token = data['auth_token']
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
        self.register('John', 'john@example.com')
        auth_token = ''
        if login:
            login_response = self.login('john@example.com')
            data = json.loads(login_response.data.decode())
            auth_token = data['auth_token']
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
        self.register('John', 'john@example.com')
        login_response = self.login('john@example.com')
        data = json.loads(login_response.data.decode())
        auth_token = data['auth_token']
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
        self.register('John', 'john@example.com')
        login_response = self.login('john@example.com')
        data = json.loads(login_response.data.decode())
        auth_token = data['auth_token']
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
        self.register('John', 'john@example.com')
        login_response = self.login('john@example.com')
        data = json.loads(login_response.data.decode())
        auth_token = data['auth_token']
        request = '/bucketlists/{}/items/{}'.format(id, item_id, name)
        response = self.client().put(
            request,
            headers = {
                'Authorization': auth_token
            },
            data= json.dumps({
                'name': name
            }),
            content_type = 'application/json'
        )
        return response

    def tearDown(self):
        db.session.close()
        db.drop_all()
