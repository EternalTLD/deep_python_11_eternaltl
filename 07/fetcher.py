from collections import Counter
import asyncio
import re
import argparse
import aiohttp
from bs4 import BeautifulSoup


async def get_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    return html


def parse_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text()
    return page_text


def get_most_common_words(text: str, most_common: int) -> dict:
    words = re.findall(r"\b[А-Яа-яA-Za-z]+\b", text.lower())
    most_common_words = Counter(words).most_common(most_common)
    return dict(most_common_words)


async def fetch_workers(que: asyncio.Queue, most_common: int) -> None:
    while True:
        url = await que.get()
        try:
            html = await get_html(url)
            text = parse_html(html)
            data = get_most_common_words(text, most_common)
            print(f"{url}: {data}")
        except aiohttp.ClientError:
            print(f"{url} is broken")
        finally:
            que.task_done()


async def run_fetcher(workers_number: int, filename: str, most_common: int) -> None:
    que = asyncio.Queue()

    workers = [
        asyncio.create_task(fetch_workers(que, most_common))
        for _ in range(workers_number)
    ]

    with open(filename, "r", encoding="utf-8") as file_object:
        for url in file_object:
            await que.put(url.strip())

    await que.join()

    for worker in workers:
        worker.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async script for processing urls")
    parser.add_argument("-c", type=int, help="Number of simultaneous requests")
    parser.add_argument("filename", help="File with urls")
    parser.add_argument("most_common", type=int, help="Number of most common words")
    args = parser.parse_args()

    asyncio.run(run_fetcher(args.c, args.filename, args.most_common))
