import sys

from http_client import HTTPClient

if __name__ == '__main__':
    response = HTTPClient.get(host='www.google.co.in', resource="/")
    # output the response body (or the header if there is no body)
    if response.content_length > 0:
        output = response.body
    else:
        output = response.header
    sys.stdout.buffer.write(output)