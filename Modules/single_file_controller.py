import os
import struct

NUMBER_OF_KBYTES = 3


class SFC:
    def __init__(self, path, size=NUMBER_OF_KBYTES * 1024 - 2,
                 create_new=False):
        self.path = path
        self.size = size
        self.file_length = NUMBER_OF_KBYTES * 1024

        if create_new:
            if os.path.isfile(path):
                raise FileExistsError(f'given file {path} is already exists')
            self.create_storage_file()

        if not os.path.isfile(path):
            raise FileNotFoundError(f'no such file as {path}')

        self.empties, self.transitions = self.get_tables_from_file()

    def create_storage_file(self):
        """Creates empty storage file in <path>"""

        (first, second) = self._get_encoded_boundary_descriptor(
            NUMBER_OF_KBYTES * 1024 - 2, 0, True)
        data = bytearray(1024 * NUMBER_OF_KBYTES)
        data[0] = first
        data[1] = second
        data.extend(self._get_encoded_tables([0], {}))

        with open(self.path, 'bw') as file:
            file.write(data)

    def get_data(self, index):
        """returns list of data that contains in file in <path>
        by global <index>"""
        if index not in self.transitions:
            return None

        indexs_in_file = self.transitions[index]
        datas = []
        for index in indexs_in_file:
            is_empty, size, _ = self._get_info_from_file_boundary(index)

            if is_empty:
                datas.append(b'')
            else:

                with open(self.path, 'rb') as file:
                    file.seek(index + 2)
                    data = file.read(size)
                    datas.append(data)

        return datas

    def _get_index_of_suitable_spot(self, size):
        """returns local index of most suitable empty spot of file in <path>
         for <size>"""
        min_difference = NUMBER_OF_KBYTES * 1024 + 1
        index_of_suitable_spot = -1

        for index in self.empties:
            _, current_size, number_of_empty = \
                self._get_info_from_file_boundary(index)

            if 0 <= current_size + number_of_empty - size < min_difference:
                min_difference = current_size + number_of_empty - size
                index_of_suitable_spot = index

        return index_of_suitable_spot

    def recompose(self):
        """recomposes file in <path> with given <file_length>
        and <available_place>
         and returns change of empty place"""
        new_file_data = bytearray()
        new_translation_table = {}
        new_index = 0

        for key in self.transitions:
            new_translation_table[key] = []

            for collision in self.transitions[key]:
                is_empty, size, empty_num = \
                    self._get_info_from_file_boundary(collision)

                with open(self.path, 'rb') as file:
                    file.seek(collision + 2)
                    new_data = file.read(size)

                new_empty_num = self.file_length - (new_index+size+2) - 1
                if new_empty_num > 2:
                    new_empty_num = 0

                new_descriptor = self._get_encoded_boundary_descriptor(
                    size, new_empty_num, is_empty)
                new_file_data.extend(new_descriptor)
                new_file_data.extend(new_data)
                new_translation_table[key].append(new_index)
                new_index += size + 2

        empty_bytes = self.file_length - new_index
        if empty_bytes <= 2:
            new_empties = []
            empty_bytes = 0
        else:

            new_empties = [new_index]
            empty_descriptor = self._get_encoded_boundary_descriptor(
                empty_bytes - 2, 0, True)
            new_file_data.extend(empty_descriptor)
            empty_bytes -= 2

        tables = self._get_encoded_tables(new_empties,
                                          new_translation_table)

        with open(self.path, 'rb+') as file:
            file.write(new_file_data)
            file.seek(self.file_length)
            file.write(tables)
            file.truncate()

        self.transitions = new_translation_table
        self.empties = new_empties
        self.size += empty_bytes - self.size

    def write_data(self, data, index):
        """writes <data> to file on <path> by global <index> and returns
        size_change"""
        local_index = self._get_index_of_suitable_spot(len(data))
        new_space = 0

        if local_index == -1:
            self.recompose()
            local_index = self._get_index_of_suitable_spot(len(data))
            if local_index == -1:
                raise ValueError(f'no place in {self.path} for given data')

        _, size, empty_bytes = self._get_info_from_file_boundary(local_index)
        write_data = bytearray()
        empty_bytes = size + empty_bytes - len(data)

        if index in self.transitions:
            self.transitions[index].append(local_index)
        else:
            self.transitions[index] = [local_index]

        self.empties.remove(local_index)
        boundary_first, boundary_second = \
            self._get_encoded_boundary_descriptor(
                len(data), empty_bytes if empty_bytes <= 2 else 0, False)
        write_data.append(boundary_first)
        write_data.append(boundary_second)
        write_data.extend(data)

        if empty_bytes > 2:
            empty_descriptor = self._get_encoded_boundary_descriptor(
                size - len(data) - 2, 0, True)
            self.empties.append(len(write_data) + local_index)
            write_data.extend(empty_descriptor)
            difference = new_space - len(data) - 2
        else:
            difference = new_space - len(data)

        table_bytes = self._get_encoded_tables(self.empties, self.transitions)

        with open(self.path, 'rb+') as file:
            file.seek(local_index)
            file.write(write_data)
            file.seek(self.file_length)
            file.write(table_bytes)
            file.truncate()

        self.size += difference

    def del_data(self, index, index_of_collision):
        """removes data from file on <path> by global <index> and
        <index_of_collisions> and returns file size difference"""
        if not os.path.isfile(self.path):
            raise ValueError(f'no such file {self.path}')

        if (index not in self.transitions)\
                or (len(self.transitions[index]) <= index_of_collision):
            raise ValueError('incorrect input')

        local_index = self.transitions[index][index_of_collision]
        _, size, number_of_empty = self._get_info_from_file_boundary(
            local_index)
        new_boundary = self._get_encoded_boundary_descriptor(
            size + number_of_empty, 0, True)
        self.empties.append(local_index)

        del self.transitions[index][index_of_collision]
        if len(self.transitions[index]) == 0:
            del self.transitions[index]

        new_tables = self._get_encoded_tables(self.empties, self.transitions)
        with open(self.path, 'br+') as file:
            file.seek(local_index)
            file.write(bytearray(new_boundary))
            file.seek(self.file_length)
            file.write(new_tables)
            file.truncate()

        self.size += size + number_of_empty
        if self._has_empty_neighbour(local_index):
            self.size += 2
            self.size = min(self.size, self.file_length - 2)

    def _has_empty_neighbour(self, index):
        _, size, empty_num = self._get_info_from_file_boundary(index)
        for other_index in self.empties:
            if other_index == index:
                continue
            _, new_size, new_empty = self._get_info_from_file_boundary(
                other_index)
            if other_index + new_size + new_empty + 2 == index:
                return True
            if size + empty_num + 2 + index == other_index:
                return True
        return False

    def _get_info_from_file_boundary(self, index):
        """reads boundary descriptor of file in <path> and returns tuple:
        (bool is_empty, int size_of_block, int number_of_empty bytes)"""
        if not os.path.isfile(self.path):
            raise ValueError(f'{self.path} is not file')

        with open(self.path, 'rb') as file:
            file.seek(index)
            boundary = file.read(2)

        return self._get_info_from_bytes(boundary)

    @staticmethod
    def _get_info_from_bytes(boundary):
        if len(boundary) != 2:
            raise ValueError(f'{boundary} is not boundary descriptor')

        info = SFC._get_bin(boundary[0], 8) + SFC._get_bin(boundary[1], 8)[2:]
        is_empty = info[2] == '0'
        size = int(info[3:15], 2) + 1
        number_of_empty_bytes = int(info[15:], 2)

        return is_empty, size, number_of_empty_bytes

    @staticmethod
    def _get_encoded_boundary_descriptor(size, number_of_empty_bytes,
                                         is_empty):
        """returns boundary descriptor (2 bytes) by given <size>,
        <number_of_empty_bytes> and bool <is_empty>"""
        if size < 1 or size > 2**12:
            raise ValueError(f'size out of range(1, {2**12})')

        if number_of_empty_bytes < 0 or number_of_empty_bytes > 7:
            raise ValueError('empty bytes number out of range(8)')

        s = SFC._get_bin(size - 1, 12)
        first = '0b' + ('0' if is_empty else '1') + s[2:9]
        second = '0b' + s[-5:] + SFC._get_bin(number_of_empty_bytes, 3)[2:]

        return int(first, 2), int(second, 2)

    @staticmethod
    def _get_encoded_tables(empty_table, transition_dict):
        """returns bytes of table of empty spots and translation table"""
        bytes_array = bytearray()
        empty_bytes = SFC._encode_empty_table(empty_table)
        len_bytes = struct.pack('h', len(empty_bytes))
        transition_bytes = SFC._encode_transition_table(transition_dict)
        bytes_array.extend(len_bytes)
        bytes_array.extend(empty_bytes)
        bytes_array.extend(transition_bytes)

        return bytes_array

    def get_tables_from_file(self):
        """returns table of empty spots and translation table
        from file in <path>"""
        if not os.path.isfile(self.path):
            raise ValueError(f'{self.path} on such storage file')

        with open(self.path, 'rb') as file:
            file.seek(self.file_length)
            table_bytes = file.read()

        return self._get_tables_from_bytes(table_bytes)

    @staticmethod
    def _get_tables_from_bytes(table_bytes):
        (empty_table_length,) = struct.unpack('h', table_bytes[:2])
        empties = SFC._decode_empty_table(
            table_bytes[2: empty_table_length + 2])
        transitions = SFC._decode_transition_table(
            table_bytes[empty_table_length + 2:])
        return empties, transitions

    @staticmethod
    def _encode_transition_table(transition_dict):
        """returns bytes of encoded translation table"""
        bytes_table = bytearray()

        for key in transition_dict:
            for collision in transition_dict[key]:
                bytes_table.extend(struct.pack('i', key))
                bytes_table.extend(struct.pack('h', collision))

        return bytes_table

    @staticmethod
    def _decode_transition_table(transition_bytes):
        """returns translation table from bytes"""
        table = {}
        index = 0

        while index < len(transition_bytes):
            (key,) = struct.unpack('i', transition_bytes[index:index+4])
            (value,) = struct.unpack('h', transition_bytes[index+4:index+6])

            if key in table:
                table[key].append(value)
            else:
                table[key] = [value]

            index += 6

        return table

    @staticmethod
    def _decode_empty_table(bytes_of_empty_table):
        """returns table of empty spots from bytes"""
        empties = []

        for i in range(0, len(bytes_of_empty_table), 3):
            first = SFC._get_bin(bytes_of_empty_table[i], 8)
            second = SFC._get_bin(bytes_of_empty_table[i + 1], 8)
            third = SFC._get_bin(bytes_of_empty_table[i + 2], 8)
            first_number = int(first + second[2:6], 2) - 1
            second_number = int('0b' + second[6:] + third[2:], 2) - 1
            empties.append(first_number)

            if second_number >= 0:
                empties.append(second_number)

        return empties

    @staticmethod
    def _encode_empty_table(emptyes_table):
        """returns bytes of table of empty spots"""
        bytes_table = bytearray()
        for i in range(0, len(emptyes_table), 2):

            if emptyes_table[i] >= 4095 or emptyes_table[i] < 0:
                raise ValueError(
                    f'tables elenemt on position {i} is out of range(4095)')

            if i+1 < len(emptyes_table) \
                    and (emptyes_table[i+1] >= 4095 or emptyes_table[i+1] < 0):
                raise ValueError(
                    f'tables elenemt on position {i+1} is out of range(4095)')

            first = SFC._get_bin(emptyes_table[i] + 1, 12)
            bytes_table.append(int(first[:10], 2))

            if i + 1 == len(emptyes_table):
                next_byte = SFC._get_bin(0, 12)
            else:
                next_byte = SFC._get_bin(emptyes_table[i + 1] + 1, 12)

            second = '0b' + first[10:] + next_byte[2:6]
            third = '0b' + next_byte[6:]
            bytes_table.append(int(second, 2))
            bytes_table.append(int(third, 2))

        return bytes_table

    @staticmethod
    def _get_bin(num, length=None):
        """converting <num> to binary with given <length>
        (adding '0' and removing symbols from start of binary string
        if length doesn't feat)"""
        bin_str = bin(num)
        if length is None:
            return bin_str

        if length >= len(bin_str[2:]):
            return '0b' + '0' * (length - len(bin_str[2:])) + bin_str[2:]

        return '0b' + bin_str[len(bin_str) - length:]
