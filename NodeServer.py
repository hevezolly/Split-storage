import socket
import struct
import argparse
import shlex
from Modules.socket_controller import recv
from node import Node


class NodeServer:
    def __init__(self, path, host, port):
        self.node = Node(path)
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.start()

    @staticmethod
    def send_line(connection, line):
        encoded = line.encode('utf8')
        length = struct.pack('i', len(encoded))
        connection.sendall(length+encoded)

    def start(self):
        parser = Node.get_parser()
        while True:
            connection, addr = self.socket.accept()
            print(f'{addr} just connected')
            while True:
                data = recv(connection, 4)
                if not data:
                    break
                length, = struct.unpack('i', data)
                if length <= 0:
                    self.socket.close()
                    return
                message = recv(connection, length)
                if not message:
                    break
                message = message.decode("utf8")
                parsed_message = shlex.split(message)
                print(parsed_message)
                print('get message:')
                print(' '.join(map(shlex.quote, parsed_message)))
                if parsed_message == ['ping']:
                    self.send_line(connection, 'ping')
                    self.send_line(connection, '')
                    continue
                answer = self.node.process_args(parser.parse_args(
                    parsed_message))
                if answer is not None:
                    for line in answer:
                        self.send_line(connection, line)
                self.send_line(connection, '')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('DIRECTORY', help='path to node')
    parser.add_argument('PORT', help='server port')
    parser.add_argument('--host', metavar='HOST',
                        default='localhost',
                        help='host')

    args = parser.parse_args()
    server = NodeServer(args.DIRECTORY, args.host, int(args.PORT))
