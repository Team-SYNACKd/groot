from tcp_client import TCPClient

if __name__ == "__main__":
    client = TCPClient("127.0.0.1", 8000)
    client.start()