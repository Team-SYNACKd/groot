from .url import URL

class HTTPRequest:
    def __init__(self, uri: URL, method: str = None, data: bytes = b''):
        self.uri = uri
        self.host = uri.host
        self.port = uri.port
        self.resource = uri.full_path
        self.method = method
        self.http_version = '1.1' # default to HTTP/1.1 if request doesn't provide a version
        self.headers = {} # a dictionary for headers
        self.data = data #stores the request data send to the server to be parsed.
        self.content_length = 0
        self.body = bytes()

        self.http_header_delimiter = b'\r\n\r\n'
        self.content_length_field = b'Content-Length:'

    '''
    _read_request() function is an internal API used to parse
    the request received at the server and to determine
    what sort of HTTP method the client connecting to our
    server is requesting for.
    '''
    def _read_request(self, request: bytes):
        lines = request.decode('utf8').split('\r\n')

        request_line = lines[0]
        words = request_line.split(' ')
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.http_version = words[2]
