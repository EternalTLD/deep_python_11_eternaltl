import asyncio
from unittest.mock import MagicMock
import aiohttp
import pytest

import fetcher


@pytest.mark.asyncio
async def test_invalid_url(mocker, capsys):
    url = "https://somesite.com"
    parse_mock = mocker.patch("fetcher.parse_html", return_value="Some text")
    count_words_mock = mocker.patch(
        "fetcher.get_most_common_words", return_value="{'word1': 2}"
    )
    client_mock = mocker.patch("aiohttp.ClientSession.get", return_value="Some html")

    que = asyncio.Queue()
    await que.put(url)

    task = asyncio.create_task(fetcher.fetch_workers(que, 1))
    await que.join()
    task.cancel()

    fetcher_print = capsys.readouterr().out.split("\n")
    expected_print = "https://somesite.com is broken"

    assert fetcher_print[0] == expected_print
    assert parse_mock.call_count == 0
    assert count_words_mock.call_count == 0
    assert client_mock.call_count == 1


@pytest.mark.asyncio
async def test_valid_url(mocker, capsys):
    url = "https://somesite.com"
    parse_mock = mocker.patch("fetcher.parse_html", return_value="Some text")
    count_words_mock = mocker.patch(
        "fetcher.get_most_common_words", return_value="{'word1': 2}"
    )

    client_mock = aiohttp.ClientSession
    client_mock.get = MagicMock()
    client_mock.get.return_value.__aenter__.return_value.status = 200
    client_mock.get.return_value.__aenter__.return_value.text.return_value = (
        "test content"
    )

    que = asyncio.Queue()
    await que.put(url)

    task = asyncio.create_task(fetcher.fetch_workers(que, 1))
    await que.join()
    task.cancel()

    fetcher_print = capsys.readouterr().out.split("\n")
    expected_print = "https://somesite.com: {'word1': 2}"

    assert fetcher_print[0] == expected_print
    assert parse_mock.call_count == 1
    assert count_words_mock.call_count == 1
    assert client_mock.get.call_count == 1


def test_parse_html():
    html = "<html>Some text with <a>link</a></html>"
    text = fetcher.parse_html(html)
    assert text == "Some text with link"


def test_get_most_common_words():
    text = "Test, teStiNg. Testcase // test, test."
    count_words = fetcher.get_most_common_words(text, 2)
    assert count_words == {"test": 3, "testing": 1}
