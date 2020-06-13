import socket
import sys

class TCPServer:
    def __init__(
        self,
        host: str,
        port: int
    ) -> None:
        self.host = host
        self.port = port
        self.PACKET_SIZE = 4096

    def start(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        # configure how many client the server can listen simultaneously
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(self.PACKET_SIZE)
            sys.stdout.buffer.write(data)
            response = self.handle_request(data)
            conn.sendall(response.encode())
            conn.close()

    def handle_request(self, data: bytes) -> bytes:
        """
        Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data