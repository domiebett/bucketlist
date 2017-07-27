from . test import BaseTestCase, db
from bucketlist.models import BucketList
import json


class TestCase(BaseTestCase):

    def test_add_bucketlist(self):
        response = self.add_bucketlist('Bucketlist')
        bucketlists = BucketList.query.all()
        self.assertEqual(bucketlists[0].name, 'Bucketlist')
        self.assertIn('Bucketlist', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_get_all_bucketlists(self):
        self.add_bucketlist('Bucketlist')
        response = self.retrieve_bucketlist(login=True)
        self.assertIn('Bucketlist', str(response.data))
        self.assertIn('john@example.com', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_get_single_bucketlist(self):
        self.add_bucketlist('Bucketlist1')
        self.add_bucketlist('Bucketlist2')
        response = self.retrieve_bucketlist(login=True, id=2)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucketlist2', str(response.data))

    def test_update_bucketlist(self):
        self.add_bucketlist('Bucketlist1')
        response = self.update_bucketlist(1, "Modified Name")
        self.assertIn('Modified Name', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_delete_bucketlist(self):
        self.add_bucketlist('Bucketlist1')
        self.add_bucketlist('Bucketlist2')
        self.add_bucketlist('Bucketlist3')
        response = self.delete_bucketlist(login=True, id=2)
        bucketlists = BucketList.query.all()
        self.assertEqual(len(bucketlists), 2)
        self.assertIn('Successfully deleted.', str(response.data))
        self.assertEqual(response.status_code, 410)

    def test_login_is_required(self):
        response = self.retrieve_bucketlist()
        self.assertIn('Provide a valid auth token', str(response.data))
        self.assertEqual(response.status_code, 401)
