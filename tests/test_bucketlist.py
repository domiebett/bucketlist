from . test import BaseTestCase, db
from bucketlist.models import BucketList
import json


class TestCase(BaseTestCase):

    def test_add_bucketlist(self):
        response = self.add_bucketlist('Bucketlist')
        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Bucketlist')
        bucketlists = BucketList.query.all()
        self.assertEqual(bucketlists[0].name, 'Bucketlist')

    def test_get_bucketlists(self):
        self.add_bucketlist('Bucketlist')
        response = self.retrieve_bucketlist(login=True)
        data = json.loads(response.data.decode())
        self.assertEqual(data[0]['name'], 'Bucketlist')
        self.assertEqual(data[0]['id'], 1)
        self.assertListEqual(data[0]['items'], [])
        self.assertEqual(data[0]['created_by'], 'john@example.com')
        self.assertTrue(data[0]['date_modified'])
        self.assertTrue(data[0]['date_created'])

    def test_login_is_required(self):
        response = self.retrieve_bucketlist()
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'],
                         'Provide a valid auth token.')
