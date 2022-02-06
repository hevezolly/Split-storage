import unittest
import os
from Modules.info import Info


class InfoTests(unittest.TestCase):
    JSON_PATH = 'tests.json'

    def tearDown(self):
        if os.path.isfile(self.JSON_PATH):
            os.remove(self.JSON_PATH)

    def test_creation(self):
        info = Info(self.JSON_PATH, True)
        self.assertListEqual([], info.sizes)
        self.assertDictEqual({}, info.transitions)
