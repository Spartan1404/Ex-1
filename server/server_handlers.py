import logging
import struct
import sys

from server_logic import calc_ponderation


class Handler:
    """
    Server handler interface
    """
    def handle(self, client_sock):
        pass  # Placeholder method to be overridden by child classes


class PonderationChainHandler(Handler):
    """
    Class to handle the "ponderation-chains" server functionality
    """
    def handle(self, client_sock):
        logger = logging.getLogger('server')
        try:
            dl_data = client_sock.recv(4)
            data_length = struct.unpack('!i', dl_data)[0]
            data = recvall(client_sock, data_length).decode()
            chains = data.split('\n')
            pond = [calc_ponderation(c) for c in chains]

            response = '\n'.join([str(w) for w in pond])

            response_len = struct.pack('>I', len(response))

            client_sock.sendall(response_len)
            client_sock.sendall(response.encode())
            logger.info("closing connection")
            client_sock.close()
        except Exception as e:
            logger.exception(e)


def recvall(sock, n: int):
    """
    Helper function to recv n bytes or return None if EOF is hit
    :param sock: The client socket
    :param n: The amount of bytes to receive
    :return: The complete data or None
    """
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
