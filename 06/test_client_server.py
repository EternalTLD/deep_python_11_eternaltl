from io import StringIO
import queue
import socket
import threading
import time

import pytest
from client import Client
from server import Server
from unittest import mock
from requests import Response


def test_client(mocker, capsys):
    urls = []
    with open('06/urls.txt', 'r') as file_object:
        for url in file_object:
            urls.append(url.strip())
    urls.append("SHUTDOWN")

    expected_recv_data = [url + ": {'word1': 6, 'word2': 5}" for url in urls if url != "SHUTDOWN"]
    expected_send_data = [url.encode("utf-8 ") for url in urls]

    recv_mock = mocker.patch(
        "socket.socket.recv", 
        return_value='{"word1": 6, "word2": 5}'.encode("utf-8")
    )
    connect_mock = mocker.patch("socket.socket.connect")
    send_mock = mocker.patch("socket.socket.send")

    client = Client(3, '06/urls.txt')
    client.start()
    captured = capsys.readouterr()
    recv_data = [data for data in captured.out.split("\n")[:-1]]
    send_data = [data[0][0] for data in send_mock.call_args_list]

    assert sorted(recv_data) == sorted(expected_recv_data)
    assert sorted(send_data) == sorted(expected_send_data)
    assert recv_mock.call_count == 100
    assert send_mock.call_count == 101
    assert connect_mock.call_count == 101


def test_server_master():
    server = Server(workers_number=2, most_common_words_number=10, host="127.0.0.1", port=4000)
    master_thread = threading.Thread(target=server.listen_client_connection)
    master_thread.start()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 4000))
    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket2.connect(("127.0.0.1", 4000))
    client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket3.connect(("127.0.0.1", 4000))

    server.shutdown_event.set()
    master_thread.join()
    assert server.clients_queue.qsize() == 3


def test_parse_html(mocker):
    response = Response()
    response._content = "<html>Some text with <a>link</a></html>".encode('utf-8')
    mocker.patch("requests.get", return_value=response)
    server = Server(1, 3)
    html_text = server.parse_html("https://somesite.com")
    assert html_text == "Some text with link"


def test_count_words():
    server = Server(1, 2)
    text = "Test, teStiNg. Testcase // test, test."
    expected_data = '{"test": 3, "testing": 1}'
    count_words = server.count_words(text)
    assert count_words == expected_data
