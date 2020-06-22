import argparse

from server.http_server import HTTPServer

def main():
    parser = argparse.ArgumentParser(description="HTTP/1.1 server")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="listen on the specified address (defaults to ::)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="listen on the specified port (defaults to 8080)",
    )
    args = parser.parse_args()

    server = HTTPServer(args.host, args.port)
    server.start()

if __name__ == '__main__':
    main()
