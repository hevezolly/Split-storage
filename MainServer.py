from Modules.MainNodeClient import MainNodeClient, ImportantNodesDisconnected
import argparse
import struct
import socket
import shlex
from Modules.socket_controller import recv

MAX_GROUP_LENGTH = 4


def get_user_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('HOST', help='server host')
    parser.add_argument('PORT', help='server host', type=int)
    parser.add_argument('-w', '--write', nargs=2, metavar=('KEY', 'VALUE'),
                        help='writes VALUE by KEY')
    parser.add_argument('-r', '--read', metavar='KEY',
                        help='reads value by KEY')
    parser.add_argument('-e', '--empty', metavar='KEY',
                        help='deletes value by KEY')
    return parser


def get_administrator_parser():
    parser = get_user_parser()
    parser.add_argument('-c', '--connect', metavar='INDEX',
                        help='connects to existing node by INDEX')
    parser.add_argument('-n', '--connect_new', nargs=2,
                        metavar=('HOST', 'PORT'),
                        help='connects to new node by HOST and PORT')
    parser.add_argument('-s', '--shut', action='store_true', default=False,
                        help='turns server off')
    parser.add_argument('-d', '--disconnect', metavar='INDEX',
                        help='disconnects node by INDEX')
    parser.add_argument('-i', '--indexes', action='store_true',
                        default=False,
                        help='prints indexes of active nodes')
    return parser


class MainServer:
    def __init__(self, directory, host_port, create_new=False):
        self.client = MainNodeClient(directory, create_new)
        self.socket = socket.socket()
        self.socket.bind(host_port)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.listen(5)
        self.is_running = True
        self.start()

    def get_composition(self):
        self.client.ping()
        return list(self.client.get_active_indexes())

    @staticmethod
    def _send(connection, line):
        data = line.encode('utf8')
        length = struct.pack('i', len(data))
        connection.sendall(length+data)

    def start(self):
        while self.is_running:
            connection, addr = self.socket.accept()
            print(f'{addr} just connected')
            self.recive_msg(connection)
            connection.close()
            print(f'request from {addr} was finished')

    def recive_msg(self, connection):
        first_data = recv(connection, 4)
        if first_data is None:
            return None
        length, = struct.unpack('i', first_data)
        if length <= 0:
            self.socket.close()
        data = recv(connection, length)
        if data is None:
            return
        is_administrator, = struct.unpack('?', data[0:1])
        parser = get_user_parser()
        if is_administrator:
            parser = get_administrator_parser()
        msg = data[1:].decode('utf8')
        parsed_msg = shlex.split(msg)
        print('get message:')
        print(' '.join(map(shlex.quote, parsed_msg)))
        args = parser.parse_args(parsed_msg)
        try:
            result = self.process_args(args)
        except ImportantNodesDisconnected as e:
            result = str(e)
        if result is None:
            self._send(connection, '')
            return
        self._send(connection, result)

    def process_args(self, args):
        try:
            if args.write is not None:
                composition = self.get_composition()
                print(composition)
                self.client.add_key_with_composition(
                    args.write[0], args.write[1], composition)
                return None
            elif args.read is not None:
                return self.client.get_key(args.read)
            elif args.empty is not None:
                self.client.delete_key(args.empty)
                return None
            elif args.connect is not None:
                self.client.connect_to_node(int(args.connect[0]))
                return None
            elif args.shut:
                self.client.disconnect_all(True)
                self.is_running = False
                return None
            elif args.disconnect is not None:
                self.client.ping()
                self.client.disconnect(int(args.disconnect), True)
                return None
            elif args.indexes:
                self.client.ping()
                indexes = list(self.client.get_active_indexes())
                str_indexes = ' '.join(map(str, indexes))
                return 'active indexes: \n'+str_indexes
            elif args.connect_new is not None:
                success = self.client.connect_to_new_node(
                    args.connect_new[0], int(args.connect_new[1]))
                if success:
                    return 'node was connected'
                return 'failed to connect to node'
            raise ValueError('incorrect params')
        except Exception as e:
            return str(e)


class ArgumentException(Exception):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('DIRECTORY', help='path to main directory')
    parser.add_argument('PORT', help='socket port', type=int)
    parser.add_argument('--host', metavar='HOST',
                        help='socket host', default='localhost')
    parser.add_argument('-c', '--create_new', action='store_true',
                        default=False)
    args = parser.parse_args()
    server = MainServer(args.DIRECTORY, (args.host, args.PORT),
                        args.create_new)
