import socket
import sys

sys.path.append("..")
from http_common import HTTPRequest

class TCPClient:
    def __init__(
        self,
        host,
        port,
        resource
    ) -> None:
        self.host = host
        self.port = port
        self.resource = resource
        self.TCP_FASTOPEN = 23
        self.qlen = 5 # queue length for number of TFO request
        self.PACKET_SIZE = 4096

    def connect(self, host: str, port: int) -> socket:
        ip = self.getaddrinfo(host)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.setsockopt(socket.SOL_TCP, self.TCP_FASTOPEN, self.qlen)
        sock.connect((ip, port))
        return sock

    # TODO: Improve this
    def getaddrinfo(self, host: str):
        ip = socket.gethostbyname(host)
        return ip

    def send_request(self, sock, method = 'GET'):
        sock.sendall(
            self.perform_http_request(self.host, self.resource, method)
        )

    def read_until(self, sock, condition, length_start=0, chunk_size=4096):
        data = bytes()
        chunk = bytes()
        length = length_start
        try:
            while not condition(length, chunk):
                chunk = sock.recv(chunk_size)
                if not chunk:
                    break
                else:
                    data += chunk
                    length += len(chunk)
        except socket.timeout:
            pass
        return data

    def perform_http_request(self, host, resource, method):
        return
