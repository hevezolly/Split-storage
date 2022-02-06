import unittest
import os
import struct
from random import randint
from Modules.single_file_controller import SFC


class SFCTests(unittest.TestCase):
    PATH = 'storageTest'

    def setUp(self):
        if os.path.isfile(self.PATH):
            os.remove(self.PATH)

    def tearDown(self):
        if os.path.isfile(self.PATH):
            os.remove(self.PATH)

    def test_get_bin(self):
        self.assertEqual(bin(4095), SFC._get_bin(4095), 'without length')
        self.assertEqual(5, len(SFC._get_bin(12, 5)[2:]), 'incorrect length')
        self.assertEqual('0b001', SFC._get_bin(1, 3),
                         'equals with more length')
        self.assertEqual('0b0', SFC._get_bin(2, 1), 'equals with less length')

    def run_boundary_test(self, exp_size, exp_is_empty, exp_empty):
        is_empty, size, empty = SFC._get_info_from_bytes(
            SFC._get_encoded_boundary_descriptor(exp_size, exp_empty,
                                                 exp_is_empty))
        self.assertEqual(exp_is_empty, is_empty, 'is empty')
        self.assertEqual(exp_size, size, 'size')
        self.assertEqual(exp_empty, empty, 'number of empty')

    def test_boundary(self):
        for i in range(50):
            size = randint(1, 4096)
            is_empty = randint(0, 1) == 1
            num_of_empty = randint(0, 2)
            self.run_boundary_test(size, is_empty, num_of_empty)

    def run_empty_table_test(self, exp_table):
        table = SFC._decode_empty_table(SFC._encode_empty_table(exp_table))
        self.assertListEqual(exp_table, table)

    @staticmethod
    def generate_empty_table(length_bound):
        length = randint(0, length_bound)
        table = []
        for j in range(length):
            table.append(randint(0, 2 ** 12 - 2))
        return table

    def test_empty_table(self):
        for i in range(100):
            self.run_empty_table_test(self.generate_empty_table(100))

    def run_translation_table_test(self, exp_table):
        table = SFC._decode_transition_table(SFC._encode_transition_table(
            exp_table))
        self.assertDictEqual(exp_table, table)

    @staticmethod
    def generate_translation_table(keys_bound, collision_bound):
        table = {}
        num_of_keys = randint(1, keys_bound)
        for j in range(num_of_keys):
            key = randint(0, 500000)
            table[key] = []
            num_of_collisions = randint(1, collision_bound)
            for l in range(num_of_collisions):
                table[key].append(randint(0, 2 ** 12))
        return table

    def test_translation_table(self):
        for i in range(100):
            self.run_translation_table_test(
                self.generate_translation_table(100, 10))

    def run_tables_test(self, exp_empty_table, exp_translation_table):
        empty, translation = SFC._get_tables_from_bytes(
            SFC._get_encoded_tables(exp_empty_table, exp_translation_table))
        self.assertListEqual(exp_empty_table, empty)
        self.assertDictEqual(exp_translation_table, translation)

    def test_tables(self):
        empty = [0, 2]
        translation = {0: [2, 3], 15: [2, 4]}
        self.run_tables_test(empty, translation)

    def test_empty_file(self):
        file = SFC(self.PATH, create_new=True)
        emptyes, translations = file.get_tables_from_file()
        self.assertListEqual([0], emptyes)
        self.assertEqual([0], file.empties)
        self.assertDictEqual({}, translations)

    def test_write_to_file(self):
        file = SFC(self.PATH, create_new=True)
        size = file.size
        index = 1
        exp_data = struct.pack('h', 1050)
        (exp_translation,) = struct.unpack('h', exp_data)
        file.write_data(data=exp_data, index=index)
        self.assertEqual(size-4, file.size)
        data = file.get_data(index)
        (actual,) = struct.unpack('h', data[0])
        self.assertEqual(exp_translation, actual)

    def test_write_large_file(self):
        file = SFC(self.PATH, create_new=True)
        size = file.size
        index = 1
        exp_data = bytearray(size)
        file.write_data(data=exp_data, index=index)
        self.assertEqual(0, file.size)
        data = file.get_data(index)[0]
        self.assertEqual(exp_data, data)

    def test_write_multiple_no_collisions(self):
        file = SFC(self.PATH, create_new=True)
        for index in range(1, 10):
            exp_data = struct.pack('h', 10 * index)
            file.write_data(data=exp_data, index=index)
        for i in range(1, 10):
            data = file.get_data(i)
            (actual,) = struct.unpack('h', data[0])
            self.assertEqual(10 * i, actual)

    def test_get_best_index(self):
        file = SFC(self.PATH, create_new=True)
        best_index = file._get_index_of_suitable_spot(4)
        self.assertEqual(0, best_index)
        file.write_data(data=bytes(4), index=1)
        best_index = file._get_index_of_suitable_spot(4)
        self.assertEqual(6, best_index)

    def test_write_multiple_collisions(self):
        file = SFC(self.PATH, create_new=True)
        datas = [10*i for i in range(1, 10)]
        pucked_datas = [struct.pack('h', d) for d in datas]
        for data in pucked_datas:
            file.write_data(data=data, index=1)
        actual_datas = file.get_data(1)
        unpackes_datas = [struct.unpack('h', d)[0] for d in actual_datas]
        self.assertListEqual(datas, unpackes_datas)

    def test_del_no_collisions(self):
        file = SFC(self.PATH, create_new=True)
        file.write_data(data=bytes(1), index=1)
        self.assertIsNotNone(file.get_data(1))
        file.del_data(index=1, index_of_collision=0)
        self.assertIsNone(file.get_data(1))

    def test_del_collisions(self):
        file = SFC(self.PATH, create_new=True)
        file.write_data(data=bytes(1), index=1)
        file.write_data(data=bytes(1), index=1)
        self.assertEqual(2, len(file.get_data(1)))
        file.del_data(index=1, index_of_collision=1)
        self.assertEqual(1, len(file.get_data(1)))
        file.del_data(index=1, index_of_collision=0)
        self.assertIsNone(file.get_data(1))

    def test_recomposition(self):
        file = SFC(self.PATH, create_new=True)
        file.write_data(data=bytes(1), index=1)
        file.write_data(data=bytes(2), index=2)
        file.write_data(data=bytes(1), index=3)
        file.write_data(data=bytes(2), index=4)
        file.del_data(2, 0)
        file.del_data(3, 0)
        exp1 = file.get_data(1)[0]
        exp2 = file.get_data(4)[0]
        file.recompose()
        act1 = file.get_data(1)[0]
        act2 = file.get_data(4)[0]
        self.assertEqual(exp1, act1)
        self.assertEqual(exp2, act2)

    def test_write_recomposition(self):
        file = SFC(self.PATH, create_new=True)
        file.write_data(data=bytes(1), index=1)
        file.del_data(index=1, index_of_collision=0)
        file.write_data(data=bytes(3070), index=1)
        exp = bytes(3070)
        act = file.get_data(1)[0]
        self.assertEqual(exp, act)
