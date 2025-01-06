import argparse
import socket
import threading
import ssl
import sys
import logging
import os
import select
from server_handlers import PonderationChainHandler


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
    logger = logging.getLogger('server')
    logger.addHandler(log_handler)
    log_level = logging.getLevelName(log_level_str.upper())
    logger.setLevel(log_level)
    return logger


class HandlerFactory:
    @staticmethod
    def create_handler(functionality):
        match functionality:
            case "ponderation-chains":
                return PonderationChainHandler()
            case _:
                raise ValueError("Unknown functionality")


class Server:
    def __init__(self, host, port, logger: logging.Logger):
        self.host = host
        self.port = port
        self.logger = logger
        self.dirname = os.path.dirname(__file__)
        self.functionalities = ["ponderation-chains"]

    def ssl_wrap(self, sock):
        """
        Wrap the socket with ssl to establish a secure connection
        :param sock: The socket to be wrapped
        :return: A secure SSLSocket
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.check_hostname = False

        context.load_cert_chain(os.path.join(self.dirname, 'certs/cert.pem'), os.path.join(self.dirname, 'certs/key.pem'))
        ssock = context.wrap_socket(sock, server_side=True)
        return ssock

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.host, self.port))
                self.logger.info(f"Server running on address: {self.host}, port: {self.port}")
                sock.listen()
                sock = self.ssl_wrap(sock)
                while True:
                    conn, addr = sock.accept()
                    self.logger.info(f"New connection from {addr}")
                    try:
                        key_length = conn.recv(1)[0]
                        key = conn.recv(key_length).decode()
                        if key in self.functionalities:
                            conn.sendall(b'\x00')
                            handler = HandlerFactory.create_handler(key)
                            self.logger.info(f"Executing functionality: {key}")
                            self.logger.info(f"Creating new thread, number of current threads is: {threading.active_count()}")
                            thread = threading.Thread(target=handler.handle, args=(conn,))
                            thread.start()
                        else:
                            self.logger.error(f"Functionality '{key}' not found, request made by {addr}")
                            conn.sendall(b'\xFF')
                    except Exception as e:
                        conn.sendall(b'\x01')
                        self.logger.exception(e)
        except KeyboardInterrupt:
            pass


def main(args):
    dirname = os.path.dirname(__file__)
    logger = make_logger(log_path=os.path.join(dirname, 'server_log.txt'))
    server = Server(args.host, args.port, logger)
    server.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server process")

    parser.add_argument('-s', '--host', action='store', default='127.0.0.1',
                        help='IP/Hostname to serve on', type=str)
    parser.add_argument('-p', '--port', action='store', default=3000,
                        help='Port to serve on', type=int)
    args = parser.parse_args()
    main(args)
