import json


class Info:
    def __init__(self, json_path, write_new=False):
        self.path = json_path
        if write_new:
            data = {'sizes': [],
                    'transitions': {},
                    'alternatives': {}}

            with open(self.path, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            data = self.load()

        self.transitions = data['transitions']
        self.sizes = data['sizes']
        self.alternatives = data['alternatives']

    def contains_key(self, key):
        return key in self.transitions

    def contains_local_index(self, index):
        return 0 <= index < len(self.sizes)

    def get_all_locations(self, global_index):
        for index in self.transitions[global_index]:
            yield index

    def dump(self):
        data = {'alternatives': self.alternatives,
                'transitions': self.transitions, 'sizes': self.sizes}

        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)

    def load(self):
        with open(self.path, 'r') as file:
            return json.load(file)
