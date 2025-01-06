import argparse
import socket
import logging
import struct
import time
import ssl
import sys
import os
from client_logic import generate_chain_file, DEFAULT_CHARS


def make_logger(log_path=None, log_level_str='INFO'):
    """
    Helper function to initialize the logger
    :param log_path: Path for the log file. Will print the log in the console if left None
    :param log_level_str: Sets the minimum level to log
    :return: The configured log object
    """
    formatter = logging.Formatter('%(asctime)s: %(name)s (%(levelname)s): %(message)s')
    if log_path:
        log_handler = logging.FileHandler(log_path)
    else:
        log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(formatter)
    logger = logging.getLogger('client')
    logger.addHandler(log_handler)
    log_level = logging.getLevelName(log_level_str.upper())
    logger.setLevel(log_level)
    return logger


class Client:
    def __init__(self, logger: logging.Logger, server_ip: str = 'localhost', server_port: int = 3000):
        self.server_ip = server_ip
        self.server_port = server_port
        self.logger = logger
        self.dirname = os.path.dirname(__file__)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def ssl_wrap(self):
        self.logger.info('Creating SSL context')
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.load_verify_locations(os.path.join(self.dirname, 'certs/cert.pem'))
        self.logger.info('Wrapping socket in SSL')
        self.socket = context.wrap_socket(self.socket, server_hostname=self.server_ip)

    def connect(self):
        self.ssl_wrap()
        self.logger.info(f'Connecting to server on address: {self.server_ip}, port: {self.server_port}')
        self.socket.connect((self.server_ip, self.server_port))

    def send_file_to_server(self, filename):
        """
        Method to execute the functionality "ponderation-chains" from the server
        :param filename: Name of the file to be sent to the server
        :return: True if the process was completed successfully, False if otherwise
        """
        try:
            prc = 'ponderation-chains'

            self.socket.sendall(bytes([len(prc)]))
            self.socket.sendall(prc.encode())

            confirmation = self.socket.recv(1)
            if confirmation == b'\xFF':
                self.logger.error("Server does not have the requested functionality, shutting down")
                return False
            if confirmation == b'\x01':
                self.logger.error("An unknown error happened in the server, shutting down")
                return False

            self.logger.info("Request accepted, reading and sending file")
            with open(filename, 'r') as file:
                data = file.read()

            msg = struct.pack('!i', len(data))
            self.socket.sendall(msg)
            self.socket.sendall(data.encode())
            self.logger.info("File sent to the server")

            response_length_data = self.socket.recv(4)
            response_length = struct.unpack('>I', response_length_data)[0]
            response = self.recvall(response_length).decode()
            with open(os.path.join(self.dirname, 'response.txt'), 'w') as resp_file:
                resp_file.write(response)
            self.logger.info("Response received and saved to response.txt")
            self.logger.info("Shutting down")
            self.socket.close()
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def recvall(self, n: int):
        """
        Helper function to recv n bytes or return None if EOF is hit
        :param n: The amount of bytes to receive
        :return: The complete data or None
        """
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def generate_file(self,
                      amount: int = 1000000,
                      min_length: int = 50,
                      max_length: int = 100,
                      chars: str = DEFAULT_CHARS,
                      min_spaces: int = 3,
                      max_spaces: int = 5,
                      filename: str = 'chains.txt'):
        path = os.path.join(self.dirname, filename)
        generate_chain_file(amount=amount, chain_min_length=min_length, chain_max_length=max_length, chain_chars=chars,
                            chain_min_spaces=min_spaces, chain_max_spaces=max_spaces, filename=path)


def main(args):
    start_time = time.time()
    dirname = os.path.dirname(__file__)
    logger = make_logger(log_path=os.path.join(dirname, 'client_log.txt'))
    client = Client(server_ip=args.host, server_port=args.port, logger=logger)
    client.connect()
    client.generate_file(amount=args.amount,
                         min_length=args.min_length,
                         max_length=args.max_length,
                         min_spaces=args.min_spaces,
                         max_spaces=args.max_spaces,
                         chars=args.chars,
                         filename=args.filename)
    client.send_file_to_server(os.path.join(dirname, args.filename))
    end_time = time.time()
    logger.info(f"Process completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client process")

    parser.add_argument('-s', '--host', action='store', default='127.0.0.1',
                        help='IP/Hostname of the server', type=str)
    parser.add_argument('-p', '--port', action='store', default=3000,
                        help='Port of the server', type=int)
    parser.add_argument('-a', '--amount', action='store', default=1000000,
                        help='Amount of strings to generate', type=int)
    parser.add_argument('-ln', '--min-length', action='store', default=50,
                        help='Minimum size of the generated strings', type=int)
    parser.add_argument('-lm', '--max-length', action='store', default=100,
                        help='Maximum size of the generated strings', type=int)
    parser.add_argument('-sn', '--min-spaces', action='store', default=3,
                        help='Minimum amount of spaces (" ") to be included in the generated strings', type=int)
    parser.add_argument('-sm', '--max-spaces', action='store', default=5,
                        help='Maximum amount of spaces (" ") to be included in the generated strings', type=int)
    parser.add_argument('-c', '--chars', action='store', default=DEFAULT_CHARS,
                        help='List of characters to pick randomly from when creating the string', type=str)
    parser.add_argument('-f', '--filename', action='store', default='chains.txt',
                        help='Name of the file where the strings will be stored', type=str)
    args = parser.parse_args()

    main(args)
