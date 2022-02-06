import unittest
import Modules.parse as parser


class ParserTests(unittest.TestCase):
    def test(self):
        key = "asdffasgaew"
        value = "hoqrqwbegdsaufhidjlkqen"
        act_key, act_value = parser.decode_pair(parser.encode_pair(key, value))
        self.assertEqual(key, act_key)
        self.assertEqual(value, act_value)
