import socket
# from urllib.parse import urlparse

# class URL:
#     def __init__(self, url: str) -> None:
#         parsed = urlparse(url)

#         self.authority = parsed.netloc
#         self.full_path = parsed.path
#         if parsed.query:
#             self.full_path += "?" + parsed.query
#         self.scheme = parsed.scheme


class HTTPClient:
    def __init__(self, host, resource):
        self.host = host
        self.resource = resource
        self.header = bytes()
        self.content_length = 0
        self.body = bytes()
        
        self.http_header_delimiter = b'\r\n\r\n'
        self.content_length_field = b'Content-Length:'

    def formatted_http_request(self, host, resource, method='GET'):
        request =  '{} {} HTTP/1.1\r\nhost: {}\r\n\r\n'.format(method,
                                                 resource,
                                                 host)
        return request.encode()
        
    def end_of_header(self, length, data):
        return b'\r\n\r\n' in data

    def end_of_content(self, length, data):
        return self.content_length <= length

    def separate_header_and_body(self, data):
        try:
            index = data.index(self.http_header_delimiter)
        except:
            return (data, bytes())
        else:
            index += len(self.http_header_delimiter)
            return (data[:index], data[index:])

    def get_content_length(self, header):
        for line in header.split(b'\r\n'):
            if self.content_length_field in line:
                return int(line[len(self.content_length_field):])
        return 0

    def send(self, sock, method='GET'):
        sock.sendall(self.formatted_http_request(self.host, self.resource, method))

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

    def recv(self, sock):
        '''
        Reads an HTTP Response from the given socket. Returns that response as a
        tuple (header, body) as two sequences of bytes.
        '''
        #read until at end of header
        self.data = self.read_until(sock, self.end_of_header)
        #separate our body and header
        self.header, self.body = self.separate_header_and_body(self.data)

        self.content_length = self.get_content_length(self.header)

        # read until end of Content Length
        self.body += self.read_until(sock, self.end_of_content, len(self.body))

        return (self.header, self.body)

    @classmethod
    def get(cls, host, resource):
        '''
        Creates a new HTTPResource with the given host and request, then tries
        to resolve the host, send the request and receive the response. The
        downloaded HTTPResource is then returned.
        '''
        http = cls(host, resource)
        port = 80
        try:
            ip = socket.gethostbyname(host)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            http.send(sock)
            http.recv(sock)
        except Exception as e:
            raise e
        return http



