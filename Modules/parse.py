import struct
from Modules.single_file_controller import NUMBER_OF_KBYTES
import hashlib

ENCODING = 'utf-8'


def encode_pair(key, value):
    key_data = encode_key(key)
    value_bytes = encode_value(value)
    key_data.extend(value_bytes)
    return key_data


def encode_value(value):
    return bytearray(value.encode(ENCODING))


def encode_key(key):
    key_bytes = bytearray(key.encode(ENCODING))
    if len(key_bytes) >= NUMBER_OF_KBYTES * 1024 - 1:
        raise ValueError('key is to big')

    key_len = bytearray(struct.pack('h', len(key_bytes)))
    key_len.extend(key_bytes)
    return key_len


def get_key(b):
    (length,) = struct.unpack('h', b[:2])
    return b[2:2+length].decode(ENCODING)


def get_value_bytes(b):
    (length,) = struct.unpack('h', b[:2])
    value = b[2+length:]
    return value


def decode_pair(b):
    key = get_key(b)
    value = get_value_bytes(b).decode(ENCODING)
    return key, value


def get_value(b):
    return b.decode(ENCODING)


def get_index(key):
    key_hash = int(hashlib.md5(key.encode(ENCODING)).hexdigest(), 16)
    index = key_hash % (2**32)
    index -= 2**31
    return index
