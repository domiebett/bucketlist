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
                'Authorization': 'Bearer {}'.format(auth_token)
            },
            content_type='application/json'
        )
        return response

    def retrieve_bucketlist(self, login=False):
        self.register('John', 'john@example.com')
        auth_token = ''
        if login:
            login_response = self.login('john@example.com')
            data = json.loads(login_response.data.decode())
            auth_token = data['auth_token']
        response = self.client().get(
            '/bucketlists/',
            headers={
                'Authorization': 'Bearer {}'.format(auth_token)
            },
            content_type='application/json'
        )
        return response

    def tearDown(self):
        db.session.close()
        db.drop_all()
