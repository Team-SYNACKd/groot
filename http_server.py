from tcp_server import TCPServer

class HTTPServer(TCPServer):
    status_codes = {
        200: 'OK',
        404: 'Not Found',
    }

    def handle_request(self, data) -> str:
        response = (
            'HTTP/1.1 200 OK\r\n', # response line
            '\r\n', # blank line
            'Request received!' # response body
        )
        #return "".join(response).encode()
        return "".join(response)