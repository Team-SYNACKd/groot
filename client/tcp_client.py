import socket
from http_client import HTTPClient, HTTPRequest

class TCPClient(HTTPClient):
    def __init__(self) -> None:
        self.PACKET_SIZE = 4096

    def start(self) -> None:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # connect the client 
        c.connect((self.host, self.port))
        
        # send some data
        request = HTTPRequest(self.host, self.port, "/")
        req = request.perform_http_request()
        c.send(req.encode())

        # receive some data 
        response = c.recv(self.PACKET_SIZE)  
        http_response = repr(response)
        http_response_len = len(http_response)
        print(http_response)

    def _request(self) -> str:
        '''
        Override this in subclass.
        '''
        return 'GET / HTTP/1.0\r\nHost: {}\r\n\r\n'.format(self.host)