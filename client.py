import sys
import argparse

from client.http_client import HTTPClient

from common.url import URL
from common.http import HTTPRequest

def main():
    parser = argparse.ArgumentParser(description="HTTP/1.1 client")
    parser.add_argument(
        "url", type=str, nargs="+", help="the URL to query (must be HTTP as of now)"
    )
    parser.add_argument(
        "--port", type=int, help="local port to bind for connections",
    )

    args = parser.parse_args()

    for url in args.url:
        print("sending request to {}\n".format(url))
        request = HTTPRequest(uri=URL(url))
        client = HTTPClient(request)

        #TODO: return a Response object
        req = client.get()

        sys.stdout.buffer.write(req.headers)
        if req.content_length > 0:
            sys.stdout.buffer.write(req.body)


if __name__ == '__main__':
    main()
