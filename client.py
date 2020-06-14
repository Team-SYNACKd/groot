import sys

from client.http_client import HTTPClient
from http_common import URL, HTTPRequest

if __name__ == '__main__':
    request = HTTPRequest(uri=URL("http://www.google.co.in"))
    client = HTTPClient(request)

    #TODO: return a Response object
    req = client.get()

    sys.stdout.buffer.write(req.headers)
    if req.content_length > 0:
        sys.stdout.buffer.write(req.content)
