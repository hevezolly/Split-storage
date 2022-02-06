import socket


def recv(connection: socket.socket, num_bytes: int, rise=False):
    data = []
    length_to_recv = num_bytes
    while length_to_recv:
        try:
            data_part = connection.recv(length_to_recv)
            if not data_part:
                raise socket.error('connection was closed')
            length_to_recv -= len(data_part)
            data.append(data_part)
        except socket.error:
            if rise:
                raise
            return None
    return b''.join(data)
