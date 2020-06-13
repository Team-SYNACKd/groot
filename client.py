import sys

from client.http_client import HTTPClient
from http_common import URL

if __name__ == '__main__':
    client = HTTPClient()

    #TODO: return a Response object
    client.get(url=URL("http://www.google.co.in"))

    if client.content_length > 0:
        output = client.body
    else:
        output = client.header
    sys.stdout.buffer.write(output)