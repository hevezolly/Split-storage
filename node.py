import Modules.parse as Parser
from Modules.info import Info
import os
import argparse
import sys
import shutil
import csv
from Modules.single_file_controller import SFC, NUMBER_OF_KBYTES


class Node:
    JSON_NAME = 'local_info.json'

    def __init__(self, dir_path):
        self.dir_path = dir_path
        info_file_name = os.path.join(dir_path, self.JSON_NAME)

        if not os.path.isdir(dir_path):
            raise ValueError('no such directory')

        if not os.path.isfile(info_file_name):
            shutil.rmtree(dir_path, ignore_errors=True)
            os.mkdir(dir_path)
            self.info = Info(info_file_name, True)
        else:
            self.info = Info(info_file_name)

    def __len__(self):
        self._fix_missing_files()
        return len(self.info.transitions)

    def __iter__(self):
        self._fix_missing_files()
        return iter(self.info.transitions)

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        if key in self:
            self.replace_data(key, value)
        else:
            self.write_data(key, value)

    def __contains__(self, key):
        return key in self.info.transitions

    def write_multiple(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]

    def del_multiple(self, case_sensitive, *keys):
        for key in keys:
            self.del_data(key, case_sensitive)

    def contains_key(self, key, case_sensitive=True):
        if case_sensitive:
            return key in self.info.transitions
        lower_key = key.casefold()
        return lower_key in self.info.alternatives

    def clear(self):
        shutil.rmtree(self.dir_path, ignore_errors=True)
        os.mkdir(self.dir_path)
        self.info.transitions = {}
        self.info.sizes = []
        self.info.alternatives = {}
        self.info.dump()

    def get_value(self, key, case_sensitive=True, boundary=(None, None)):
        if case_sensitive:
            value = self._get_value_by_key(key)
            if value is None:
                raise ValueError("key doesn't exists")
            return [self._get_value_by_key(key, boundary)]

        data = []
        lower_key = key.casefold()
        if lower_key not in self.info.alternatives:
            raise ValueError("key doesn't exists")

        for new_key in self.info.alternatives[lower_key]:
            data.append(self._get_value_by_key(new_key, boundary))

        return data

    def _get_value_by_key(self, key, boundary=(None, None)):
        if key not in self:
            return None

        pathes = self.info.transitions[key]
        all_bytes = bytearray()
        for index in pathes:
            path = self._path(index)
            try:
                file = SFC(path, self.info.sizes[int(index)])
            except FileNotFoundError:
                self._fix_missing_files()
                return None
            datas = file.get_data(Parser.get_index(key))

            for data in datas:
                new_key = Parser.get_key(data)
                if key == new_key:
                    all_bytes.extend(Parser.get_value_bytes(data))
                    break
            else:
                return None
        return Parser.get_value(all_bytes[boundary[0]:boundary[1]])

    def replace_data(self, key, value):
        if key not in self:
            raise ValueError("key doesn't exists")

        self._fix_missing_files()
        self.del_data(key)
        self.write_data(key, value)

    def del_data(self, key, case_sensitive=True):
        lower_key = key.casefold()
        if case_sensitive:
            self._del_data_by_single_key(key)
            self.info.alternatives[lower_key].remove(key)
            if not self.info.alternatives[lower_key]:
                del self.info.alternatives[lower_key]
            self.info.dump()
            return

        if lower_key not in self.info.alternatives:
            raise ValueError("key doesn't exists")

        for key in self.info.alternatives[lower_key]:
            self._del_data_by_single_key(key)
        del self.info.alternatives[lower_key]
        self.info.dump()

    def _del_data_by_single_key(self, key):
        if key not in self:
            raise ValueError("key doesn't exists")

        index = Parser.get_index(key)
        pathses = self.info.transitions[key]
        for file_index in pathses:
            try:
                file = SFC(self._path(file_index), self.info.sizes[file_index])
            except FileNotFoundError:
                self._fix_missing_files()
                raise ValueError("key doesn't exists")
            datas = file.get_data(index)

            for i in range(len(datas)):
                new_key, value = Parser.decode_pair(datas[i])

                if new_key == key:
                    file.del_data(index, i)
                    self.info.sizes[self.info.transitions[key][i]] = file.size
                    break

        del self.info.transitions[key]
        self.info.dump()

    def write_data(self, key, value):
        if key in self:
            raise ValueError('key already in storage')

        all_data = Parser.encode_value(value)
        max_size = NUMBER_OF_KBYTES * 1024 - 2
        key_data = Parser.encode_key(key)
        self.info.transitions[key] = []

        available_size = max_size - len(key_data)
        num_of_divides = len(all_data) // available_size
        for i in range(num_of_divides):
            data_to_write = all_data[i*available_size:(i+1)*available_size]
            write_index = self._write_short(key, data_to_write)
            self.info.transitions[key].append(write_index)

        data_to_write = all_data[num_of_divides * available_size:]
        write_index = self._write_short(key, data_to_write)
        self.info.transitions[key].append(write_index)

        lower_key = key.casefold()
        if lower_key in self.info.alternatives:
            self.info.alternatives[lower_key].append(key)
        else:
            self.info.alternatives[lower_key] = [key]
        self.info.dump()

    def _write_short(self, key, data_bytes):
        key_data = Parser.encode_key(key)
        key_data.extend(data_bytes)

        size = len(key_data)
        if size > NUMBER_OF_KBYTES * 1024 - 2:
            raise ValueError('data size is to big')

        file_index = self._get_best_file_index(len(key_data))
        path = self._path(file_index)
        if file_index is None:
            file_index = self._create_new_file()
            path = self._path(file_index)

        index = Parser.get_index(key)
        try:
            file = SFC(path, self.info.sizes[int(file_index)])
        except FileNotFoundError:
            self._fix_missing_files()
            return self._write_short(key, data_bytes)
        file.write_data(data=key_data, index=index)
        self.info.sizes[int(file_index)] = file.size
        return file_index

    def _path(self, index):
        return os.path.join(self.dir_path, str(index))

    def _create_new_file(self):
        path = len(self.info.sizes)
        if os.path.isfile(self._path(path)):
            os.remove(self._path(path))
        file = SFC(self._path(path), create_new=True)
        self.info.sizes.append(file.size)
        self.info.dump()
        return path

    def _get_best_file_index(self, size):
        min_difference = NUMBER_OF_KBYTES * 1024
        index = -1

        for i in range(len(self.info.sizes)):
            difference = self.info.sizes[i] - size

            if 0 <= difference < min_difference:
                index = i
                min_difference = difference

        return None if index == - 1 else index

    def _fix_missing_files(self):
        missing_indexes = [i for i in range(len(self.info.sizes))
                           if not os.path.isfile(self._path(i))]

        if not missing_indexes:
            return

        mis = set(missing_indexes)
        missing_keys = {}
        for key in self.info.transitions:
            key_set = set(map(int, self.info.transitions[key]))
            if mis & key_set:
                missing_keys[key] = list(key_set - mis)

        for key in missing_keys:
            index_in_file = Parser.get_index(key)
            for file_index in missing_keys[key]:
                file = SFC(self._path(file_index), self.info.sizes[file_index])
                datas = file.get_data(index_in_file)

                for i in range(len(datas)):
                    new_key = Parser.get_key(datas[i])
                    if new_key == key:
                        file.del_data(index_in_file, i)
                        self.info.sizes[file_index] = file.size
                        break

            self.info.alternatives[key.casefold()].remove(key)
            if not self.info.alternatives[key.casefold()]:
                del self.info.alternatives[key.casefold()]
            del self.info.transitions[key]

        for file_index in missing_indexes:
            file = SFC(self._path(file_index), create_new=True)
            self.info.sizes[file_index] = file.size
        self.info.dump()

    def process_args(self, args):
        if args.empty:
            self.clear()

        elif args.contains is not None:
            contains = self.contains_key(args.contains, args.reg)
            if contains:
                return ['YES']
            return ['NO']

        elif args.write is not None:
            key, value = args.write
            try:
                self[key] = value
            except ValueError:
                return ['Error: key is to big']

        elif args.write_multiple is not None:
            if args.write_multiple:
                data = args.write_multiple
            else:
                data = sys.stdin.readlines()
                data = [a.rstrip() for a in data]
            try:

                def get_key_value(line):
                    splits = list(csv.reader([line],
                                             delimiter='=',
                                             quotechar='"'))[0]
                    if len(splits) <= 1:
                        raise TypeError()
                    return splits[0], '='.join(splits[1:])

                data = dict(map(get_key_value, data))
            except TypeError:
                return ['Error: input is not in format KEY=VALUE']
            try:
                self.write_multiple(**data)
            except ValueError:
                return ['Error: key is to big']

        elif args.read is not None:

            def try_int(value):
                if value is None:
                    return None
                return int(value)

            key = args.read
            r = list(map(try_int, args.range))
            return list(self.get_value(key, args.reg, r))

        elif args.delete is not None:
            key = args.delete
            self.del_data(key, args.reg)

        elif args.delete_multiple is not None:
            if args.delete_multiple:
                data = args.delete_multiple
            else:
                data = sys.stdin.readlines()
                data = list(set([a.rstrip() for a in data]))
            self.del_multiple(args.reg, *data)

        elif args.list:
            return list(self)

        else:
            return None

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-w', '--write', nargs=2, metavar=('KEY', 'VALUE'),
                            help='writes VALUE to store by KEY and exit')

        parser.add_argument('-W', '--write_multiple', nargs='*',
                            metavar=('KEY=VALUE', 'KEY=VALUE'),
                            help='''writes multiple VALUEs by its KEY,
                                if no pairs were given - reads data from
                                                                stdin''')

        parser.add_argument('-r', '--read', metavar='KEY',
                            help='read value by KEY in storage and exit')

        parser.add_argument('-g', '--range', metavar=('START', 'END'), nargs=2,
                            default=(None, None),
                            help='if used with -r, outs values with range')

        parser.add_argument('-d', '--delete', metavar='KEY',
                            help='delete value in storage by KEY and exit')
        parser.add_argument('-D', '--delete_multiple', nargs='*',
                            metavar=('KEY', 'KEY'),
                            help='''deletes multiple KEYs from node, if no KEY
                                were given - reads data from stdin''')

        parser.add_argument('-e', '--empty', action='store_true',
                            default=False,
                            help='clear the storage and exit')

        parser.add_argument('-c', '--contains', metavar='KEY',
                            help='writes whether node contains KEY')

        parser.add_argument('-l', '--list', action='store_true', default=False,
                            help='writes all keys in storage and exit')

        parser.add_argument('-i', '--ignore_register', action='store_false',
                            dest='reg',
                            default=True,
                            help='allows to ignore register in key')

        return parser


def answer():
    usage = 'node.py DIRECTORY OPTIONS'
    parser = Node.get_parser()
    parser.usage = usage
    parser.description = 'local storage node'

    parser.add_argument('DIRECTORY', help='path to local storage')

    parser.add_argument('-h', '--help', action='help')

    parser.add_argument('-s', '--silent_mode', action='store_true',
                        dest='silent',
                        default=False,
                        help='makes program write nothing to the output')

    args = parser.parse_args()
    node = Node(args.DIRECTORY)
    result = node.process_args(args)
    if not args.silent and result is not None:
        for line in result:
            print(line)


if __name__ == '__main__':
    answer()
