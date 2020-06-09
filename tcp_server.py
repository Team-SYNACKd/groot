import socket

class TCPServer:
    def __init__(
        self,
        host: str,
        port: int) -> None:
        self.host = host
        self.port = port

    def start(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024)
            response = self.handle_request(data)
            conn.sendall(response.encode())
            conn.close()

    def handle_request(self, data) -> str:
        """
        Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data