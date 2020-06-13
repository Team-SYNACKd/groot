class HTTPRequest:
    def __init__(self, data: bytes):
        self.method = None
        self.uri = None
        self.http_version = '1.1' # default to HTTP/1.1 if request doesn't provide a version
        self.headers = {} # a dictionary for headers

        # call self.parse method to parse the request data
        self.parse(data)

    def parse(self, data: bytes):
        lines = data.decode('utf8').split('\r\n')

        request_line = lines[0]
        self.parse_request_line(request_line)

    def parse_request_line(self, request_line):
        words = request_line.split(' ')
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.http_version = words[2]