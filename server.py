from server.http_server import HTTPServer

if __name__ == '__main__':
    server = HTTPServer("127.0.0.1", 8000)
    server.start()