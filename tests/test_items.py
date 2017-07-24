from . test import BaseTestCase
from bucketlist.models import ListItem
import json


class TestCase(BaseTestCase):

    def test_item_is_added(self):
        self.add_bucketlist("Bucketlist1")
        response = self.add_bucketlist_item(1, "Run a marathon.")
        data = json.loads(response.data.decode())
        list_items = ListItem.query.all()
        self.assertEqual(len(list_items), 1)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['bucketlist_id'], 1)
        self.assertEqual(data['name'], "Run a marathon.")
        self.assertEqual(data['message'], "Item added successfully")

    def test_item_is_deleted(self):
        self.add_bucketlist("Bucketlist1")
        self.add_bucketlist_item(1, "Run a marathon")
        self.add_bucketlist_item(1, "Ride a horse")
        response = self.delete_bucketlist_item(id=1, item_id=1)
        data = json.loads(response.data.decode())
        list_items = ListItem.query.all()
        self.assertEqual(len(list_items), 1)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], "Successfully deleted." )

    def test_item_is_updated(self):
        self.add_bucketlist("Bucketlist1")
        self.add_bucketlist_item(1, "Run a marathon")
        response = self.update_bucketlist_item(id=1, item_id=1, name="Sky dive")
        data = json.loads(response.data.decode())
        self.assertEqual(data['name'], "Sky dive")
        self.assertNotEqual(data['date_modified'], data['date_created'])
