import socket
import threading


class Server:

    def __init__(self, workers=1, host='127.0.0.1', port=2000) -> None:
        self.host = host
        self.port = port
        self.workers = workers
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def start(self):
        self.socket.listen(5)
        while True:
            client_socket, address = self.socket.accept()
            thread = threading.Thread(target=self._listen_client, args=(client_socket, address))
            thread.start()
            print(f"[NEW CONNECTION {address}] - Thread {thread.native_id}")

    def _listen_client(self, client_socket, addres):
        while True:
            try:
                data = client_socket.recv(4096)
                if data:
                    client_socket.send('[SERVER] - Data from server: '.encode() + data)
                    print(data.decode('utf-8'))
                else:
                    raise Exception('Client disconnected')
            except:
                client_socket.close()
                return False
                


if __name__ == "__main__":
    server = Server()
    server.start()
