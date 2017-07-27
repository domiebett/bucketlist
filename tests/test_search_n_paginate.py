from . test import BaseTestCase, db
import json

class TestPaginate(BaseTestCase):

    def test_paginate_works(self):
        for i in range(10):
            self.add_bucketlist("Bucketlist{}".format(i))
        response = self.paginate(4)
        self.assertTrue(len(response.data), 4)

    def test_search_works(self):
        for i in range(10):
            self.add_bucketlist("Bucketlist{}".format(i))
        self.add_bucketlist("Search1")
        self.add_bucketlist("Search2")
        response = self.search()
        self.assertEqual(len(json.loads(response.data)), 2)
