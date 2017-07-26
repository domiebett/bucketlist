from tests.test import BaseTestCase
import json

class TestRegister(BaseTestCase):

    def test_register_works(self):
        response = self.register("John", "john@example.com")
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')

    def test_duplicate_registration(self):
        self.register("John", "john@example.com")
        response = self.register("John", "john@example.com")
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'],
                        'User already exists. Please Log in.')
        self.assertTrue(response.content_type == 'application/json')

    def test_login_succesful(self):
        self.register("John", "john@example.com")
        response = self.login('john@example.com')
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'],
                         'Successfully logged in.')
        self.assertTrue(data['auth_token'])

    def test_unregistered_login(self):
        response = self.login("randy@example.com")
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'],
                         'Access Denied. Login Again')
