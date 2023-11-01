import socket
import threading
import queue
import json
import argparse


class Client:
    def __init__(self, threads_number, file, host="127.0.0.1", port=3000):
        self.threads_number = threads_number
        self.file = file
        self.host = host
        self.port = port
        self.url_queue = queue.Queue()

    def start(self):
        threads = [
            threading.Thread(
                target=self.send_url_and_receive_data, name=f"Thread - {i+1}"
            )
            for i in range(self.threads_number)
        ]

        for thread in threads:
            thread.start()

        self.fetch_urls()

        for thread in threads:
            thread.join()

        self.shutdown_server()

    def send_url_and_receive_data(self):
        while True:
            try:
                url = self.url_queue.get(timeout=1)
            except queue.Empty:
                continue

            if url is None:
                self.url_queue.put(None)
                break

            client_socket = None
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.port))
                client_socket.send(url.encode("utf-8"))

                data = json.loads(client_socket.recv(4096).decode("utf-8"))
                print(f"{url}: {data}")
            except (socket.error, json.JSONDecodeError) as exception:
                print(
                    f"Error in thread - {threading.current_thread().name}: {exception}"
                )
                continue
            finally:
                if client_socket:
                    client_socket.close()

    def fetch_urls(self):
        with open(file=self.file, encoding="utf-8") as file_object:
            for url in file_object:
                self.url_queue.put(url.strip())
        self.url_queue.put(None)

    def shutdown_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        client_socket.send("SHUTDOWN".encode("utf-8"))
        client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-threaded client for sending urls to the server"
    )
    parser.add_argument("threads_number", type=int, help="Number of threads")
    parser.add_argument("filename", help="File with URLs to send")
    args = parser.parse_args()

    client = Client(args.threads_number, args.filename)
    client.start()
