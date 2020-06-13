import sys
sys.path.append("..")
from http_common import URL

import socket
from typing import Tuple
from urllib.parse import urlparse

class HTTPClient:
    def __init__(
        self,
        host: str = None,
        resource: str = None,
        header: bytes = b'',
        content: bytes = b'',
        content_length: int = 0
    ) -> None:
        self.host = host
        self.resource = resource
        self.header = header
        self.content_length = content_length
        self.content = content
        
        self.http_header_delimiter = b'\r\n\r\n'
        self.content_length_field = b'Content-Length:'

    def formatted_http_request(self, host: str, resource: str, method: str ='GET') -> str:
        request =  '{} {} HTTP/1.1\r\nhost: {}\r\n\r\n'.format(method,
                                                 resource,
                                                 host)
        return request.encode()
        
    def end_of_header(self, length: int, data: bytes) -> str:
        return b'\r\n\r\n' in data

    def end_of_content(self, length: int, data: bytes) -> str:
        return self.content_length <= length

    def separate_header_and_body(self, data: bytes) -> Tuple[bytes, bytes]:
        try:
            index = data.index(self.http_header_delimiter)
        except:
            return (data, bytes())
        else:
            index += len(self.http_header_delimiter)
            return (data[:index], data[index:])

    def get_content_length(self, header: bytes) -> int:
        for line in header.split(b'\r\n'):
            if self.content_length_field in line:
                return int(line[len(self.content_length_field):])
        return 0

    def send(self, sock: socket, method: str ='GET') -> None:
        sock.sendall(self.formatted_http_request(self.host, self.resource, method))

    def read_until(self, sock: socket, condition, length_start: int = 0, chunk_size: int = 4096) -> bytes:
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

    def recv(self, sock: socket) -> Tuple[bytes, bytes]:
        '''
        Reads an HTTP Response from the given socket. Returns that response as a
        tuple (header, body) as two sequences of bytes.
        '''
        #read until at end of header
        self.data = self.read_until(sock, self.end_of_header)
        #separate our body and header
        self.header, self.content = self.separate_header_and_body(self.data)

        self.content_length = self.get_content_length(self.header)

        # read until end of Content Length
        self.content += self.read_until(sock, self.end_of_content, len(self.content))
        return (self.header, self.content)

    '''
    Creates a new HTTPResource with the given host and request, then tries
    to resolve the host, send the request and receive the response. The
    downloaded HTTPResource is then returned.
    '''
    def get(self, url: URL) -> None:
        self.host = url.host
        self.resource = url.full_path
        try:
            ip = socket.gethostbyname(url.host)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, url.port))
            self.send(sock)
            self.recv(sock)
        except Exception as e:
            raise e



