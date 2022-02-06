import json
import os


class Storage:

    FILE_NAME = "storage.json"

    def __init__(self, dir_path, create_new=False):
        self.path = os.path.join(dir_path, self.FILE_NAME)
        self.key_indexes = {}
        self.key_length = {}
        self.deleted_keys = {}
        self.capacities = []
        self._nodes_data = []
        if create_new:
            self.dump()
        elif not os.path.isfile(self.path):
            raise FileNotFoundError(f'no such file as {self.path}')
        self.load()

    def dump(self):
        data = {"key_compositions": self.key_indexes,
                "key_length": self.key_length,
                "deleted_keys": self.deleted_keys, 'capacity': self.capacities,
                'nodes_data': self._nodes_data}
        with open(self.path, 'w') as file:
            json.dump(data, file)

    def load(self):
        with open(self.path, 'r') as file:
            data = json.load(file)
        self.key_indexes = data["key_compositions"]
        self.key_length = data["key_length"]
        self.deleted_keys = data["deleted_keys"]
        self.capacities = data['capacity']
        self._nodes_data = data['nodes_data']

    def get_keys_to_delete(self, index):
        return list(self.deleted_keys.get(str(index), []))

    def add_capacity(self, index, length):
        for i in range(index + 1):
            if i >= len(self.capacities):
                self.capacities.append(0)
        self.capacities[index] += length
        self.dump()

    def remove_capacity(self, index, length):
        if not (0 <= index < len(self.capacities)):
            raise ValueError("index is out of range")
        if length > self.capacities[index]:
            raise ValueError("length is to big")
        self.capacities[index] -= length
        self.dump()

    def delete_keys_to_delete(self, index, *keys):
        index = str(index)
        if index not in self.deleted_keys and keys:
            raise ValueError("no such index")
        for key in keys:
            self.deleted_keys[index].remove(key)
        self.dump()

    def clear_keys_to_delete(self, index):
        index = str(index)
        if index not in self.deleted_keys:
            raise ValueError("no such index")
        self.deleted_keys[index] = []
        self.dump()

    def del_nodes_data(self, index):
        self._nodes_data.pop(index)
        self.dump()

    def add_nodes_data(self, host, port):
        self._nodes_data.append([host, port])
        self.dump()

    @property
    def nodes_data(self):
        return [(h[0], int(h[1])) for h in self._nodes_data]

    def get_all_indexes(self, key):
        if key not in self.key_indexes:
            raise ValueError("no such key")
        return self.key_indexes[key]

    def add_keys_to_delete(self, index, *keys):
        index = str(index)
        if index not in self.deleted_keys:
            self.deleted_keys[index] = []
        for key in keys:
            if key not in self.deleted_keys[index]:
                self.deleted_keys[index].append(key)
        self.dump()

    def __contains__(self, item):
        return item in self.key_indexes

    def add_index(self, key, index):
        if key not in self:
            self.key_indexes[key] = []
        if index not in self.key_indexes[key]:
            self.key_indexes[key].append(index)
            self.dump()

    def delete_key(self, key):
        if key not in self:
            raise ValueError(f'no such key as {key}')
        self.key_indexes.pop(key)
        self.dump()
