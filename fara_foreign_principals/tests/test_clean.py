from __future__ import absolute_import
import unittest
from fara_foreign_principals.spiders import CleanSpider
from responses import fake_response_from_file

class CleanSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = CleanSpider()

    def _test_item_results(self, results, expected_length):
        count = 0
        for item in results:
            self.assertIsNotNone(item['url'])
            self.assertIsNotNone(item['country'])
            self.assertIsNotNone(item['state'])
            self.assertIsNotNone(item['reg_num'])
            self.assertIsNotNone(item['address'])
            self.assertIsNotNone(item['foreign_principal'])
            self.assertIsNotNone(item['date'])
            self.assertIsNotNone(item['registrant'])
            self.assertIsNotNone(item['exhibit_url'])
        self.assertEqual(count, expected_length)

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('sample.html'))
        self._test_item_results(results, 9)
