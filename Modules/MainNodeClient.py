import socket
import struct
import multiprocessing.dummy as mult
import multiprocessing
from Modules.socket_controller import recv
from Modules.storage_controller import Storage
import shlex
import os

lock = multiprocessing.Lock()


class MainNodeClient:
    def __init__(self, directory, create_new=False):
        self.nodes = []
        self.path = directory
        if not os.path.isdir(self.path):
            raise NotADirectoryError(f'no such directory as {directory}')
        self.storage = Storage(directory, create_new)
        self.nodes_data = self.storage.nodes_data
        self.cleared_indexes = []
        self.clear = create_new
        self.nodes = [None] * len(self.nodes_data)
        self.inactive_indexes = set(range(len(self.nodes)))
        for i in range(len(self.nodes_data)):
            self.connect_to_node(i)

    def add_inactive_index(self, index):
        self.inactive_indexes.add(index)
        self.nodes[index].close()

    def get_capacities(self):
        return self.storage.capacities

    def get_active_indexes(self):
        for i in range(len(self.nodes)):
            if self.nodes[i] and i not in self.inactive_indexes:
                yield i

    def __contains__(self, item):
        return item in self.storage.key_indexes

    def get_active_composition(self, key):
        composition = self.storage.get_all_indexes(key)
        return [c for c in self.get_active_indexes() if c in composition]

    def get_key(self, key):
        if key not in self:
            raise ValueError("no such key")
        self.ping()
        indexes = self.get_active_composition(key)
        if not indexes:
            raise ImportantNodesDisconnected("no active nodes")

        def get_boundary(local_index):
            length = self.storage.key_length[key]
            fragment_length = length // len(indexes)
            start = local_index * fragment_length
            if local_index == len(indexes) - 1:
                end = length
            else:
                end = (local_index + 1) * fragment_length
            return start, end

        def get_real_key(local_index, active_node_index=None):
            if active_node_index is None:
                node_index = indexes[local_index]
            else:
                node_index = list(self.get_active_indexes())[active_node_index]
            boundary = get_boundary(local_index)
            if boundary[0] == boundary[1]:
                return ''
            return self.get_key_part(node_index, key, boundary)

        def get_nones(result_list):
            none_number = 0
            for i in range(len(result_list)):
                if result_list[i] is None:
                    yield i, none_number
                    none_number += 1

        p = mult.Pool()
        result = p.map(lambda a: get_real_key(a), range(len(indexes)))
        while None in result:
            def assign(index, value):
                result[index] = value
            active_nodes = self.get_active_composition(key)
            if not active_nodes:
                raise ImportantNodesDisconnected("no active nodes were found")
            p.map(lambda args: assign(
                args[0], get_real_key(args[0], args[1])), get_nones(result))
        return ''.join(result)

    def get_key_part(self, index, key, boundary=None):
        if key not in self:
            raise ValueError("no such key")
        if index in self.inactive_indexes:
            return None
        try:
            if boundary is None:
                answer = self.get_answer(index, f'-r {shlex.quote(key)}')
            else:
                answer = self.get_answer(
                    index,
                    f'-r {shlex.quote(key)} -g {boundary[0]} {boundary[1]}')
        except socket.error:
            self.add_inactive_index(index)
            return None
        return answer[0]

    def disconnect_all(self, total=False):
        for i in self.get_active_indexes():
            self.disconnect(i, total)

    def disconnect(self, index, total=False):
        active_indexes = list(self.get_active_indexes())
        if index not in active_indexes:
            raise ValueError("incorrect index")
        s = self.nodes[index]
        if total:
            s.sendall(struct.pack('i', -1))
        s.close()
        self.add_inactive_index(index)

    def add_key_with_composition(self, key, value, composition=(0,)):
        was_added = False
        if key in self:
            self.delete_key(key)

        def add(node_index):
            nonlocal was_added
            if node_index in self.inactive_indexes:
                return
            try:
                self.get_answer(node_index,
                                f'-w {shlex.quote(key)} {shlex.quote(value)}')
                self.storage.add_index(key, node_index)
                self.storage.add_capacity(node_index, len(value))
                was_added = True
            except socket.error:
                self.add_inactive_index(node_index)

        p = mult.Pool()
        p.map(add, composition)
        if not was_added:
            raise ImportantNodesDisconnected("no nodes found")
        self.storage.key_length[key] = len(value)
        self.storage.dump()

    def delete_key(self, key):
        if key not in self:
            raise ValueError("no such key")

        def delete(node_index):
            self.storage.remove_capacity(node_index,
                                         self.storage.key_length[key])
            self.delete_pure_keys(node_index, key)

        p = mult.Pool()
        p.map(delete, self.storage.get_all_indexes(key))
        self.storage.key_indexes.pop(key)
        self.storage.key_length.pop(key)
        self.storage.dump()

    def delete_pure_keys(self, index, *keys):
        if not keys:
            return
        if index in self.inactive_indexes:
            self.storage.add_keys_to_delete(index, *keys)
        delete_data = '-D '
        for key in keys:
            delete_data += f'{shlex.quote(key)} '

        delete_data = delete_data.rstrip()
        try:
            self.get_answer(index, delete_data)
        except socket.error:
            self.add_inactive_index(index)
            self.storage.add_keys_to_delete(index, *keys)

    def ping(self):
        for index in self.get_active_indexes():
            try:
                self.get_answer(index, 'ping')
            except socket.error:
                self.add_inactive_index(index)

    def get_answer(self, index, request):
        if index < 0 or index >= len(self.nodes):
            raise ValueError("index is out of range")
        msg = request.encode('utf8')
        sock = self.nodes[index]
        sock.sendall(struct.pack('i', len(msg)) + msg)
        answers = []
        while True:
            data = recv(sock, 4, True)
            length, = struct.unpack('i', data)
            if length <= 0:
                break
            main_data = recv(sock, length, True)
            answer = main_data.decode('utf8')
            answers.append(answer)
        return answers

    def connect_to_new_node(self, host, port):
        if (host, port) in self.nodes_data:
            raise ValueError("this node is already exists")
        sock = socket.socket()
        index = len(self.nodes)
        try:
            sock.connect((host, port))
            self.nodes.append(sock)
            self.nodes_data.append((host, port))
            self.storage.add_nodes_data(host, port)
            self.get_answer(index, '-e')
            self.cleared_indexes.append(index)
        except socket.error:
            if sock in self.nodes:
                self.nodes.remove(sock)
            if (host, port) in self.nodes_data:
                self.nodes_data.remove((host, port))
                self.storage.del_nodes_data(index)
            return False
        return True

    def connect_to_node(self, index):
        sock = socket.socket()
        empty = self.clear and index not in self.cleared_indexes
        if not 0 <= index < len(self.nodes_data):
            raise ValueError('index is out of range')
        try:
            sock.connect(self.nodes_data[index])
            self.nodes[index] = sock
            if index < len(self.nodes):
                if index in self.inactive_indexes:
                    self.inactive_indexes.remove(index)
                if empty:
                    self.get_answer(index, '-e')
                    self.storage.clear_keys_to_delete(index)
                    self.cleared_indexes.append(index)
                else:
                    keys_to_delete = self.storage.get_keys_to_delete(index)
                    self.delete_pure_keys(index, *keys_to_delete)
                    self.storage.delete_keys_to_delete(index, *keys_to_delete)
            if index in self.inactive_indexes:
                self.inactive_indexes.remove(index)
            print(f'successfully connected to {self.nodes_data[index]} '
                  f'by index {index}')
        except socket.error:
            if sock not in self.nodes:
                self.nodes[index] = sock
            self.add_inactive_index(index)
            print(f'failed to connected to {self.nodes_data[index]} '
                  f'by index {index}')


class ImportantNodesDisconnected(Exception):
    pass
