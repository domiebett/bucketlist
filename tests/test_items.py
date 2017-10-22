from . test import BaseTestCase
from bucketlist.models import ListItem
import json


class TestCase(BaseTestCase):

    def test_item_is_added(self):
        self.add_bucketlist("Bucketlist1")
        response = self.add_bucketlist_item(1, "Run a marathon.")
        list_items = ListItem.query.all()
        self.assertEqual(len(list_items), 1)
        self.assertIn('Run a marathon.', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_item_is_deleted(self):
        self.add_bucketlist("Bucketlist1")
        self.add_bucketlist_item(1, "Run a marathon")
        self.add_bucketlist_item(1, "Ride a horse")
        response = self.delete_bucketlist_item(id=1, item_id=1)
        list_items = ListItem.query.all()
        self.assertEqual(len(list_items), 1)
        self.assertIn("Successfully deleted.", str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_item_is_updated(self):
        self.add_bucketlist("Bucketlist1")
        self.add_bucketlist_item(1, "Run a marathon")
        response = self.update_bucketlist_item(id=1, item_id=1, name="Sky dive")
        data = json.loads(response.data.decode())
        self.assertIn("Sky dive", str(response.data))
        self.assertNotEqual(data['date_modified'], data['date_created'])

    def test_first_letter_is_capitalised(self):
        self.add_bucketlist("Bucketlist1")
        response = self.add_bucketlist_item(1, "run a marathon")
        self.assertIn('Run a marathon', str(response.data))
