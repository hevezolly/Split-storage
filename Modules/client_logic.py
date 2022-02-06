import socket
import sys
import struct
from Modules.socket_controller import recv
import shlex
from MainServer import get_administrator_parser, get_user_parser


class ClientLogic:

    @staticmethod
    def get_parser(is_administrator):
        if is_administrator:
            parser = get_administrator_parser()
        else:
            parser = get_user_parser()
        parser.add_argument('-h', '--help', action='help')
        return parser

    @staticmethod
    def parse(is_administrator):
        sock = socket.socket()
        parser = ClientLogic.get_parser(is_administrator)
        args = parser.parse_args()
        if len(sys.argv) == 3:
            print(parser.format_help())
            return
        sock.connect((args.HOST, args.PORT))
        message = ' '.join(map(shlex.quote, sys.argv[1:]))
        data = message.encode('utf8')
        length = struct.pack('i', len(data) + 1)
        is_adm = struct.pack('?', is_administrator)
        sock.sendall(length + is_adm + data)
        answer = recv(sock, 4)
        if answer:
            length, = struct.unpack('i', answer)
            if length <= 0:
                return
            data = recv(sock, length)
            if not data:
                print('connection was failed')
                return
            print(data.decode('utf8'))
        else:
            print('connection was failed')
