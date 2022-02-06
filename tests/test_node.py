import unittest
import os
import shutil
from node import Node


class NodeTest(unittest.TestCase):
    PATH = 'testDir'

    def setUp(self):
        if not os.path.isdir(self.PATH):
            os.mkdir(self.PATH)

    def tearDown(self):
        if os.path.isdir(self.PATH):
            shutil.rmtree(self.PATH)

    def test_creation(self):
        node = Node(self.PATH)
        node.clear()
        self.assertDictEqual({}, node.info.transitions)
        self.assertListEqual([], node.info.sizes)

    def test_write(self):
        node = Node(self.PATH)
        node.clear()
        node['asdf'] = 'elrk'
        self.assertTrue('asdf' in node)
        self.assertListEqual(['elrk'], node['asdf'])
        new_node = Node(self.PATH)
        self.assertListEqual(['elrk'], node['asdf'])
        self.assertTrue('asdf' in new_node)

    def test_index(self):
        node = Node(self.PATH)
        node.clear()
        node['asdf'] = 'asdf'
        index = node._get_best_file_index(10)
        self.assertEqual(1, len(node.info.sizes))
        self.assertEqual(0, index)

    def test_multiple_register_write(self):
        node = Node(self.PATH)
        node.clear()
        node['asdf'] = 'asdf'
        node['Asdf'] = 'Asdf'
        node['ASdf'] = '1'
        self.assertListEqual(['asdf', 'Asdf', '1'],
                             node.get_value('aSdf', False))
        self.assertListEqual(['Asdf'], node.get_value('Asdf'))

    def test_multiple_write_one_by_one(self):
        node = Node(self.PATH)
        node.clear()
        exp = []
        for i in map(str, range(100)):
            node[i] = i
            exp.append(i)
        self.assertEqual(100, len(node))
        act = [node[key][0] for key in node]
        self.assertListEqual(exp, act)

    def test_multiple_write(self):
        node = Node(self.PATH)
        node.clear()
        data = {'foo': '1', 'bar': '2', 'baz': '3'}
        node.write_multiple(**data)
        for key in data:
            self.assertEqual([data[key]], node[key])

    def test_size_skip(self):
        amount = 1500
        node = Node(self.PATH)
        node.clear()
        for i in range(amount):
            node[str(i)] = str(i)
        self.assertEqual(amount, len(node))
        for i in range(amount):
            self.assertListEqual([str(i)], node[str(i)])
        new_node = Node(self.PATH)
        self.assertEqual(amount, len(new_node))
        for i in range(amount):
            self.assertListEqual([str(i)], new_node[str(i)])

    def test_large_file(self):
        node = Node(self.PATH)
        node.clear()
        data = 'z'*5000
        node['1'] = data
        print(node.info.sizes)
        self.assertListEqual([data], node['1'])
        new_node = Node(self.PATH)
        self.assertListEqual([data], new_node['1'])

    def test_del_file(self):
        node = Node(self.PATH)
        node.clear()
        node['1'] = 'asdf'
        self.assertListEqual(['asdf'], node['1'])
        node.del_data('1')
        with self.assertRaises(ValueError):
            test = node['1']

    def test_del_multiple_register_one_by_one(self):
        node = Node(self.PATH)
        node.clear()
        node['asdf1'] = '1'
        node['Asdf1'] = '2'
        self.assertListEqual(['1', '2'], node.get_value('asdf1', False))
        node.del_data('asdf1', False)
        self.assertEqual(0, len(node))
        with self.assertRaises(ValueError):
            t = node.get_value('asdf1', False)

    def test_del_in_multiple_one_by_one(self):
        node = Node(self.PATH)
        node.clear()
        for i in range(100):
            node[str(i)] = str(i)
        node.del_data('50')
        node.del_data('49')
        self.assertEqual(98, len(node))
        for i in range(100):
            if i not in (50, 49):
                self.assertListEqual([str(i)], node[str(i)])
            else:
                with self.assertRaises(ValueError):
                    t = node[str(i)]

    def test_del_multiple(self):
        node = Node(self.PATH)
        node.clear()
        data = {'foo': '1', 'bar': '2', 'baz': '3'}
        node.write_multiple(**data)
        node.del_multiple(True, 'foo', 'bar')
        with self.assertRaises(ValueError):
            t = node['foo']
            t = node['bar']
        self.assertEqual(['3'], node['baz'])

    def test_del_multiple_register(self):
        node = Node(self.PATH)
        node.clear()
        data = {'foo': 'bar', 'Foo': 'Bar', 'BAR': 'BAZ', 'bar': 'baz'}
        node.write_multiple(**data)
        node.del_multiple(False, 'foo', 'bar')
        with self.assertRaises(ValueError):
            t = node['foo']
            t = node['Foo']
            t = node['BAR']
            t = node['bar']

    def test_replace(self):
        node = Node(self.PATH)
        node.clear()
        node['1'] = 'asdf'
        self.assertListEqual(['asdf'], node['1'])
        node['1'] = 'sdfg'
        self.assertListEqual(['sdfg'], node['1'])

    def test_fix(self):
        node = Node(self.PATH)
        node.clear()
        node['1'] = 'z' * 5000
        node['2'] = 'asdf'
        os.remove(node._path(0))
        node._fix_missing_files()
        self.assertFalse('1' in node)
        self.assertEqual(['asdf'], node['2'])

    def test_fix_write(self):
        node = Node(self.PATH)
        node.clear()
        node['1'] = 'asdf'
        os.remove(node._path(0))
        node['2'] = 'zxcv'
        self.assertFalse('1' in node)
        self.assertEqual(['zxcv'], node['2'])

    def test_fix_delete(self):
        node = Node(self.PATH)
        node.clear()
        node['1'] = 'asdf'
        os.remove(node._path(0))
        with self.assertRaises(ValueError):
            node.del_data('1')
