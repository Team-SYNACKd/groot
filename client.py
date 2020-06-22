import sys
import argparse
import logging

from client.http_client import HTTPClient

from common.url import URL
from common.http import HTTPRequest

logger = logging.getLogger("Client")

def main():
    parser = argparse.ArgumentParser(description="HTTP/1.1 client")
    parser.add_argument(
        "url", type=str, nargs="+", help="the URL to query (must be HTTP as of now)"
    )
    parser.add_argument(
        "--port", type=int, help="local port to bind for connections",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase logging verbosity"
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    for url in args.url:
        logger.info("sending request to {}\n".format(url))
        request = HTTPRequest(uri=URL(url))
        client = HTTPClient(request)

        #TODO: return a Response object
        req = client.get()

        sys.stdout.buffer.write(req.headers)
        if req.content_length > 0:
            sys.stdout.buffer.write(req.body)


if __name__ == '__main__':
    main()
