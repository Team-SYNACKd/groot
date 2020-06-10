import socket

class TCPClient:
    def __init__(
        self,
        host: str,
        port: int
    ) -> None:
        self.host = host
        self.port = port
        self.PACKET_SIZE = 4096

    def start(self) -> None:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # connect the client 
        c.connect((self.host, self.port))
        
        # send some data 
        request = self.handle_request(host=self.host)
        c.send(request.encode())

        # receive some data 
        response = c.recv(self.PACKET_SIZE)  
        http_response = repr(response)
        http_response_len = len(http_response)
        print(http_response)

    def handle_request(
        self,
        host: str
    ) -> str:
        return host
