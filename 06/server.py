import re
import socket
import threading
import json
from collections import Counter
import queue
import argparse
import requests
from bs4 import BeautifulSoup


class Server:
    URL_PATTERN = r"https?://\S+"

    def __init__(
        self, workers_number, most_common_words_number, host="127.0.0.1", port=3000
    ) -> None:
        self.workers_number = workers_number
        self.most_common_words_number = most_common_words_number
        self.host = host
        self.port = port

        self.init_server_components()
        self.init_socket()

    def init_server_components(self):
        self.clients_queue = queue.Queue()
        self.count_urls = 0
        self.shutdown_event = threading.Event()
        self.lock = threading.Lock()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)

    def start(self):
        master = threading.Thread(target=self.listen_client_connection, name="Master")
        master.start()

        workers = [
            threading.Thread(target=self.process_url, name=f"Worker {i+1}")
            for i in range(self.workers_number)
        ]

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

        master.join()
        self.socket.close()

    def listen_client_connection(self):
        self.socket.listen()
        while not self.shutdown_event.is_set():
            try:
                client_socket, _ = self.socket.accept()
                self.clients_queue.put(client_socket)
            except Exception:
                continue

    def process_url(self):
        while not self.shutdown_event.is_set():
            try:
                client_socket = self.clients_queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                url = client_socket.recv(4096).decode("utf-8")
                if url == "SHUTDOWN":
                    self.shutdown_event.set()
                    break

                if url is None or not re.match(self.URL_PATTERN, url):
                    data = "URL is broken"
                else:
                    page_text = self.get_text_from_html(url)
                    data = self.get_most_common_words(page_text)

                client_socket.send(data.encode("utf-8"))

                with self.lock:
                    client_socket.close()
                    self.count_urls += 1
                    print(f"Proccessed {self.count_urls} urls")
            except socket.error as exception:
                print(f"Socket error processing URL - {exception}")
                continue

    def get_text_from_html(self, url):
        try:
            response = requests.get(url, timeout=1)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            page_text = soup.get_text()
            return page_text
        except requests.exceptions.RequestException as exception:
            print(f"Requests error processing URL - {exception}")
        return None

    def get_most_common_words(self, text):
        if text:
            words = re.findall(r"\b[А-Яа-яA-Za-z]+\b", text.lower())
            most_common_words = Counter(words).most_common(
                self.most_common_words_number
            )
            most_common_words_json = json.dumps(dict(most_common_words))
            return most_common_words_json
        return "Data is broken"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Master-worker server for processing urls"
    )
    parser.add_argument("-w", type=int, help="Number of workers")
    parser.add_argument("-k", type=int, help="Number of most common words")
    args = parser.parse_args()

    server = Server(args.w, args.k)
    server.start()
